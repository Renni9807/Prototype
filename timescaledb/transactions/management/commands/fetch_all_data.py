from django.core.management.base import BaseCommand
from django.utils import timezone
from transactions.models import Swap, Mint, Burn, EthUsdcOhlcv
from decimal import Decimal
from django.utils.crypto import get_random_string
from typing import Any, Dict, List
import os
import time
from datetime import datetime, timedelta
from dateutil import tz
from dotenv import load_dotenv
from transactions.fetchers.fetch_swaps import fetch_swaps
from transactions.fetchers.fetch_mints import fetch_mints
from transactions.fetchers.fetch_burns import fetch_burns
from transactions.fetchers.fetch_ohlcv import create_ohlcv

load_dotenv()

class Command(BaseCommand):
    help = 'Fetches swaps, mints, burns, and creates OHLCV data while measuring time taken.'

    def handle(self, *args, **options) -> None:
        SUBGRAPH_URL: str = os.getenv("API_URL")
        self.ETH_USDC_POOL_ADDRESS = "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8".lower()

        end_timestamp: int = int(time.time())
        start_timestamp: int = self.get_unix_timestamp_n_days_ago(1)
        print(f"Fetching data from {datetime.fromtimestamp(start_timestamp)} to {datetime.fromtimestamp(end_timestamp)}")

        total_start_time: float = time.time()

        # Fetch and save swaps
        swaps_start_time: float = time.time()
        swaps: List[Dict[str, Any]] = fetch_swaps(
            subgraph_url=SUBGRAPH_URL,
            pool_address=self.ETH_USDC_POOL_ADDRESS,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
        self.save_swaps(swaps)
        swaps_elapsed_time: float = time.time() - swaps_start_time
        print(f"Fetched and saved {len(swaps)} swaps in {swaps_elapsed_time:.2f} seconds.")

        # Fetch and save mints
        mints_start_time: float = time.time()
        mints: List[Dict[str, Any]] = fetch_mints(
            subgraph_url=SUBGRAPH_URL,
            pool_address=self.ETH_USDC_POOL_ADDRESS,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
        self.save_mints(mints)
        mints_elapsed_time: float = time.time() - mints_start_time
        print(f"Fetched and saved {len(mints)} mints in {mints_elapsed_time:.2f} seconds.")

        # Fetch and save burns
        burns_start_time: float = time.time()
        burns: List[Dict[str, Any]] = fetch_burns(
            subgraph_url=SUBGRAPH_URL,
            pool_address=self.ETH_USDC_POOL_ADDRESS,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
        self.save_burns(burns)
        burns_elapsed_time: float = time.time() - burns_start_time
        print(f"Fetched and saved {len(burns)} burns in {burns_elapsed_time:.2f} seconds.")

        # Create and save OHLCV data
        ohlcv_start_time: float = time.time()
        token0_decimals: int = 6  # USDC has 6 decimals
        token1_decimals: int = 18  # WETH has 18 decimals
        ohlcv: List[Dict[str, Any]] = create_ohlcv(
            swaps=swaps,
            token0_decimals=token0_decimals,
            token1_decimals=token1_decimals
        )
        self.save_ohlcv(ohlcv)
        ohlcv_elapsed_time: float = time.time() - ohlcv_start_time
        print(f"Created and saved {len(ohlcv)} OHLCV records in {ohlcv_elapsed_time:.2f} seconds.")

        total_elapsed_time: float = time.time() - total_start_time
        print(f"Total time taken: {total_elapsed_time:.2f} seconds.")

        self.save_swaps(swaps)
        self.save_mints(mints)
        self.save_burns(burns)
        self.save_ohlcv(ohlcv)
        
    def get_unix_timestamp_n_days_ago(self, days: int) -> int:
        n_days_ago: datetime = datetime.now(tz=tz.UTC) - timedelta(days=days)
        return int(n_days_ago.timestamp())

    def save_swaps(self, swaps: List[Dict[str, Any]]):
        for swap in swaps:
            print(swap['id'])

            Swap.objects.create(
                id=swap['id'],
                amount0=swap['amount0'],
                amount1=swap['amount1'],
                pool_id=self.ETH_USDC_POOL_ADDRESS,
                recipient=swap['recipient'],
                sender=swap['sender'],
                sqrtPriceX96=swap['sqrtPriceX96'],
                tick=swap['tick'],
                timestamp=timezone.make_aware(datetime.fromtimestamp(int(swap['timestamp'])))
            )

    def save_mints(self, mints: List[Dict[str, Any]]):
        for mint in mints:
            Mint.objects.create(
                id=mint['id'],
                amount=mint['amount'],
                amount0=mint['amount0'],
                amount1=mint['amount1'],
                owner=mint['owner'],
                pool_id=self.ETH_USDC_POOL_ADDRESS,
                sender=mint['sender'],
                tickLower=mint['tickLower'],
                tickUpper=mint['tickUpper'],
                timestamp=timezone.make_aware(datetime.fromtimestamp(int(mint['timestamp'])))
            )

    def save_burns(self, burns: List[Dict[str, Any]]):
        for burn in burns:
            Burn.objects.create(
                id=burn['id'],
                amount=burn['amount'],
                amount0=burn['amount0'],
                amount1=burn['amount1'],
                owner=burn['owner'],
                pool_id=self.ETH_USDC_POOL_ADDRESS,
                tickLower=burn['tickLower'],
                tickUpper=burn['tickUpper'],
                timestamp=timezone.make_aware(datetime.fromtimestamp(int(burn['timestamp'])))
            )

    def save_ohlcv(self, ohlcv_data: List[Dict[str, Any]]):
        for ohlcv in ohlcv_data:
            EthUsdcOhlcv.objects.create(
                timestamp=timezone.make_aware(datetime.strptime(ohlcv['timestamp'], '%Y-%m-%d %H:%M:%S')),
                open=Decimal(ohlcv['open']),
                high=Decimal(ohlcv['high']),
                low=Decimal(ohlcv['low']),
                close=Decimal(ohlcv['close']),
                volume=Decimal(ohlcv['volume'])
            )
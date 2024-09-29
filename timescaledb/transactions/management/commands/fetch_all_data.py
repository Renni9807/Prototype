import os
import time
from datetime import datetime
from typing import List, Dict, Any

from django.core.management.base import BaseCommand

from transactions.fetchers.fetch_swaps import fetch_swaps
from transactions.fetchers.fetch_mints import fetch_mints
from transactions.fetchers.fetch_burns import fetch_burns
from transactions.fetchers.fetch_ohlcv import create_ohlcv

class Command(BaseCommand):
    help = 'Fetches swaps, mints, burns, and creates OHLCV data while measuring time taken.'

    def handle(self, *args, **options) -> None:
        SUBGRAPH_URL: str = os.getenv("API_URL")
        self.ETH_USDC_POOL_ADDRESS = "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8".lower()

        end_timestamp: int = int(time.time())
        start_timestamp: int = self.get_unix_timestamp_n_days_ago(1)
        print(f"Fetching data from {datetime.fromtimestamp(start_timestamp)} to {datetime.fromtimestamp(end_timestamp)}")

        total_start_time: float = time.time()

        # Fetch swaps
        swaps_start_time: float = time.time()
        swaps: List[Dict[str, Any]] = fetch_swaps(
            subgraph_url=SUBGRAPH_URL,
            pool_address=self.ETH_USDC_POOL_ADDRESS,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
        self.print_swaps(swaps)
        swaps_elapsed_time: float = time.time() - swaps_start_time
        print(f"Fetched {len(swaps)} swaps in {swaps_elapsed_time:.2f} seconds.")

        # Fetch mints
        mints_start_time: float = time.time()
        mints: List[Dict[str, Any]] = fetch_mints(
            subgraph_url=SUBGRAPH_URL,
            pool_address=self.ETH_USDC_POOL_ADDRESS,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
        self.print_mints(mints)
        mints_elapsed_time: float = time.time() - mints_start_time
        print(f"Fetched {len(mints)} mints in {mints_elapsed_time:.2f} seconds.")

        # Fetch burns
        burns_start_time: float = time.time()
        burns: List[Dict[str, Any]] = fetch_burns(
            subgraph_url=SUBGRAPH_URL,
            pool_address=self.ETH_USDC_POOL_ADDRESS,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
        self.print_burns(burns)
        burns_elapsed_time: float = time.time() - burns_start_time
        print(f"Fetched {len(burns)} burns in {burns_elapsed_time:.2f} seconds.")

        # Create OHLCV data
        ohlcv_start_time: float = time.time()
        token0_decimals: int = 6  # USDC has 6 decimals
        token1_decimals: int = 18  # WETH has 18 decimals
        ohlcv: List[Dict[str, Any]] = create_ohlcv(
            swaps=swaps,
            token0_decimals=token0_decimals,
            token1_decimals=token1_decimals
        )
        self.print_ohlcv(ohlcv)
        ohlcv_elapsed_time: float = time.time() - ohlcv_start_time
        print(f"Created {len(ohlcv)} OHLCV records in {ohlcv_elapsed_time:.2f} seconds.")

        total_elapsed_time: float = time.time() - total_start_time
        print(f"Total time taken: {total_elapsed_time:.2f} seconds.")

    def print_swaps(self, swaps: List[Dict[str, Any]]):
        print("\n--- SWAPS ---")
        for swap in swaps:
            print(f"ID: {swap['id']}")
            print(f"Amount0: {swap['amount0']}")
            print(f"Amount1: {swap['amount1']}")
            print(f"Recipient: {swap.get('recipient', 'N/A')}")
            print(f"Sender: {swap['sender']}")
            print(f"SqrtPriceX96: {swap['sqrtPriceX96']}")
            print(f"Tick: {swap['tick']}")
            print(f"Timestamp: {datetime.fromtimestamp(int(swap['timestamp']))}")
            print("---")

    def print_mints(self, mints: List[Dict[str, Any]]):
        print("\n--- MINTS ---")
        for mint in mints:
            print(f"ID: {mint['id']}")
            print(f"Amount: {mint['amount']}")
            print(f"Amount0: {mint['amount0']}")
            print(f"Amount1: {mint['amount1']}")
            print(f"Owner: {mint['owner']}")
            print(f"Sender: {mint['sender']}")
            print(f"TickLower: {mint['tickLower']}")
            print(f"TickUpper: {mint['tickUpper']}")
            print(f"Timestamp: {datetime.fromtimestamp(int(mint['timestamp']))}")
            print("---")

    def print_burns(self, burns: List[Dict[str, Any]]):
        print("\n--- BURNS ---")
        for burn in burns:
            print(f"ID: {burn['id']}")
            print(f"Amount: {burn['amount']}")
            print(f"Amount0: {burn['amount0']}")
            print(f"Amount1: {burn['amount1']}")
            print(f"Owner: {burn['owner']}")
            print(f"TickLower: {burn['tickLower']}")
            print(f"TickUpper: {burn['tickUpper']}")
            print(f"Timestamp: {datetime.fromtimestamp(int(burn['timestamp']))}")
            print("---")

    def print_ohlcv(self, ohlcv_data: List[Dict[str, Any]]):
        print("\n--- OHLCV ---")
        for ohlcv in ohlcv_data:
            print(f"Timestamp: {ohlcv['timestamp']}")
            print(f"Open: {ohlcv['open']}")
            print(f"High: {ohlcv['high']}")
            print(f"Low: {ohlcv['low']}")
            print(f"Close: {ohlcv['close']}")
            print(f"Volume: {ohlcv['volume']}")
            print("---")
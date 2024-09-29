from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
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

# Create your views here.

load_dotenv()

class MeasureDataFetchTimeView(View):
    def get(self, request) -> JsonResponse:
        SUBGRAPH_URL: str = os.getenv("API_URL")
        ETH_USDC_POOL_ADDRESS: str = "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8".lower()

        # Define time range (e.g., last 30 days)
        end_timestamp: int = int(time.time())
        start_timestamp: int = self.get_unix_timestamp_n_days_ago(30)

        total_start_time: float = time.time()

        # Fetch swaps
        swaps_start_time: float = time.time()
        swaps: List[Dict[str, Any]] = fetch_swaps(
            subgraph_url=SUBGRAPH_URL,
            pool_address=ETH_USDC_POOL_ADDRESS,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
        swaps_elapsed_time: float = time.time() - swaps_start_time

        # Fetch mints
        mints_start_time: float = time.time()
        mints: List[Dict[str, Any]] = fetch_mints(
            subgraph_url=SUBGRAPH_URL,
            pool_address=ETH_USDC_POOL_ADDRESS,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
        mints_elapsed_time: float = time.time() - mints_start_time

        # Fetch burns
        burns_start_time: float = time.time()
        burns: List[Dict[str, Any]] = fetch_burns(
            subgraph_url=SUBGRAPH_URL,
            pool_address=ETH_USDC_POOL_ADDRESS,
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp
        )
        burns_elapsed_time: float = time.time() - burns_start_time

        # Create OHLCV data
        ohlcv_start_time: float = time.time()
        # Assuming token0_decimals and token1_decimals are known; replace with actual values
        token0_decimals: int = 6  # Example: USDC has 6 decimals
        token1_decimals: int = 18  # Example: WETH has 18 decimals
        ohlcv: List[Dict[str, Any]] = create_ohlcv(
            swaps=swaps,
            token0_decimals=token0_decimals,
            token1_decimals=token1_decimals
        )
        ohlcv_elapsed_time: float = time.time() - ohlcv_start_time

        total_elapsed_time: float = time.time() - total_start_time

        response_data: Dict[str, Any] = {
            "swaps_fetched": len(swaps),
            "swaps_time_seconds": swaps_elapsed_time,
            "mints_fetched": len(mints),
            "mints_time_seconds": mints_elapsed_time,
            "burns_fetched": len(burns),
            "burns_time_seconds": burns_elapsed_time,
            "ohlcv_created": len(ohlcv),
            "ohlcv_time_seconds": ohlcv_elapsed_time,
            "total_time_seconds": total_elapsed_time
        }

        return JsonResponse(response_data)

    def get_unix_timestamp_n_days_ago(self, days: int) -> int:
        """Returns the UNIX timestamp of n days ago."""
        n_days_ago: datetime = datetime.now(tz=tz.UTC) - timedelta(days=days)
        return int(n_days_ago.timestamp())

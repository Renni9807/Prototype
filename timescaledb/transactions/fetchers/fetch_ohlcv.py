from typing import Any, Dict, List
from datetime import datetime, timedelta
from dateutil import tz

def get_price_from_sqrtPriceX96(sqrtPriceX96: str, token0_decimals: int, token1_decimals: int) -> float:
    """Calculate price from sqrtPriceX96."""
    sqrt_price = float(sqrtPriceX96) / (2 ** 96)
    price = sqrt_price ** 2
    decimal_adjustment = 10 ** (token0_decimals - token1_decimals)
    return price * decimal_adjustment

def create_ohlcv(swaps: List[Dict[str, Any]], token0_decimals: int, token1_decimals: int) -> List[Dict[str, Any]]:
    """Convert swap data to OHLCV data."""
    ohlcv_data: Dict[str, Dict[str, Any]] = {}
    from_zone = tz.tzutc()
    to_zone = tz.gettz('Asia/Hong_Kong')  # HKT

    for swap in swaps:
        timestamp = int(swap["timestamp"])
        utc_time = datetime.fromtimestamp(timestamp, tz=from_zone)
        hk_time = utc_time.astimezone(to_zone)

        # Assume trading day starts at 09:00 AM HKT
        if hk_time.hour < 9:
            open_time = hk_time.replace(hour=9, minute=0, second=0, microsecond=0) - timedelta(days=1)
        else:
            open_time = hk_time.replace(hour=9, minute=0, second=0, microsecond=0)

        period = open_time.strftime('%Y-%m-%d %H:%M:%S')

        price = get_price_from_sqrtPriceX96(sqrtPriceX96=swap["sqrtPriceX96"], token0_decimals=token0_decimals, token1_decimals=token1_decimals)

        if period not in ohlcv_data:
            ohlcv_data[period] = {
                "open": price,
                "high": price,
                "low": price,
                "close": price,
                "volume": 0.0,
                "timestamp": period
            }
        else:
            ohlcv_data[period]["high"] = max(ohlcv_data[period]["high"], price)
            ohlcv_data[period]["low"] = min(ohlcv_data[period]["low"], price)
            ohlcv_data[period]["close"] = price

        try:
            volume = abs(float(swap["amount0"]))
            ohlcv_data[period]["volume"] += volume
        except ValueError:
            print(f"Invalid amount0 value: {swap['amount0']} at timestamp {timestamp}")

    ohlcv_list: List[Dict[str, Any]] = sorted(ohlcv_data.values(), key=lambda x: x["timestamp"])
    return ohlcv_list

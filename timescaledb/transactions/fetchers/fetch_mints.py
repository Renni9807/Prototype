import requests
from typing import Any, Dict, List
import time
from datetime import datetime, timedelta
from dateutil import tz

def fetch_mints(
    subgraph_url: str,
    pool_address: str,
    start_timestamp: int,
    end_timestamp: int,
    page_size: int = 1000,
    max_mints: int = 1000000,
    max_runtime: int = 500
) -> List[Dict[str, Any]]:
    """Fetches mint events from the Uniswap V3 Subgraph within the given time range."""
    mints: List[Dict[str, Any]] = []
    skip: int = 0
    start_time: float = time.time()

    while True:
        if time.time() - start_time > max_runtime:
            print(f"Maximum runtime of {max_runtime} seconds reached. Stopping.")
            break

        if len(mints) >= max_mints:
            print(f"Maximum number of mints ({max_mints}) reached. Stopping.")
            break

        query: str = f"""
        query ($poolAddress: String!, $startTime: Int!, $endTime: Int!, $skip: Int!) {{
          mints(
            where: {{
              pool: $poolAddress,
              timestamp_gte: $startTime,
              timestamp_lt: $endTime
            }},
            orderBy: timestamp,
            orderDirection: asc,
            first: {page_size},
            skip: $skip
          ) {{
            id
            amount
            amount0
            amount1
            tickLower
            tickUpper
            timestamp
            sender
            owner
          }}
        }}
        """

        variables: Dict[str, Any] = {
            "poolAddress": pool_address,
            "startTime": start_timestamp,
            "endTime": end_timestamp,
            "skip": skip
        }

        try:
            print(f"Sending request with skip={skip}")
            response: requests.Response = requests.post(
                subgraph_url,
                json={"query": query, "variables": variables}
            )
            response.raise_for_status()
            data: Dict[str, Any] = response.json()

            if "errors" in data:
                print("GraphQL Errors:", data["errors"])
                break

            if "data" not in data or "mints" not in data["data"]:
                print("Unexpected response structure:", data)
                break

            fetched_mints: List[Dict[str, Any]] = data["data"]["mints"]
            mints.extend(fetched_mints)

            print(f"Fetched {len(fetched_mints)} mints. Total so far: {len(mints)}")
            print(f"Elapsed time: {time.time() - start_time:.2f} seconds")

            if len(fetched_mints) < page_size:
                print("Reached end of data")
                break

            skip += page_size
            time.sleep(0.2)

        except requests.exceptions.RequestException as e:
            print("Request failed:", e)
            break

    return mints

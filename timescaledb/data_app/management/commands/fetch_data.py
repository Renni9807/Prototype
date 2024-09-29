from datetime import timezone as datetime_timezone
from datetime import datetime, timedelta
import time
from decimal import Decimal, getcontext

from django.core.management.base import BaseCommand
from django.utils import timezone

from data_app.models import Swap, Mint, Burn, OHLCV
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from dateutil import tz
from dotenv import load_dotenv
import os

load_dotenv()

class Command(BaseCommand):
    help = 'Fetch Uniswap data from The Graph and store it in TimescaleDB.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data fetch...'))

        # Configuration
        SUBGRAPH_URL = os.getenv("API_URL")
        if not SUBGRAPH_URL:
            self.stdout.write(self.style.ERROR('API_URL is not set in environment variables.'))
            return

        ETH_USDC_POOL_ADDRESS = "0x8ad599c3a0ff1de082011efddc58f1908eb6e6d8".lower()
        getcontext().prec = 28  # Set decimal precision

        # Set up GraphQL client
        transport = RequestsHTTPTransport(
            url=SUBGRAPH_URL,
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        # Set timestamps (fetch data from the last 30 days)
        end_timestamp = int(time.time())
        start_timestamp = end_timestamp - 86400 * 30  # 30 days ago

        # Fetch data
        swaps = self.fetch_swaps(client, ETH_USDC_POOL_ADDRESS, start_timestamp, end_timestamp)
        mints = self.fetch_mints(client, ETH_USDC_POOL_ADDRESS, start_timestamp, end_timestamp)
        burns = self.fetch_burns(client, ETH_USDC_POOL_ADDRESS, start_timestamp, end_timestamp)

        # Save data
        self.save_swaps(swaps)
        self.save_mints(mints)
        self.save_burns(burns)

        # Generate and save OHLCV data
        ohlcv_data = self.create_ohlcv(swaps)
        self.save_ohlcv(ohlcv_data)

        self.stdout.write(self.style.SUCCESS('Data fetch and storage completed.'))

    def fetch_swaps(self, client, pool_address, start_time, end_time):
        """Fetch swaps data from The Graph API."""
        self.stdout.write('Fetching Swaps data...')
        swaps = []
        skip = 0
        batch_size = 1000

        while True:
            query = gql("""
            query ($poolAddress: String!, $startTime: BigInt!, $endTime: BigInt!, $first: Int!, $skip: Int!) {
                swaps(
                    first: $first,
                    skip: $skip,
                    orderBy: timestamp,
                    orderDirection: asc,
                    where: {pool: $poolAddress, timestamp_gte: $startTime, timestamp_lte: $endTime}
                ) {
                    id
                    amount0
                    amount1
                    tick
                    sqrtPriceX96
                    timestamp
                    sender
                    recipient
                    pool {
                        id
                    }
                }
            }
            """)

            variables = {
                "poolAddress": pool_address,
                "startTime": start_time,
                "endTime": end_time,
                "first": batch_size,
                "skip": skip
            }

            try:
                result = client.execute(query, variable_values=variables)
                fetched_swaps = result['swaps']
                swaps.extend(fetched_swaps)

                self.stdout.write(f"Fetched {len(fetched_swaps)} swaps.")

                if len(fetched_swaps) < batch_size:
                    break
                else:
                    skip += batch_size

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching swaps: {e}"))
                break

        self.stdout.write(f"Total swaps fetched: {len(swaps)}")
        return swaps

    def fetch_mints(self, client, pool_address, start_time, end_time):
        """Fetch mints data from The Graph API."""
        self.stdout.write('Fetching Mints data...')
        mints = []
        skip = 0
        batch_size = 1000

        while True:
            query = gql("""
            query ($poolAddress: String!, $startTime: BigInt!, $endTime: BigInt!, $first: Int!, $skip: Int!) {
                mints(
                    first: $first,
                    skip: $skip,
                    orderBy: timestamp,
                    orderDirection: asc,
                    where: {pool: $poolAddress, timestamp_gte: $startTime, timestamp_lte: $endTime}
                ) {
                    id
                    amount
                    amount0
                    amount1
                    tickLower
                    tickUpper
                    timestamp
                    sender
                    owner
                    pool {
                        id
                    }
                }
            }
            """)

            variables = {
                "poolAddress": pool_address,
                "startTime": start_time,
                "endTime": end_time,
                "first": batch_size,
                "skip": skip
            }

            try:
                result = client.execute(query, variable_values=variables)
                fetched_mints = result['mints']
                mints.extend(fetched_mints)

                self.stdout.write(f"Fetched {len(fetched_mints)} mints.")

                if len(fetched_mints) < batch_size:
                    break
                else:
                    skip += batch_size

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching mints: {e}"))
                break

        self.stdout.write(f"Total mints fetched: {len(mints)}")
        return mints

    def fetch_burns(self, client, pool_address, start_time, end_time):
        """Fetch burns data from The Graph API."""
        self.stdout.write('Fetching Burns data...')
        burns = []
        skip = 0
        batch_size = 1000

        while True:
            query = gql("""
            query ($poolAddress: String!, $startTime: BigInt!, $endTime: BigInt!, $first: Int!, $skip: Int!) {
                burns(
                    first: $first,
                    skip: $skip,
                    orderBy: timestamp,
                    orderDirection: asc,
                    where: {pool: $poolAddress, timestamp_gte: $startTime, timestamp_lte: $endTime}
                ) {
                    id
                    amount
                    amount0
                    amount1
                    tickLower
                    tickUpper
                    timestamp
                    owner
                    pool {
                        id
                    }
                }
            }
            """)

            variables = {
                "poolAddress": pool_address,
                "startTime": start_time,
                "endTime": end_time,
                "first": batch_size,
                "skip": skip
            }

            try:
                result = client.execute(query, variable_values=variables)
                fetched_burns = result['burns']
                burns.extend(fetched_burns)

                self.stdout.write(f"Fetched {len(fetched_burns)} burns.")

                if len(fetched_burns) < batch_size:
                    break
                else:
                    skip += batch_size

            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching burns: {e}"))
                break

        self.stdout.write(f"Total burns fetched: {len(burns)}")
        return burns

    def save_swaps(self, swaps):
        """Save swaps data to the database with duplicate checking."""
        self.stdout.write('Saving Swaps data...')
        swap_objects = []
        for swap in swaps:
            swap_objects.append(
                Swap(
                    event_id=swap['id'],
                    amount0=Decimal(swap['amount0']),
                    amount1=Decimal(swap['amount1']),
                    pool_id=swap['pool']['id'],
                    recipient=swap['recipient'],
                    sender=swap['sender'],
                    sqrtPriceX96=Decimal(swap['sqrtPriceX96']),
                    tick=int(swap['tick']),
                    timestamp=datetime.fromtimestamp(int(swap['timestamp']), tz=datetime_timezone.utc),
                )
            )
        # Bulk upsert (update or create)
        Swap.objects.bulk_create(
            swap_objects,
            update_conflicts=True,
            unique_fields=['event_id', 'timestamp'],
            update_fields=['amount0', 'amount1', 'pool_id', 'recipient', 'sender', 'sqrtPriceX96', 'tick', 'updated_at']
        )
        self.stdout.write(f"{len(swap_objects)} swaps records saved.")

    def save_mints(self, mints):
        """Save mints data to the database with duplicate checking."""
        self.stdout.write('Saving Mints data...')
        mint_objects = []
        for mint in mints:
            mint_objects.append(
                Mint(
                    event_id=mint['id'],
                    amount=Decimal(mint['amount']),
                    amount0=Decimal(mint['amount0']),
                    amount1=Decimal(mint['amount1']),
                    owner=mint['owner'],
                    pool_id=mint['pool']['id'],
                    sender=mint.get('sender', ''),
                    tickLower=int(mint['tickLower']),
                    tickUpper=int(mint['tickUpper']),
                    timestamp=datetime.fromtimestamp(int(mint['timestamp']), tz=datetime_timezone.utc),
                )
            )
        Mint.objects.bulk_create(
            mint_objects,
            update_conflicts=True,
            unique_fields=['event_id', 'timestamp'],
            update_fields=['amount', 'amount0', 'amount1', 'owner', 'pool_id', 'sender', 'tickLower', 'tickUpper', 'updated_at']
        )
        self.stdout.write(f"{len(mint_objects)} mints records saved.")

    def save_burns(self, burns):
        """Save burns data to the database with duplicate checking."""
        self.stdout.write('Saving Burns data...')
        burn_objects = []
        for burn in burns:
            burn_objects.append(
                Burn(
                    event_id=burn['id'],
                    amount=Decimal(burn['amount']),
                    amount0=Decimal(burn['amount0']),
                    amount1=Decimal(burn['amount1']),
                    owner=burn['owner'],
                    pool_id=burn['pool']['id'],
                    tickLower=int(burn['tickLower']),
                    tickUpper=int(burn['tickUpper']),
                    timestamp=datetime.fromtimestamp(int(burn['timestamp']), tz=datetime_timezone.utc),
                )
            )
        Burn.objects.bulk_create(
            burn_objects,
            update_conflicts=True,
            unique_fields=['event_id', 'timestamp'],
            update_fields=['amount', 'amount0', 'amount1', 'owner', 'pool_id', 'tickLower', 'tickUpper', 'updated_at']
        )
        self.stdout.write(f"{len(burn_objects)} burns records saved.")

    def create_ohlcv(self, swaps):
        """Create OHLCV data from swaps."""
        self.stdout.write('Creating OHLCV data...')
        ohlcv_data = {}
        from_zone = tz.tzutc()
        to_zone = tz.gettz('Asia/Hong_Kong')  # Hong Kong timezone

        for swap in swaps:
            timestamp = int(swap["timestamp"])
            utc_time = datetime.fromtimestamp(timestamp, tz=from_zone)
            hk_time = utc_time.astimezone(to_zone)

            # Group by date
            period = hk_time.strftime('%Y-%m-%d')

            price = self.calculate_price_from_sqrtPriceX96(swap["sqrtPriceX96"])

            if period not in ohlcv_data:
                ohlcv_data[period] = {
                    "timestamp": datetime.strptime(period, '%Y-%m-%d').replace(tzinfo=to_zone),
                    "open": price,
                    "high": price,
                    "low": price,
                    "close": price,
                    "volume": Decimal(abs(float(swap["amount0"]))),
                }
            else:
                ohlcv_data[period]["high"] = max(ohlcv_data[period]["high"], price)
                ohlcv_data[period]["low"] = min(ohlcv_data[period]["low"], price)
                ohlcv_data[period]["close"] = price
                ohlcv_data[period]["volume"] += Decimal(abs(float(swap["amount0"])))

        ohlcv_list = sorted(ohlcv_data.values(), key=lambda x: x["timestamp"])
        self.stdout.write(f"Generated {len(ohlcv_list)} OHLCV records.")
        return ohlcv_list

    def save_ohlcv(self, ohlcv_data):
        """Save OHLCV data to the database with duplicate checking."""
        self.stdout.write('Saving OHLCV data...')
        ohlcv_objects = []
        for data in ohlcv_data:
            ohlcv_objects.append(
                OHLCV(
                    timestamp=data['timestamp'],
                    open=Decimal(data['open']),
                    high=Decimal(data['high']),
                    low=Decimal(data['low']),
                    close=Decimal(data['close']),
                    volume=data['volume'],
                )
            )
        # Bulk upsert for OHLCV data
        OHLCV.objects.bulk_create(
            ohlcv_objects,
            update_conflicts=True,
            unique_fields=['timestamp'],
            update_fields=['open', 'high', 'low', 'close', 'volume']
        )
        self.stdout.write(f"{len(ohlcv_objects)} OHLCV records saved.")

    def calculate_price_from_sqrtPriceX96(self, sqrtPriceX96):
        """Calculate price from sqrtPriceX96 value."""
        sqrtPriceX96 = Decimal(sqrtPriceX96)
        Q96 = Decimal(2 ** 96)
        price = (sqrtPriceX96 / Q96) ** 2
        # Adjust for token decimals (assuming USDC/WETH pool)
        decimal_adjustment = Decimal(10) ** (6 - 18)
        adjusted_price = price * decimal_adjustment
        # Convert WETH price to USDC
        if adjusted_price != 0:
            adjusted_price = Decimal(1) / adjusted_price
        else:
            adjusted_price = Decimal(0)
        return float(adjusted_price)

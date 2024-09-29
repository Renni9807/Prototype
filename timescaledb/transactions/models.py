from django.db import models
from django.utils import timezone

class Burn(models.Model):
    event_id = models.TextField()  # 'id'에서 'event_id'로 변경
    amount = models.TextField()
    amount0 = models.TextField()
    amount1 = models.TextField()
    owner = models.TextField()
    pool_id = models.TextField()
    tickLower = models.IntegerField()
    tickUpper = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)  # 파티셔닝 키
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'burn'
        unique_together = ('event_id', 'timestamp')  # 고유 제약 조건 설정

class Mint(models.Model):
    event_id = models.TextField()
    amount = models.TextField()
    amount0 = models.TextField()
    amount1 = models.TextField()
    owner = models.TextField()
    pool_id = models.TextField()
    sender = models.TextField()
    tickLower = models.IntegerField()
    tickUpper = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mint'
        unique_together = ('event_id', 'timestamp')

class Swap(models.Model):
    event_id = models.TextField()
    amount0 = models.TextField()
    amount1 = models.TextField()
    pool_id = models.TextField()
    recipient = models.TextField()
    sender = models.TextField()
    sqrtPriceX96 = models.TextField()
    tick = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'swap'
        unique_together = ('event_id', 'timestamp')

class EthUsdcOhlcv(models.Model):
    timestamp = models.DateTimeField(primary_key=True)
    open = models.DecimalField(max_digits=20, decimal_places=8)
    high = models.DecimalField(max_digits=20, decimal_places=8)
    low = models.DecimalField(max_digits=20, decimal_places=8)
    close = models.DecimalField(max_digits=20, decimal_places=8)
    volume = models.DecimalField(max_digits=30, decimal_places=10)

    class Meta:
        db_table = 'ethusdcohlcv'

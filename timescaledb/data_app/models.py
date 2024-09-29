from django.db import models

class OHLCV(models.Model):
    timestamp = models.DateTimeField(primary_key=True, db_index=True)
    open = models.DecimalField(max_digits=30, decimal_places=10)
    high = models.DecimalField(max_digits=30, decimal_places=10)
    low = models.DecimalField(max_digits=30, decimal_places=10)
    close = models.DecimalField(max_digits=30, decimal_places=10)
    volume = models.DecimalField(max_digits=40, decimal_places=20)

    class Meta:
        db_table = 'ohlcv'

class Swap(models.Model):
    event_id = models.TextField()
    amount0 = models.DecimalField(max_digits=50, decimal_places=20)
    amount1 = models.DecimalField(max_digits=50, decimal_places=20)
    pool_id = models.TextField()
    recipient = models.TextField()
    sender = models.TextField()
    sqrtPriceX96 = models.DecimalField(max_digits=80, decimal_places=40)
    tick = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'swap'
        unique_together = (('event_id', 'timestamp'),)

class Mint(models.Model):
    event_id = models.TextField()
    amount = models.DecimalField(max_digits=50, decimal_places=20)
    amount0 = models.DecimalField(max_digits=50, decimal_places=20)
    amount1 = models.DecimalField(max_digits=50, decimal_places=20)
    owner = models.TextField()
    pool_id = models.TextField()
    sender = models.TextField()
    tickLower = models.IntegerField()
    tickUpper = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'mint'
        unique_together = (('event_id', 'timestamp'),)

class Burn(models.Model):
    event_id = models.TextField()
    amount = models.DecimalField(max_digits=50, decimal_places=20)
    amount0 = models.DecimalField(max_digits=50, decimal_places=20)
    amount1 = models.DecimalField(max_digits=50, decimal_places=20)
    owner = models.TextField()
    pool_id = models.TextField()
    tickLower = models.IntegerField()
    tickUpper = models.IntegerField()
    timestamp = models.DateTimeField(db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'burn'
        unique_together = (('event_id', 'timestamp'),)

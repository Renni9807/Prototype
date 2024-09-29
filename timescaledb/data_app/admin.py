from django.contrib import admin
from .models import Swap, Mint, Burn, OHLCV

# Register your models here.
admin.site.register(Swap)
admin.site.register(Mint)
admin.site.register(Burn)
admin.site.register(OHLCV)
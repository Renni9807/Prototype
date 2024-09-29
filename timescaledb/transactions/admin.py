from django.contrib import admin
from .models import Burn, Mint, Swap, EthUsdcOhlcv

# Register your models here.
admin.site.register(Burn)
admin.site.register(Mint)
admin.site.register(Swap)
admin.site.register(EthUsdcOhlcv)

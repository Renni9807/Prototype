from django.shortcuts import render
from .models import Swap, Mint, Burn, OHLCV

# Create your views here.
def dashboard(request):
    context = {
        'swap_count': Swap.objects.count(),
        'mint_count': Mint.objects.count(),
        'burn_count': Burn.objects.count(),
        'ohlcv_count': OHLCV.objects.count(),
        'latest_ohlcv': OHLCV.objects.order_by('-timestamp').first()
    }
    
    return render(request, 'data_app/dashboard.html', context)
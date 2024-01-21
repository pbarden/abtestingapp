from django.shortcuts import render
from django.http import HttpResponse
from scipy.stats import norm
from .forms import PreTestAnalysisForm

def index(request):
    if request.method == 'POST':
        form = PreTestAnalysisForm(request.POST)
        if form.is_valid():
            result = weekly_mde(form.cleaned_data['weekly_visitors'], form.cleaned_data['weekly_conversions'])
            return render(request, 'pre_test_analysis/result.html', {'result': result})
    else:
        form = PreTestAnalysisForm()
    return render(request, 'pre_test_analysis/index.html', {'form': form})

def weekly_mde(weekly_visitors, weekly_conversions, total_weeks=6, alpha=0.05, power=0.8):
    weekly_mdes = []
    for week in range(1, total_weeks + 1):
        cumulative_visitors = weekly_visitors * week
        cumulative_conversions = weekly_conversions * week
        conversion_rate = cumulative_conversions / cumulative_visitors
        standard_deviation = (conversion_rate * (1 - conversion_rate)) ** 0.5
        z_alpha = norm.ppf(1 - alpha / 2)
        z_power = norm.ppf(power)
        mde = (z_alpha + z_power) * standard_deviation / (cumulative_visitors ** 0.5)
        weekly_mdes.append(mde)
    return {
        "weekly_mdes" : weekly_mdes,
        "conversion_rate" : conversion_rate,
        "weekly_visitors": weekly_visitors, 
        "weekly_conversions": weekly_conversions
    }
from django.shortcuts import render
from django.http import HttpResponse
from scipy.stats import norm
import scipy.stats as stats
from .forms import PostTestAnalysisForm
from math import sqrt

def index(request):
    if request.method == 'POST':
        form = PostTestAnalysisForm(request.POST)
        if form.is_valid():
            # Extract form data
            test_duration = form.cleaned_data['test_duration']
            control_visitors = form.cleaned_data['control_visitors']
            control_conversions = form.cleaned_data['control_conversions']
            variant_visitors = form.cleaned_data['variant_visitors']
            variant_conversions = form.cleaned_data['variant_conversions']

            # Run each of your statistical functions
            basic_metrics = calculate_basic_metrics(control_visitors, control_conversions, variant_visitors, variant_conversions)
            stats_results = calculate_statistical_significance_and_power(control_visitors, control_conversions, variant_visitors, variant_conversions)
            confidence_intervals = calculate_confidence_intervals(control_visitors, control_conversions, variant_visitors, variant_conversions)
            mde = calculate_mde(control_visitors, control_conversions)
            required_sample_size = calculate_required_sample_size(control_conversions / control_visitors, mde)
            suggested_test_duration = estimate_test_duration(required_sample_size, (control_visitors + variant_visitors) / test_duration)

            control_rate = control_conversions / control_visitors
            variant_rate = variant_conversions / variant_visitors
            control_sd = (control_rate * (1 - control_rate)) ** 0.5
            variant_sd = (variant_rate * (1 - variant_rate)) ** 0.5

            effect_size = calculate_cohens_d(
                basic_metrics['control_conversion_rate'], 
                basic_metrics['variant_conversion_rate'], 
                control_sd, 
                variant_sd
            )

            # Combine all results in a dictionary to pass to the template
            results = {
                'basic_metrics': basic_metrics,
                'stats_results': stats_results,
                'confidence_intervals': confidence_intervals,
                'mde': mde,
                'required_sample_size': required_sample_size,
                'suggested_test_duration': suggested_test_duration,
                'effect_size': effect_size,
                'test_duration': test_duration,
                'control_visitors': control_visitors,
                'control_conversions': control_conversions,
                'variant_visitors': variant_visitors,
                'variant_conversions': variant_conversions
            }

            # Render a different template to show the results
            return render(request, 'post_test_analysis/result.html', {'results': results})
    else:
        form = PostTestAnalysisForm()

    return render(request, 'post_test_analysis/index.html', {'form': form})

def calculate_basic_metrics(control_users, control_conversions, variant_users, variant_conversions):
    control_conversion_rate = control_conversions / control_users
    variant_conversion_rate = variant_conversions / variant_users
    conversion_rate_lift = ((variant_conversion_rate - control_conversion_rate) / control_conversion_rate) * 100
    return {
        "control_conversion_rate": control_conversion_rate,
        "variant_conversion_rate": variant_conversion_rate,
        "conversion_rate_lift": conversion_rate_lift
    }

def calculate_statistical_significance_and_power(control_users, control_conversions, variant_users, variant_conversions, alpha=0.05, power=0.8):
    control_rate = control_conversions / control_users
    variant_rate = variant_conversions / variant_users
    pooled_rate = (control_conversions + variant_conversions) / (control_users + variant_users)
    standard_error = (pooled_rate * (1 - pooled_rate) * (1 / control_users + 1 / variant_users)) ** 0.5
    z_score = (variant_rate - control_rate) / standard_error
    p_value_one_tail = norm.cdf(-abs(z_score))
    p_value = 2 * p_value_one_tail
    p_value = min(p_value, 1)  
    is_significant = p_value < alpha
    return {
        "z_score": z_score,
        "p_value": p_value,
        "is_significant": is_significant,
        "power": power
    }

def calculate_mde(control_users, control_conversions, alpha=0.05, power=0.8):
    control_rate = control_conversions / control_users
    standard_deviation = (control_rate * (1 - control_rate)) ** 0.5
    z_alpha = norm.ppf(1 - alpha / 2)
    z_power = norm.ppf(power)
    mde = (z_alpha + z_power) * standard_deviation / (control_users ** 0.5)
    return mde

def calculate_confidence_intervals(control_users, control_conversions, variant_users, variant_conversions):
    control_rate = control_conversions / control_users
    variant_rate = variant_conversions / variant_users
    se_control = (control_rate * (1 - control_rate) / control_users) ** 0.5
    se_variant = (variant_rate * (1 - variant_rate) / variant_users) ** 0.5
    confidence_level = 0.95
    z = stats.norm.ppf(1 - (1 - confidence_level) / 2)
    ci_control = (control_rate - z * se_control, control_rate + z * se_control)
    ci_variant = (variant_rate - z * se_variant, variant_rate + z * se_variant)
    return {
        "ci_control": ci_control,
        "ci_variant": ci_variant
    }

def calculate_required_sample_size(baseline_conversion_rate, mde, power=0.8, alpha=0.05):
    standard_deviation = (baseline_conversion_rate * (1 - baseline_conversion_rate)) ** 0.5
    z_alpha = stats.norm.ppf(1 - alpha / 2)
    z_power = stats.norm.ppf(power)
    sample_size = ((z_alpha + z_power) ** 2 * standard_deviation * (1 - standard_deviation)) / (mde ** 2)
    return round(sample_size)

def estimate_test_duration(required_sample_size, daily_visitors):
    if daily_visitors <= 0:
        raise ValueError("Daily visitors must be greater than zero.")
    days_needed = required_sample_size / daily_visitors
    return round(days_needed)

def calculate_cohens_d(control_mean, variant_mean, control_sd, variant_sd):
    pooled_sd = sqrt((control_sd ** 2 + variant_sd ** 2) / 2)
    d = (variant_mean - control_mean) / pooled_sd
    return d

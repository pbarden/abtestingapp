from django import forms

class PostTestAnalysisForm(forms.Form):
    test_duration = forms.IntegerField(label='Test Duration')
    control_visitors = forms.IntegerField(label='Control Visitors')
    control_conversions = forms.IntegerField(label='Control Conversions')
    variant_visitors = forms.IntegerField(label='Variant Visitors')
    variant_conversions = forms.IntegerField(label='Variant Conversions')

from django import forms

class PreTestAnalysisForm(forms.Form):
    weekly_visitors = forms.IntegerField(label='Weekly Visitors')
    weekly_conversions = forms.IntegerField(label='Weekly Conversions')

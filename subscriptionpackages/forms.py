from django import forms

class PaymentForm(forms.Form):
    mobileNumberWidget = forms.TextInput(
        attrs = {
            "id": "billing_number",
            "class":"form-input-text",
            "placeholder":"mobile money number"
        })

    referenceTextWidget = forms.TextInput(
        attrs = {
            "id": "reference",
            "class":"form-input-text",
            "placeholder":"Transaction reference"
        })

    vodafoneTokenWidget = forms.TextInput(
        attrs = {
            "id": "vodafone-token-input",
            "class":"form-input-text",
            "name": "vodafone-token",
            "placeholder":"Transaction reference"
        })

    mobileNumberInput = forms.CharField(widget=mobileNumberWidget, min_length=10)
    referenceInput = forms.CharField(widget=referenceTextWidget)
    vodafoneTokenInput = forms.CharField(widget=vodafoneTokenWidget,min_length=6,required=False)

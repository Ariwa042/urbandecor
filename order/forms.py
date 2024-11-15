from django import forms

class CheckoutForm(forms.Form):
    email = forms.EmailField(label='Email Address', required=True)
    phone_number = forms.CharField(max_length=15, label='Phone Number', required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}), label='Shipping Address', required=True)
    city = forms.CharField(max_length=100, label='City', required=True)
#    shipping_method = forms.ChoiceField(
#        choices=[('standard', 'Standard Shipping'), ('express', 'Express Shipping')],
#        label='Shipping Method',
#        required=True
#    )

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if not phone_number.isdigit():
            raise forms.ValidationError("Phone number must contain only digits.")
        return phone_number

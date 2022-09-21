from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Password',
                'class': 'form-control'
            }
        )
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm Password',
                'class': 'form-control'
            }
        )
    )

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'password']

    def clean(self):
        cleaned_data = super(RegistrationForm,
                             self).clean()  # super class is used to change the way this fields is being saved.
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:  # basically checks if both password matches or not
            raise forms.ValidationError("password does not match!")

    def __init__(self, *arg,
                 **kwargs):  # using a constructor am applying style to each field of the above form (applying class
        # form-control to every field it can also be done in mata class just like on the above class i have created
        # password field and applied a widget for it to apply form control to it )
        super(RegistrationForm, self).__init__(*arg, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter your Phone Number'

        for field in self.fields:  # looping to apply same widget property to all fields
            self.fields[field].widget.attrs['class'] = 'form-control'

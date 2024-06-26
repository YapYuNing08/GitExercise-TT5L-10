from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm
from django.contrib.auth.models import User
from . models import Customer, Product, CustomizationOption, CustomizationChoice, OrderPlaced, Review, Ad

class LoginForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'class':'form-control'}))

class CustomerRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus':'True', 'class':'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='Old Password', widget=forms.PasswordInput(attrs=
    {'autofocus' : 'True', 'autocomplete' : 'current-password', 'class' : 'form-control'}))
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput(attrs=
    {'autocomplete' : 'current-password', 'class' : 'form-control'}))
    new_password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs=
    {'autocomplete' : 'current-password', 'class' : 'form-control'}))

class MyPasswordResetForm(PasswordChangeForm):
    pass

class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'points']

class AdForm(forms.ModelForm):
    class Meta:
        model = Ad
        fields = ['title', 'description', 'image']

class CustomizationForm(forms.Form):
    def __init__(self, *args, **kwargs):
        product = kwargs.pop('product')
        super().__init__(*args, **kwargs)

        for option in product.customization_options.all():
            choices = [(choice.id, f"{choice.name} (+${choice.additional_price})") for choice in option.choices.all()]
            self.fields[option.name] = forms.ChoiceField(choices=choices, label=option.name, initial=option.default_choice)

class OrderPlacedForm(forms.ModelForm):
    class Meta:
        model = OrderPlaced
        fields = ['product', 'quantity', 'method', 'table_number']  # Include method and table_number

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

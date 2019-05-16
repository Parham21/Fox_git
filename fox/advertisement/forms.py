from django import forms
from django.forms import ModelForm

from advertisement.models import Advertisement, Advertiser, Category, Area
from advertisement.validators import phone_validator, string_check
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    title = forms.CharField(label='Advertisement Title', required=False, max_length=80,
                            widget=forms.TextInput(
                                attrs={'class': 'form-control', 'placeholder': 'Enter the advertisement\'s title'}))
    immediate = forms.BooleanField(label='Immediate', required=False)
    minimum_price = forms.IntegerField(label='Minimum Price', required=False,
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control',
                                                  'placeholder': 'Enter minimum advertisement\'s price'}))
    maximum_price = forms.IntegerField(label='Maximum Price', required=False,
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control',
                                                  'placeholder': 'Enter maximum advertisement\'s price'}))
    area = forms.ModelChoiceField(label='Area', required=False, queryset=Area.objects.all())
    has_image = forms.BooleanField(label='Has Image', required=False)

    def clean(self):
        cleaned_data = super().clean()
        minimum_price = cleaned_data.get("minimum_price")
        maximum_price = cleaned_data.get("maximum_price")
        if minimum_price is not None and maximum_price is not None and minimum_price > maximum_price:
            self._errors['minimum_price'] = 'Minimum price should be bigger than maximum price'
        return cleaned_data


class AddAdvertisementForm(ModelForm):
    class Meta:
        model = Advertisement
        exclude = ['advertiser']

    def __init__(self, *args, **kwargs):
        super(AddAdvertisementForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'title'
        self.fields['price'].widget.attrs['placeholder'] = 'price'
        self.fields['phone'].widget.attrs['placeholder'] = 'phone'
        self.fields['description'].widget.attrs['placeholder'] = 'description'
        self.fields['title'].widget.attrs['class'] = 'form-control '
        self.fields['price'].widget.attrs['class'] = 'form-control '
        self.fields['phone'].widget.attrs['class'] = 'form-control '
        self.fields['description'].widget.attrs['class'] = 'form-control '
        self.fields['category'].queryset = Category.objects.exclude(id__in=Category.objects.all().values('parent_id'))

    def clean(self):
        data = self.cleaned_data
        if phone_validator(data['phone'])[0] is False:
            self._errors['phone'] = phone_validator(data['phone'])[1]
        return data

    def save(self, commit=True):
        instance = super(AddAdvertisementForm, self).save(commit=False)
        instance.advertiser = Advertiser.objects.filter(user=self.user)[0]
        if commit:
            instance.save()
        return instance


class AddAdvertiserForm(ModelForm):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Advertiser
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(AddAdvertiserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'first_name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'last_name'
        self.fields['phone'].widget.attrs['placeholder'] = 'phone'
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['sex'].widget.attrs['placeholder'] = 'sex'
        self.fields['age'].widget.attrs['placeholder'] = 'age'
        self.fields['first_name'].widget.attrs['class'] = 'form-control '
        self.fields['last_name'].widget.attrs['class'] = 'form-control '
        self.fields['phone'].widget.attrs['class'] = 'form-control '
        self.fields['email'].widget.attrs['class'] = 'form-control '
        self.fields['sex'].widget.attrs['class'] = 'form-control '
        self.fields['age'].widget.attrs['class'] = 'form-control '

    def clean(self):
        data = self.cleaned_data
        if phone_validator(data['phone'])[0] is False:
            self._errors['phone'] = phone_validator(data['phone'])[1]
        return data

    def save(self, commit=True):
        instance = super(AddAdvertiserForm, self).save(commit=False)
        user_instance = User.objects.create_user(username=self.cleaned_data['username'],
                                                 password=self.cleaned_data['password'])
        user_instance.save()
        instance.user = user_instance
        if commit:
            instance.save()
        return instance


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'username'
        self.fields['username'].widget.attrs['class'] = 'form-control '

        self.fields['password'].widget.attrs['placeholder'] = '*********'
        self.fields['password'].widget.attrs['class'] = 'form-control '

    def clean(self):
        data = self.cleaned_data
        return data


class ResetPassForm(forms.Form):
    email = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(ResetPassForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['placeholder'] = 'email'
        self.fields['email'].widget.attrs['class'] = 'form-control '


class SubmitPassword(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        super(SubmitPassword, self).__init__(*args, **kwargs)
        self.fields['password'].widget.attrs['placeholder'] = 'password'
        self.fields['password'].widget.attrs['class'] = 'form-control '

        self.fields['confirm_password'].widget.attrs['placeholder'] = 'confirm_password'
        self.fields['confirm_password'].widget.attrs['class'] = 'form-control '

    def clean(self):
        cleaned_data = super(SubmitPassword, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            self._errors['password'] = 'passwords does not match.'

        return cleaned_data


class ReportForm(forms.Form):
    description = forms.Textarea()

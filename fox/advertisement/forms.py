from django import forms
from django.forms import ModelForm

from advertisement.models import Advertisement, Advertiser
from advertisement.validators import phone_validator, string_check
from django.contrib.auth.models import User


class SearchForm(forms.Form):
    title = forms.CharField(label='Advertisement Title', max_length=80,
            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter the advertisement\'s title'}))


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
        user_instance = User.objects.create_user(username=self.cleaned_data['username'], password=self.cleaned_data['password'])
        user_instance.save()
        instance.user = user_instance
        if commit:
            instance.save()
        return instance



class LoginForm(ModelForm):
    class Meta:
        model = Advertisement  # replace with User model
        exclude = ['date_joined']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        # self.fields['title'].widget.attrs['placeholder'] = 'title'
        # self.fields['description'].widget.attrs['class'] = 'form-control '

    def clean(self):
        data = self.cleaned_data
        # if phone_validator(data['phone'])[0] is False:
        #     self._errors['phone'] = phone_validator(data['phone'])[1]
        return data

    def save(self, commit=True):
        instance = super(LoginForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class RegisterForm(ModelForm):
    class Meta:
        model = Advertisement  # replace with User model
        exclude = ['date_joined']

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        # self.fields['title'].widget.attrs['placeholder'] = 'title'
        # self.fields['description'].widget.attrs['class'] = 'form-control '

    def clean(self):
        data = self.cleaned_data
        # if phone_validator(data['phone'])[0] is False:
        #     self._errors['phone'] = phone_validator(data['phone'])[1]
        return data

    def save(self, commit=True):
        instance = super(RegisterForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance


class ResetPassForm(ModelForm):
    class Meta:
        model = Advertisement  # replace with User model
        exclude = ['date_joined']

    def __init__(self, *args, **kwargs):
        super(ResetPassForm, self).__init__(*args, **kwargs)
        # self.fields['title'].widget.attrs['placeholder'] = 'title'
        # self.fields['description'].widget.attrs['class'] = 'form-control '

    def clean(self):
        data = self.cleaned_data
        # if phone_validator(data['phone'])[0] is False:
        #     self._errors['phone'] = phone_validator(data['phone'])[1]
        return data

    def save(self, commit=True):
        instance = super(ResetPassForm, self).save(commit=False)
        if commit:
            instance.save()
        return instance

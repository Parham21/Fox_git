from django import forms
from django.forms import ModelForm

from advertisement.models import Advertisement, Advertiser
from advertisement.validators import phone_validator, string_check


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

from django import forms


class RegForm(forms.Form):
    username = forms.CharField(label='username', min_length=1, max_length=100)
    password = forms.CharField(label='password', min_length=1, max_length=100,  widget=forms.PasswordInput)
    rep_pass = forms.CharField(label='repeat password', min_length=1, max_length=100,  widget=forms.PasswordInput)
    email = forms.EmailField()


class SearchForm(forms.Form):
    search = forms.CharField(label='Search', min_length=1, max_length=100)


class LogForm(forms.Form):
    username = forms.CharField(label='username', min_length=1, max_length=100)
    password = forms.CharField(label='password', min_length=1, max_length=100,  widget=forms.PasswordInput)


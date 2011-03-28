# imports # {{{
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login

from fhurl import RequestForm, try_del
# }}}

# LoginForm # {{{
class LoginForm(RequestForm):
    username = forms.CharField(label=_("Username"), max_length=30)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    def clean_password(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError(_("Please enter a correct username and password. Note that both fields are case-sensitive."))

        self.user_cache = user

        return password

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache

    def save(self):
        login(self.request, self.user_cache)
        return "/"

    def get_json(self, saved):
        d = try_del(
            self.user.__dict__, "backend", "password", "_profile_cache",
            "_state", "email", "last_login", "date_joined", "is_staff"
        )
        return d
# }}}


# imports # {{{
from django import forms
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.models import get_current_site

from fhurl import RequestForm, try_del
import zums, hashlib
from zums.signals import UserSignedIn, UserRegistered
#from zums.models import RegistrationProfile
# }}}

# EmailOptionalRegistrationForm # {{{
class EmailOptionalRegistrationForm(RequestForm):
    username = forms.CharField(label=_("Username"), max_length=30)
    email = forms.EmailField(label=_("Email (optional)"), required=False)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)
    password2 = forms.CharField(
        label=_("Password (again)"), widget=forms.PasswordInput
    )

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError(_("Passwords don't match"))
        return password2

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(_("Username already taken."))
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(_("Email already used."))
        return email

    def get_json(self, saved):
        d = try_del(
            self.user.__dict__, "backend", "password", "_profile_cache",
            "_state", "last_login", "date_joined", "is_staff"
        )
        return d

    def save(self):
        d = self.cleaned_data.get
        email = d("email")
        if not email:
            email = "%s@email.not.set" % d("username")
        self.user = User.objects.create_user(
            username=d("username"), password=d("password"), email=email
        )
        UserRegistered.send(
            sender=zums, user=self.user,
        )
        login(
            self.request,
            authenticate(username=d("username"), password=d("password"))
        )
        return "/"
# }}}

class EmailOnlyRegistrationForm(RequestForm):
    name = forms.CharField(
        label=_("Name (optional)"), max_length=100, required=False
    )
    email = forms.EmailField(label=_("Email"))
    password = forms.CharField(
        label=_("Password"), max_length=50, widget=forms.PasswordInput
    )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            raise forms.ValidationError(_("Email already used."))
        return email

    def save(self):
        d = self.cleaned_data.get
        email = d("email")
        self.user = User.objects.create_user(
            username=hashlib.md5(email).hexdigest(), password=d("password"), email=email
        )
        UserRegistered.send(
            sender=zums, user=self.user,
        )
        login(
            self.request,
            authenticate(username=self.user.username, password=d("password"))
        )
        return "/"
    
    
    
# RegistrationForm # {{{
class RegistrationForm(EmailOptionalRegistrationForm):
    email = forms.EmailField(label=_("Email"))

    def save(self):
        d = self.cleaned_data.get
        self.user = RegistrationProfile.objects.create_inactive_user(
            d("username"), d("password"), d("email"),
            get_current_site(self.request)
        ).user
        UserRegistered.send(
            sender=zums, user=self.user,
        )
        return "/"
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
            try:
                username = User.objects.get(email=username).username
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                raise forms.ValidationError(_("Username or password incorrect."))
            else:
                user = authenticate(username=username, password=password)
                if not user:
                    raise forms.ValidationError(_("Username or password incorrect."))

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
        UserSignedIn.send(
            sender=zums, user=self.user_cache,
            sessionid=self.request.session.session_key
        )
        return "/"

    def get_json(self, saved):
        d = try_del(
            self.user_cache.__dict__, "backend", "password", "_profile_cache",
            "_state", "last_login", "date_joined", "is_staff"
        )
        return d
# }}}


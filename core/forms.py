from allauth.account.forms import *

class CustomLoginForm(LoginForm):
    password = PasswordField(label="password")
    remember = forms.BooleanField(label="Remember Me",required=False)
    #add css class to form
    password.widget.attrs.update({"class":"form-input-password"})
    remember.widget.attrs.update({"class":"checkbox_remember_me"})

    error_messages = {
        'account_inactive':"This account is currently inactive.",

        'email_password_mismatch':"The e-mail address and/or password you specified are not correct.",

        'username_password_mismatch':"The username and/or password you specified are not correct."}

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(LoginForm, self).__init__(*args, **kwargs)

        login_widget = forms.TextInput(
            attrs={
                "class": "form-input-text",
                'placeholder':"Username or e-mail",
                'autofocus': 'autofocus'
                })

        login_field = forms.CharField(label="Login",widget=login_widget)

        self.fields["login"] = login_field
        set_form_field_order(self, [ "login", "password","remember",])

class CustomSignupForm(SignupForm):
    username_widget = forms.TextInput(
        attrs={
            "class": "form-input-text",
            'placeholder':'Username',
            'autofocus': 'autofocus'
            })

    email_widget = forms.TextInput(
        attrs={
            'type': 'email',
            "class": "form-input-text",
            'placeholder':'E-mail address',
            })

    username = forms.CharField(label="Username",min_length=app_settings.USERNAME_MIN_LENGTH,widget=username_widget)
    email = forms.EmailField(label="Email",widget=email_widget)

    def __init__(self, *args, **kwargs):
        super(CustomSignupForm, self).__init__(*args, **kwargs)
        password_field = PasswordField(label="Password")
        password_field.widget.attrs.update({"class":"form-input-password"})
        self.fields['password1'] = password_field
        if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields['password2'] = password_field

    def save(self, request):
        adapter = get_adapter(request)
        user = adapter.new_user(request)
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        # TODO: Move into adapter `save_user` ?
        setup_user_email(request, user, [])
        return user

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Predmeti

User = get_user_model()

class LoginForm(forms.Form):
    email    = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)

class RegisterForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'status') #'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        # user.active = False # send confirmation email
        if commit:
            user.save()
        return user

class SubjectCreate(forms.ModelForm):
    class Meta:
        model = Predmeti
        fields = '__all__'

class SubjectView(forms.ModelForm):
    ime = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    kod = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    program = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    bodovi = forms.IntegerField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    sem_redovni = forms.IntegerField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    sem_izvanredni = forms.IntegerField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )
    izborni = forms.CharField(
        widget=forms.TextInput(attrs={'readonly':'readonly'})
    )

    class Meta:
        model = Predmeti
        fields = '__all__'


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth import authenticate
# from .models import Korisnici

# class RegistrationForm(UserCreationForm):

#     class Meta:
#         model = Korisnici
#         fields = ["email", "status"]

# class KorisnikAuthenticationForm(forms.ModelForm):
#     password = forms.CharField(label="Password", widget=forms.PasswordInput)

#     class Meta: # what to expect in form
#         model = Korisnici
#         fields = ("email", "password")

#     def clean(self): # interceptor 
#         email = self.cleaned_data['email']
#         password = self.cleaned_data['password']
#         print (email)
#         print (password)
#         a = authenticate(email= email, password = password)
#         print (a)
#         if not authenticate(email = email, password = password):
#             raise forms.ValidationError("Invalid login!")
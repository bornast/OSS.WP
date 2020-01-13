from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required
from .models import Korisnici, Predmeti

from .forms import LoginForm, RegisterForm


def login_page(request):
    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        username  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        print ("aaa")
        print (user)
        if user is not None:
            login(request, user)
            try:
                del request.session['guest_email_id']
            except:
                pass
            if is_safe_url(redirect_path, request.get_host()):
                return redirect(redirect_path)
            else:
                return redirect("/")
        else:
            # Return an 'invalid login' error message.
            print("Error")
    return render(request, "mentorski/login.html", context)


# User = get_user_model()
def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
    return render(request, "mentorski/register.html", context)

def logout_page(request):
    logout(request)
    return redirect('/mentorski/login')

@login_required(login_url='/mentorski/login')
def students_page(request):
    context = {}
    loggedUser = request.user
    if loggedUser.role != 'Mentor':
        return redirect('/mentorski/login')

    context['students'] = Korisnici.objects.filter(role='Student')
    return render(request, "mentorski/students.html", context)

@login_required(login_url='/mentorski/login')
def subjects_page(request):
    context = {}
    loggedUser = request.user
    if loggedUser.role != 'Mentor':
        return redirect('/mentorski/login')

    context['subjects'] = Predmeti.objects.all()
    return render(request, "mentorski/subjects.html", context)

# from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.decorators import login_required
# from .forms import RegistrationForm, KorisnikAuthenticationForm
# from .models import Korisnici

# # Create your views here.

# def signin(request):    
#     if request.method == 'GET':
#         userForm = AuthenticationForm()
#         return render(request, 'mentorski/signin.html', {'form': userForm})
#     elif request.method == 'POST':
#         userForm = AuthenticationForm(data=request.POST) # pass request data to authenticate
#         if userForm.is_valid():
#             user = userForm.get_user()
#             login(request, user)
#             return redirect('/mentorski/register')
#         else:
#             return render(request, 'mentorski/signin.html', {'form': userForm})
#     else:
#         return HttpResonseNotAllowed()

# def registration_view(request):
#     context = {}
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             email = form.cleaned_data.get('email')
#             raw_password = form.cleaned_data.get('password')
#             account = authenticate(email="email", password=raw_password)
#             return redirect('/mentorski/signin')
#         else:
#             context['registration_form'] = form
#     else:
#         form = RegistrationForm()
#         context['registration_form'] = form
#     return render(request, 'mentorski/register.html', context)

# def login_view(request):
#     context = {}

#     user = request.user
#     if user.is_authenticated: # if already logged in
#         a = 5
#         #return redirect("/mentorski/signin")
    
#     if request.method == "POST":
#         form = KorisnikAuthenticationForm(request.POST)
#         if form.is_valid():
#             email = request.POST['email']
#             password = request.POST['password']
#             user = authenticate(email = email, password = password)
#             print (user)
#             if (user):
#                 login(request, user)
#                 return redirect("/mentorski/signin")
#     else:
#         form = KorisnikAuthenticationForm()

#     context['login_form'] = form
#     return render(request, 'mentorski/login.html', context)             
    
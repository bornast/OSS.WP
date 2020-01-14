from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required
from .models import Korisnici, Predmeti

from .forms import LoginForm, RegisterForm, SubjectCreate, SubjectView


def login_page(request):
    loggedUser = request.user
    if loggedUser.id:
        return redirect("/")

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
            print("Error")
    return render(request, "mentorski/login.html", context)

def register_page(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        form.save()
        return redirect('/mentorski/login')
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

@login_required(login_url='/mentorski/login')
def create_subject(request):
    uploadForm = SubjectCreate()
    if request.method == 'POST':
        uploadForm = SubjectCreate(request.POST)
        if uploadForm.is_valid():
            uploadForm.save()
            return redirect('/mentorski/subjects')
        else:
            return HttpResponse("""your form is wrong, reload on <a href = "{{ url : '/mentorski/subjects'}}">reload</a>""")
    else:
        return render(request, 'mentorski/subject_create.html', {'subject_form':uploadForm})

@login_required(login_url='/mentorski/login')
def edit_subject(request, subject_id):
    subject_id = int(subject_id)
    try:
        subject = Predmeti.objects.get(id = subject_id)
    except Predmeti.DoesNotExist:
        return redirect('/mentorski/subjects')
    subject_form = SubjectCreate(request.POST or None, instance = subject)
    if subject_form.is_valid():
       subject_form.save()
       return redirect('/mentorski/subjects')
    return render(request, 'mentorski/subject_edit.html', {'subject_form':subject_form})

@login_required(login_url='/mentorski/login')
def delete_subject(request, subject_id):
    subject_id = int(subject_id)
    try:
        subject = Predmeti.objects.get(id = subject_id)
    except Predmeti.DoesNotExist:
        return redirect('/mentorski/subjects')
    subject.delete()
    return redirect('/mentorski/subjects')

@login_required(login_url='/mentorski/login')
def view_subject(request, subject_id):
    subject_id = int(subject_id)
    try:
        subject = Predmeti.objects.get(id = subject_id)
    except Predmeti.DoesNotExist:
        return redirect('/mentorski/subjects')
    subject_form = SubjectView(request.POST or None, instance = subject)
    return render(request, 'mentorski/subject_view.html', {'subject_form':subject_form})

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
    
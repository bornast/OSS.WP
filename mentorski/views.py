from django.contrib.auth import authenticate, login, get_user_model, logout
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.utils.http import is_safe_url
from django.contrib.auth.decorators import login_required
from .models import Korisnici, Predmeti, Upisi
from .forms import LoginForm, RegisterForm, SubjectCreate, SubjectView
from .decorators import mentors_only
from collections import OrderedDict

def login_page(request):
    loggedUser = request.user
    if loggedUser.id:
        return redirect("/")

    form = LoginForm(request.POST or None)
    context = {
        "form": form
    }

    if form.is_valid():
        username  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            context["login_error"] = "Failed to login, wrong username and/or password!"
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

@login_required(login_url='/mentorski/login')
def logout_page(request):
    logout(request)
    return redirect('/mentorski/login')

@mentors_only
def students_page(request):
    context = {}

    context['students'] = Korisnici.objects.filter(role='Student')
    return render(request, "mentorski/students.html", context)

@mentors_only
def delete_student(request, student_id):
    student_id = int(student_id)
    try:
        student = Korisnici.objects.get(id = student_id)
    except Korisnici.DoesNotExist:
        return redirect('/mentorski/students')
    student.delete()
    return redirect('/mentorski/students')

@mentors_only
def subjects_page(request):
    context = {}
    context['subjects'] = Predmeti.objects.all()
    return render(request, "mentorski/subjects.html", context)

@mentors_only
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

@mentors_only
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

@mentors_only
def delete_subject(request, subject_id):
    subject_id = int(subject_id)
    try:
        subject = Predmeti.objects.get(id = subject_id)
    except Predmeti.DoesNotExist:
        return redirect('/mentorski/subjects')
    subject.delete()
    return redirect('/mentorski/subjects')

@mentors_only
def view_subject(request, subject_id):
    subject_id = int(subject_id)
    try:
        subject = Predmeti.objects.get(id = subject_id)
    except Predmeti.DoesNotExist:
        return redirect('/mentorski/subjects')
    subject_form = SubjectView(request.POST or None, instance = subject)
    return render(request, 'mentorski/subject_view.html', {'subject_form':subject_form})

@login_required(login_url='/mentorski/login')
def view_student(request, student_id):

    if request.user.id != student_id and request.user.role != "Mentor":
        return redirect('/')

    context = {}
    student_id = int(student_id)
    student = Korisnici.objects.get(pk=student_id)    

    enrollments = Upisi.objects.filter(student_id=student.id)
    enrolled_subject_ids = []
    passed_enrolled_subject_ids = []
    for enrolled in enrollments:
        enrolled_subject_ids.append(enrolled.predmet_id)
        if (enrolled.status == "polozeno"):
            passed_enrolled_subject_ids.append(enrolled.predmet_id)

    # enrolled subjects by semester
    enrolled_subjects_by_semester = {}
    enrolled_subjects = Predmeti.objects.filter(pk__in=enrolled_subject_ids)
    for enrolled_subject in enrolled_subjects:
        if student.status == "Redovni":
            semester_number = enrolled_subject.sem_redovni
        elif student.status == "Izvanredni":
            semester_number = enrolled_subject.sem_izvanredni            
        if semester_number in enrolled_subjects_by_semester:
            enrolled_subjects_by_semester[semester_number].append(enrolled_subject)
        else:
            enrolled_subjects_by_semester[semester_number] = [enrolled_subject]

    # not enrolled subjects
    not_enrolled_subjects = Predmeti.objects.filter().exclude(pk__in=enrolled_subject_ids)

    context["student"] = student
    context["enrolled_subjects_by_semester"] = OrderedDict(sorted(enrolled_subjects_by_semester.items()))
    context["not_enrolled_subjects"] = not_enrolled_subjects    
    context["passed_enrolled_subject_ids"] = passed_enrolled_subject_ids
    context["student_id"] = student_id
    
    return render(request, 'mentorski/student_view.html', context)

@login_required(login_url='/mentorski/login')
def enroll_subject(request, subject_id, student_id):

    if request.user.id != student_id and request.user.role != "Mentor":
        return redirect('/')

    student = Korisnici.objects.get(pk = student_id)
    subject = Predmeti.objects.get(pk = subject_id)
    Upisi.objects.create(student_id = student.id, predmet_id = subject.id, status = "nepolozeno")    

    return redirect('/mentorski/student_view/'+str(student.id))

@login_required(login_url='/mentorski/login')
def disenroll_subject(request, subject_id, student_id):

    if request.user.id != student_id and request.user.role != "Mentor":
        return redirect('/')

    student = Korisnici.objects.get(pk = student_id)
    subject = Predmeti.objects.get(pk = subject_id)
    enrollment = Upisi.objects.filter(student_id = student.id, predmet_id = subject.id)
    enrollment.delete()

    return redirect('/mentorski/student_view/'+str(student.id))

@login_required(login_url='/mentorski/login')
def mark_subject_as_passed(request, subject_id, student_id):

    if request.user.id != student_id and request.user.role != "Mentor":
        return redirect('/')

    student = Korisnici.objects.get(pk = student_id)
    subject = Predmeti.objects.get(pk = subject_id)
    enrollment = Upisi.objects.filter(student_id = student.id, predmet_id = subject.id)
    enrollment.update(status="polozeno")

    return redirect('/mentorski/student_view/'+str(student.id))

@login_required(login_url='/mentorski/login')
def mark_subject_as_not_passed(request, subject_id, student_id):

    if request.user.id != student_id and request.user.role != "Mentor":
        return redirect('/')

    student = Korisnici.objects.get(pk = student_id)
    subject = Predmeti.objects.get(pk = subject_id)
    enrollment = Upisi.objects.filter(student_id = student.id, predmet_id = subject.id)
    enrollment.update(status="nepolozeno")

    return redirect('/mentorski/student_view/'+str(student.id))

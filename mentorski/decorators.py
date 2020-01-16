from functools import wraps
from django.http import HttpResponseRedirect

def mentors_only(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        profile = request.user        
        if profile.id is not None and profile.role == 'Mentor':
            return function(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/mentorski/login')

    return wrap

def mentor_or_student_himself(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):        
        if request.user is None:            
            return redirect('/mentorski/login')

        student_id = int(request.POST.get("student_id", -1))    
        if request.user.id != student_id and request.user.role != "Mentor":
            return redirect('/')
        else:
            return function(request, *args, **kwargs)         

    return wrap
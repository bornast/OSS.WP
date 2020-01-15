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
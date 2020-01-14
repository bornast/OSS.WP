from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class KorisniciManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password)
        # user_obj.role = role
        user_obj.save(using=self._db)
        return user_obj
    
class Predmeti(models.Model):
    ime = models.CharField(max_length=255)
    kod = models.CharField(max_length=16)
    program = models.TextField()
    bodovi = models.IntegerField(max_length=11)
    sem_redovni = models.IntegerField(max_length=11)
    sem_izvanredni = models.IntegerField(max_length=11)
    
    class Izborni(models.TextChoices):
        DA = 'Ne', _('Ne')
        NE = 'Da', _('Da')
        
    izborni = models.CharField(
        max_length=10,
        choices=Izborni.choices,
        default=Izborni.NE,
    )

    def __str__(self):
        return self.ime

class Korisnici(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True, default="test.test@test.com")

    class Role(models.TextChoices):
        MENTOR = 'Mentor', _('Mentor')
        STUDENT = 'Student', _('Student')
        
    role = models.CharField(
        max_length=7,
        choices=Role.choices,
        default=Role.STUDENT,
    )

    class Status(models.TextChoices):
        NONE = 'None', _('None')
        REDOVNI = 'Redovni', _('Redovni')
        IZVANREDNI = 'Izvanredni', _('Izvanredni')
        
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.REDOVNI,
    )

    upisni = models.ManyToManyField(Predmeti, through='Upisi')

    USERNAME_FIELD = 'email'
    # USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = []

    objects = KorisniciManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email
    
    def get_short_name(self):
        return self.email

class Upisi(models.Model):

    class Meta:
        unique_together = (('student', 'predmet'),)

    student = models.ForeignKey(Korisnici, on_delete=models.CASCADE)
    predmet = models.ForeignKey(Predmeti, on_delete=models.CASCADE)
    status = models.CharField(max_length=64)

    def __str__(self):
        return self.status


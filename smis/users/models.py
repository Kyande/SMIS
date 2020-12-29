from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser
from django.core.mail import send_mail
from django.db import models
from django.utils.translation import gettext_lazy as _

from smis.common.models import AbstractBase

from .managers import UserManager

SYSTEM_USER = 'SYSTEM_USER'
ADMIN = 'ADMIN'
TEACHER = 'TEACHER'
PARENT = 'PARENT'
STUDENT = 'STUDENT'

USER_TYPES = (
    (SYSTEM_USER, 'System user'),
    (ADMIN, 'Admin'),
    (TEACHER, 'Teacher'),
    (PARENT, 'Parent'),
    (STUDENT, 'Student')
)


class User(PermissionsMixin, AbstractBase, AbstractBaseUser):
    email = models.EmailField(_("email field"), unique=True)
    first_name = models.CharField(_('first name'), max_length=50)
    last_name = models.CharField(_('last name'), max_length=50)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    user_type = models.CharField(_('user type'), max_length=50, choices=USER_TYPES)
    is_active = models.BooleanField(_('active'), default=True)
    is_superuser = models.BooleanField(_('superuser'), default=False)
    is_staff= models.BooleanField(_('staff'), default=False)
    # TODO: validate image mimetype, size and dimension
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    class Meta(AbstractBase.Meta, AbstractBaseUser.Meta):
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        '''
        Sends an email to this User.
        '''
        send_mail(subject, message, from_email, [self.email], **kwargs)

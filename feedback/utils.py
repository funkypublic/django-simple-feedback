# -*- coding: utf-8 -*-
from django.core.mail import send_mail
from django.template import loader
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings


# Not used in Django >= 1.2
def email_backend(recipient_list, message, subject='Feedback'):
    subject = settings.EMAIL_SUBJECT_PREFIX + subject
    if type(recipient_list) is not list:
        recipient_list = [recipient_list, ]

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL,
              recipient_list, fail_silently=False)

def import_item(path, error_text):
    """Imports a model by given string. In error case raises ImpoprelyConfigured"""
    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]
    try:
        return getattr(__import__(module, {}, {}, ['']), attr)
    except ImportError, e:
        raise ImproperlyConfigured('Error importing %s %s: "%s"' % (error_text, path, e))

def get_feedback_form(key):
    from feedback.settings import FEEDBACK_FORMS
    if key not in FEEDBACK_FORMS:
        raise ImproperlyConfigured('Form %s not registered in FEEDBACK_FORMS' % key)
    return import_item(FEEDBACK_FORMS[key], 'can not import feedback form')

def mail_managers(subject, message, fail_silently):
    '''Repalcement for standars Django function.
    It uses ``DEFAULT_FROM_EMAIL`` setting instead ``SERVR_FROM_EMAIL``
    '''
    if not settings.ADMINS:
        return
    EmailMessage(settings.EMAIL_SUBJECT_PREFIX + subject, message,
                 settings.DEFAULT_FROM_EMAIL, [a[1] for a in settings.ADMINS],
                 connection=connection).send(fail_silently=fail_silently)

def mail_managers(subject, message, fail_silently=False, connection=None):
    """Sends a message to the managers, as defined by the MANAGERS setting.
    It uses ``DEFAULT_FROM_EMAIL`` setting instead ``SERVR_FROM_EMAIL``
    """
    if not settings.MANAGERS:
        return
    EmailMessage(settings.EMAIL_SUBJECT_PREFIX + subject, message,
                 settings.DEFAULT_FROM_EMAIL, [a[1] for a in settings.MANAGERS],
                 connection=connection).send(fail_silently=fail_silently)

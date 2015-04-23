# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators
from . import AlterFieldFromApp


class Migration(migrations.Migration):
    """
    Migrate the Django Auth User model to have a 255 character limit instead of
    the usual 30.
    """

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        AlterFieldFromApp(
            app_label='auth',
            model_name='user',
            name='username',
            field=models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=255, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required, 255 characters or fewer. Only letters, numbers, and @, ., +, -, or _ characters.', unique=True, verbose_name='username'),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.core.validators


class AlterFieldFromApp(migrations.AlterField):
    """
    Extend the AlterField operation to operate on a different app than the
    current one.

    This "hack" allows us to take advantage of the simplicity of AlterField
    (e.g., for updating state), while being able to run a migration on Django's
    builtin modules (like "auth") from inside our own project.
    """

    def __init__(self, *args, **kwargs):
        self.app_label = kwargs.pop('app_label')
        super(AlterFieldFromApp, self).__init__(*args, **kwargs)

    def state_forwards(self, app_label, state):
        return super(AlterFieldFromApp, self).state_forwards(self.app_label or app_label, state)

    def database_forwards(self, app_label, schema_editor, from_state, to_state):
        return super(AlterFieldFromApp, self).database_forwards(self.app_label or app_label, schema_editor, from_state, to_state)

    def database_backwards(self, app_label, schema_editor, from_state, to_state):
        self.database_forwards(app_label, schema_editor, from_state, to_state)
        return super(AlterFieldFromApp, self).database_backwards(self.app_label or app_label, schema_editor, from_state, to_state)

    def describe(self):
        if self.app_label:
            return "Alter field %s on %s.%s" % (
                self.name, self.app_label, self.model_name)
        else:
            return super(AlterFieldFromApp, self).describe()

    def __eq__(self, other):
        return (super(AlterFieldFromApp, self).__eq__(other) and
                self.app_label == other.app_label)

    def references_model(self, name, app_label=None):
        return (
            super(AlterFieldFromApp, self).references_model(name, app_label) and
            app_label == self.app_label
        )

    def references_field(self, model_name, name, app_label=None):
        return self.references_model(model_name, app_label) and name.lower() == self.name.lower()


class Migration(migrations.Migration):
    """
    Migrate the Django Auth User model to have a 255 character limit instead of
    the usual 30.
    """

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        AlterFieldFromApp(
            app_label='auth',
            model_name='user',
            name='username',
            field=models.CharField(
                help_text='Required, 255 characters or fewer. Only letters, numbers, and @, ., +, -, or _ characters.',
                unique=True,
                max_length=255,
                verbose_name='username',
                validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username.', 'invalid')]
            ),
            preserve_default=True,
        ),
    ]

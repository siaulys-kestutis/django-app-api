from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from core import models
# the recommended convention for converting strings in Python to
# human readable text - so that it gets passed through the translation
# engine
from django.utils.translation import gettext as _


# Register your models here.
class UserAdmin(BaseUserAdmin):
    # ordering will be based on the id of the object
    ordering = ['id']
    # the ordering in which the table would get displayed?
    list_display = ['email', 'name']
    # without these fieldsets, the test: test_admin.test_user_change_page
    # would fail with a message:
    #
    # django.core.exceptions.FieldError: Unknown field(s)
    # (last_name, date_joined, first_name, username)
    # specified for User.
    # Check fields/fieldsets/exclude attributes of class UserAdmin.
    fieldsets = (
        (None, {'fields':  ('email', 'password')}),
        (_('Personal Info'), {'fields': ('name',)}),
        (
            _('Permissions'),
            {'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)})
    )
    # user admin by default takes add_fieldsets which defines the
    # fields that you include on the add page (the same as the
    # create user page)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


# register our created User model as the UserAdmin model here
#
# i.e., specify which models are supposed to show up in the admin panel
# this then allows to add entries (rows) to the db based on the model
admin.site.register(models.User, UserAdmin)


from django.contrib import admin
from .models import User,StudentProfile, ProfessorProfile
# from .forms import CustomUserCreationForm
from .forms import UserCreationForm, UserChangeForm,PastCustomDatePickerWidget
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db import models

# class CustomUserAdmin(BaseUserAdmin):
#     model=User
#     add_form=CustomUserCreationForm

#     fieldsets=(
#         *BaseUserAdmin.fieldsets,
#         (
#             'User role',
#             {
#                 'fields':(
#                     'role',
#                 )
#             }
#         )
#     )

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'name', 'role', 'is_staff',  'is_superuser')
    list_filter = ('is_superuser',)

    fieldsets = (
        (None, {'fields': ('username', 'is_staff', 'is_superuser', 'password')}),
        ('Personal info', {'fields': ('name', 'role')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )
    add_fieldsets = (
        (None, {'fields': ('username', 'is_staff', 'is_superuser', 'password1', 'password2')}),
        ('Personal info', {'fields': ('name', 'role')}),
        ('Groups', {'fields': ('groups',)}),
        ('Permissions', {'fields': ('user_permissions',)}),
    )

    search_fields = ('username', 'name', 'role')
    ordering = ('username','name','role','password')
    filter_horizontal = ()


class StudentProfileModelAdmin(admin.ModelAdmin):
    list_display=('rollno_id','name','semester','admYear')
    formfield_overrides={
        models.DateField:{'widget':PastCustomDatePickerWidget},
    }
    def render_change_form(self, request, context,*args, **kwargs):
        context['adminform'].form.fields["rollno"].queryset=User.objects.filter(role="STUDENT")
        # print(context,type(context))
        return super().render_change_form(request, context,*args, **kwargs)

class  ProfessorProfileModelAdmin(admin.ModelAdmin):
    list_display=('user_id','name','dept')
    def render_change_form(self, request, context,*args, **kwargs):
        context['adminform'].form.fields["user"].queryset=User.objects.filter(role=" PROFESSOR")
        # print(context,type(context))
        return super().render_change_form(request, context,*args, **kwargs)

admin.site.register(User,UserAdmin)
admin.site.register(StudentProfile,StudentProfileModelAdmin)
admin.site.register( ProfessorProfile, ProfessorProfileModelAdmin)
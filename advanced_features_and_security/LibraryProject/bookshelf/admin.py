from django.contrib import admin
from .models import Book
from django.contrib.auth import get_user_model


User = get_user_model()


@admin.register(User)
class CustomUserAdminModel(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'date_of_birth', 'is_active')
    list_filter = ('is_active', 'is_superuser', 'is_staff', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email',
                                      'date_of_birth', 'profile_photo')
                           }
         ),
        ('Permissions', {'fields': ('is_active', 'is_superuser', 'is_staff',
                                    'groups', 'user_permissions')
                         }
         ),
        ('Important Dates', {'fields': ('last_login', 'date_joined')})
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')
    list_filter = ('title', 'author', 'publication_year')
    search_fields = ('title', 'author', 'pulication_year')

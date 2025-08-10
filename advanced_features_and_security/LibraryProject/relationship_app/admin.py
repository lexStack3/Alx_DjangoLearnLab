from django.contrib import admin
from .models import UserProfile, Author, Book, Library, Librarian, User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name',
                    'last_name', 'date_of_birth', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info:', {'fields': ('first_name', 'last_name', 'email',
                                       'date_of_birth', 'profile_photo')
                            }
         ),
        ('Permissions', {'fields': ('is_active', 'is_staff',
                                    'is_superuser', 'groups', 'user_permissions')
                         }
         ),
        ('Important dates:', {'fields': ('last_login', 'date_joined')})
    )

admin.site.register(UserProfile)
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Library)
admin.site.register(Librarian)

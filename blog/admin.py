from django.contrib import admin
from .models import *

# From GPT
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin

# User = get_user_model()
# 1st way
# class CustomUserAdmin(DefaultUserAdmin):
#     # добавим поле только для отображения, не редактирования
#     readonly_fields = ['read_later_posts_display']

#     def read_later_posts_display(self, obj):
#         return ", ".join([str(post) for post in obj.read_later_posts.all()])

#     read_later_posts_display.short_description = "Read Later Posts"
# 2nd way
class CustomUserAdmin(DefaultUserAdmin):
    readonly_fields = ['read_later_posts_display']

    fieldsets = DefaultUserAdmin.fieldsets + (
        ("Read Later", {"fields": ('read_later_posts_display',)}),
    )

    def read_later_posts_display(self, obj):
        return ", ".join([str(post) for post in obj.read_later_posts.all()])
    read_later_posts_display.short_description = "Read Later Posts"
# # admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)
# End from GPT

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageADmin(admin.ModelAdmin):
    pass

# Commented out due to GPT code
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass
from django.contrib import admin
from .models import Blog, Label, Image, User

# Register your models here.


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['title']}),
        ('Information', {'fields': [
            'label', 'summary', 'background_img', 'user', 'content'
        ]})
    ]
    list_per_page = 8
    list_display = ('title', 'create_time', 'label_name')
    list_filter = ['label', 'create_time']
    search_fields = ['title', 'label', 'summary']

    @staticmethod
    def label_name(obj):
        return obj.label.name


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_per_page = 8
    list_display = ('user_name', 'register_time')
    list_filter = ['user_name', 'register_time']
    search_fields = ['user_name']


admin.site.register(Label)
admin.site.register(Image)

admin.site.site_header = 'Blog'

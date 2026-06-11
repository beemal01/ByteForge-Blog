from django.contrib import admin
from .models import content
# Register your models here.

class BlogAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug' : ('title',)}
    list_display = ('title', 'author', 'created_at')


admin.site.register(content, BlogAdmin)



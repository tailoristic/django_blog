from django.contrib import admin
from .models import Post

@admin.register(Post)

class PostAdmin(admin.ModelAdmin):
    list_display = ['id','user_id','user_name','title','desc']

# app/admin.py
from django.contrib import admin
from .models import *

admin.site.register(Post)
admin.site.register(About)
admin.site.register(Ideals)
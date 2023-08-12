from django.contrib import admin
from .models import Vote, Choice
# Register your models here.

admin.site.register(Vote)
admin.site.register(Choice)
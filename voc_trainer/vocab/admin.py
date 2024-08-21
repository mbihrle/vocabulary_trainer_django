from django.contrib import admin

# Register your models here.
from .models import Card, Stack

admin.site.register(Card)
admin.site.register(Stack)

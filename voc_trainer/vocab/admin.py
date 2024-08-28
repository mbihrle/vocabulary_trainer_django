from django.contrib import admin

# Register your models here.
from .models import Card, Stack, Tag, StackTag

admin.site.register(Card)
admin.site.register(Stack)
admin.site.register(Tag)
admin.site.register(StackTag)
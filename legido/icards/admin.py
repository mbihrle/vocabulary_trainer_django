from django.contrib import admin

# Register your models here.
from .models import Card, Stack, Tag, StackTag

class CardAdmin(admin.ModelAdmin):
    list_display = ('front', 'back', 'front_desc', 'back_desc')
    search_fields = ('front', 'back', 'front_desc', 'back_desc')

admin.site.register(Card, CardAdmin)
admin.site.register(Stack)
admin.site.register(Tag)
admin.site.register(StackTag)
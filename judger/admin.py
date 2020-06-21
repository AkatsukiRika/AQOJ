from django.contrib import admin
from . import models

class CodeAdmin(admin.ModelAdmin):
    list_display = ('code_id', 'language', 'problem', 'postman')

# Register your models here.
admin.site.register(models.Problem)
admin.site.register(models.Code, CodeAdmin)
admin.site.register(models.User)
admin.site.register(models.Contest)
admin.site.register(models.Editable)
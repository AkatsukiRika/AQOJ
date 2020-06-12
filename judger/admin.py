from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Problem)
admin.site.register(models.Code)
admin.site.register(models.User)
admin.site.register(models.Contest)
admin.site.register(models.Editable)
from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Categoria)
admin.site.register(models.Produto)
admin.site.register(models.Padaria)
admin.site.register(models.Cesta)
admin.site.register(models.Feedback)
admin.site.register(models.Endereco)
from django.contrib import admin
from django.apps import apps
from formula.models import SlugMixin


class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


formula_config = apps.get_app_config('formula')

for model in formula_config.get_models():
    if model._meta.abstract:
        continue
    if (issubclass(model, SlugMixin)):
        admin.site.register(model, SlugAdmin)
    else:
        admin.site.register(model)
        

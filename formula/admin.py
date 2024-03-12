from django.contrib import admin
from django.apps import apps
from formula.models import SlugMixin

# Admin Interface
class SlugAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}


formula_models = apps.get_app_config('formula').get_models()

for model in formula_models:
    if model._meta.abstract:
        continue
    if (issubclass(model, SlugMixin)):
        admin.site.register(model, SlugAdmin)
    else:
        admin.site.register(model)
        

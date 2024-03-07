from django.contrib import admin
from rango.models import Category, Page
from django.contrib import admin
from rango.models import Category, Page
from rango.models import UserProfile


# Define a custom admin class for the Page model
class PageAdmin(admin.ModelAdmin):
    # This attribute specifies the order in which fields should appear in the list display.
    list_display = ( 'title', 'category', 'url')

# Add in this class to customise the Admin Interface
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}
    
# Update the registration to include this customised interface
admin.site.register(Category, CategoryAdmin)

# Register the Page model with the custom admin interface
admin.site.register(Page, PageAdmin)

admin.site.register(UserProfile)
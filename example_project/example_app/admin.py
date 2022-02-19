from django.contrib import admin
from example_app.models import CustomMetadata, ExampleCustomTable

admin.site.register(CustomMetadata)
admin.site.register(ExampleCustomTable)

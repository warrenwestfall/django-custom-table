from django.contrib import admin
import example_app.models


admin.site.register(example_app.models.ExampleCustomTable)

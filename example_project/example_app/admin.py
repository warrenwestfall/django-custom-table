from django.contrib import admin
from example_app.models import DefaultFormatMetadata, DefaultFormatCustomTable, RestSpaFormatMetadata, RestSpaFormatCustomTable

admin.site.register(DefaultFormatMetadata)
admin.site.register(DefaultFormatCustomTable)
admin.site.register(RestSpaFormatMetadata)
admin.site.register(RestSpaFormatCustomTable)

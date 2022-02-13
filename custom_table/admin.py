from django.contrib import admin
import custom_table.models


admin.site.register(custom_table.models.Metadata)
admin.site.register(custom_table.models.MetadataVersion)

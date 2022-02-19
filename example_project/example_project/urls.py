"""example_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from custom_table.views import RestMetadataView, RestCustomDataView
from example_app.views import CustomTableListView, CustomMetadata


rest_urlpatterns = [
    path('metadata/', RestMetadataView.as_view(metadata_model=CustomMetadata)),
    path('metadata/<str:name>/', RestMetadataView.as_view(metadata_model=CustomMetadata)),
    path('custom_data/<str:name>/', RestCustomDataView.as_view(metadata_model=CustomMetadata, include_metadata=True)),
    path('custom_data/<str:name>/<int:pk>/', RestCustomDataView.as_view(metadata_model=CustomMetadata, include_metadata=True)),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest/', include(rest_urlpatterns)),
    path('example/<str:name>/', CustomTableListView.as_view()),
]

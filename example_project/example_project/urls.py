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
from example_app.models import RestSpaFormatMetadata
from example_app.views import RestMetadataListView, RestMetadataDetailView
from example_app.views import RestCustomTableListView, RestCustomTableDetailView
from example_app.views import RestCustomTableListView, RestCustomTableDetailView, HtmlCustomTableListView, HtmlCustomTableDetailView



rest_urlpatterns = [
    path('metadata/', RestMetadataListView.as_view(metadata_model=RestSpaFormatMetadata)),
    path('metadata/<str:name_or_pk>/', RestMetadataDetailView.as_view(metadata_model=RestSpaFormatMetadata)),
    path('data/<str:name>/', RestCustomTableListView.as_view(metadata_model=RestSpaFormatMetadata, include_metadata=True)),
    path('data/<str:name>/<int:pk>/', RestCustomTableDetailView.as_view(metadata_model=RestSpaFormatMetadata, include_metadata=True)),
]

html_urlpatterns = [
    path('<str:name>/', HtmlCustomTableListView.as_view()),
    path('<str:name>/<int:pk>/', HtmlCustomTableDetailView.as_view()),
]

urlpatterns = [
    path('admin/', admin.site.urls),
    path('rest/', include(rest_urlpatterns)),
    path('html/', include(html_urlpatterns)),
]

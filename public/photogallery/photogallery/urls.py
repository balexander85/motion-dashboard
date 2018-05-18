"""photogallery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from photologue.views import (
    GalleryDetailView,
    PhotoDetailView,
    PhotoListView,
    GalleryListView
)
from .views import index, live, search

urlpatterns = [
    path('', index, name="index"),
    path('live', live, name="live"),
    path('search', search, name="search"),
    path('admin/', admin.site.urls),
    path('gallerylist/', GalleryListView.as_view(), name='gallery-list'),
    path('photologue/', include('photologue.urls', namespace='photologue')),
    path(
        'photolist/', PhotoListView.as_view(paginate_by=54), name='photo-list'
    ),
    path(
        'photologue/photo/<slug>/', PhotoDetailView.as_view(), name='pl-photo'
    ),
    path(
        'photologue/gallery/<slug>/',
        GalleryDetailView.as_view(),
        name='pl-gallery'
    ),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

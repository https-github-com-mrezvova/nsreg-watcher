"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from catalog import views

urlpatterns = [
    path('', views.registrator_list, name='registrator_list'),
    path('list/', views.registrator_list, name='registrator_list'),
    path('api/v1/list/', views.RegistratorList.as_view(), name='registrator_list_api'),
    path('api/v1/<int:pk>/', views.RegistratorDetail.as_view(), name='registrator_details_api'),
    path('api/v1/contact/', views.ContactView.as_view(), name='contact_api'),
    path('partner/<int:id>/', views.registrator_details, name='registrator_details'),
    path('admin/', admin.site.urls),
    path('about-us/', views.about, name='about-us'),
    path('__debug__/', include('debug_toolbar.urls')),
    path('project/', views.project_view, name='project'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
URL configuration for notice project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from app import views
from app.views import NoticeData, NoticeDataDerail

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login),

    path('notice/', views.adds),
    
    path('register/', views.register),

    # path('api/notice/', NoticeData.as_view()),
    
    # path('api/notice/<uuid:userID>/', NoticeDataDerail.as_view()),

    path('api/notice/', NoticeDataDerail.as_view()),
    
    path('api/register/', views.RegisterDataView.as_view()),
    
    path('api/sendemail/', views.sendEmail.as_view()),
    
    path('api/login/', views.LoginDataView.as_view()),

    path('lesson/', include('lessonTable.urls')),
    
    path('chat/', include('AI.urls')),

]
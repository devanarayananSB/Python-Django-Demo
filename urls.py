"""
URL configuration for discoon project.

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
from django.urls import path
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index,name="index"),
    path('register-user/', views.register,name="register"),
    path('register-action/', views.register_action,name="register_action"),
    path('login/', views.login,name="login"),
    path('login_action/', views.login_action,name="login_action"),
    path('admin_home/', views.admin_home,name="admin_home"),
    path('user_list/', views.user_list,name="user_list"),
    path('add_book/', views.add_book,name="add_book"),
    path('book_list/', views.book_list,name="book_list"),
    path('delete_book/<int:id>', views.delete_book,name="delete_book"),
    path('edit_book/<int:id>', views.edit_book,name="edit_book"),
    path('common_logout/', views.common_logout,name="common_logout"),
    path('user_home/', views.user_home,name="user_home"),
    path('profile/', views.profile,name="profile"),
    path('edit_profile/', views.edit_profile,name="edit_profile"),
    path('view_books/', views.view_books,name="view_books"),
    path('more_details/<int:id>', views.more_details,name="more_details"),


    # path('aboutus-user/', views.aboutus,name="aboutus")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

from django.urls import path
from . import views
from user_auth.views import register_view, logout_view, login_view

urlpatterns = [
    path('', views.index, name='index'),
    path('search_results', views.search_results, name='search_results'),
    path('change_show_list/<int:pk>', views.change_show_list, name='change_show_list'),
    path('register', register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('login/', login_view, name='login')
]

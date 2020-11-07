from django.urls import path
from . import views
from user_auth.views import Register, Login
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.Home.as_view(), name='index'),
    path('search', views.SearchResults.as_view(), name='search_results'),
    path('change_show_list/<int:pk>', views.ChangeShowList.as_view(), name='change_show_list'),
    path('register', Register.as_view(), name='register'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('login/', Login.as_view(), name='login'),
    path('watchlist', views.Watchlist.as_view(), name='watchlist')
]

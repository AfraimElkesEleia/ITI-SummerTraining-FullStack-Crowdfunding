from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('<int:id>/profile/',views.edit_profile,name="profile"),
    path('logout/',views.logout_view,name='logout'),
]
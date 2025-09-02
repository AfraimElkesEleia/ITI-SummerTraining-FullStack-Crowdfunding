from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('profile/<int:id>/',views.edit_profile,name="profile"),
    path('logout/',views.logout_view,name='logout'),
    path('delete/<int:id>/',views.delete_account,name="delete")
]
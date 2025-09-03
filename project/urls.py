from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('profile/<int:id>/', views.edit_profile, name="profile"),
    path('logout/', views.logout_view, name='logout'),
    path('delete/<int:id>/', views.delete_account, name="delete"),
    path('create_project/', views.create_project, name="create_project"),
    path('project_details/<int:id>/', views.project_details, name="project_detail"),
    path('api/<int:project_id>/<int:user_id>/rate/', views.rate_project, name='rate_project'),
    path('api/<int:project_id>/tags/', views.get_project_tags, name='get_project_tags'),
    path('api/<int:project_id>/donate/', views.donate_project, name='donate_project'),
    path('api/<int:project_id>/cancel/',views.cancel_project,name="cancel_project"),
    path('api/<int:comment_id>/add_reply/',views.reply,name="submit_reply"),
]

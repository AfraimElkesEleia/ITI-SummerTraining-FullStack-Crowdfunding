from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = "authentication"
urlpatterns = [
    path('',views.register_view,name='register'),
    path('login/',views.login_view,name='login'),
    path('activate/<uidb64>/<token>', views.activate, name='activate')
]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
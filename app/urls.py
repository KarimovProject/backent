from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # ... другие ваши URL-шаблоны
    path('main/files/<str:filename>', views.download_file, name='download_file'),
    path('main/<str:filename>', views.download_file_ariza, name='download_file_ariza'),
    path('', views.submit_form, name='bosh'),
    path('main/', views.index, name='home')
]
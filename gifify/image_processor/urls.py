from django.urls import path
from .views import ui_main_view, error_view, download_view, about_view

urlpatterns = [
    path('', ui_main_view, name='ui-main-view'),
    path('error/', error_view, name='error-view'),
    path('download/', download_view, name='download-view'),
    path('about/', about_view, name='about-view')
]

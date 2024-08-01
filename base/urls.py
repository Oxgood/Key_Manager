from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('request-key/', views.request_new_key, name='request_key'),
    path('search-key/', views.search_key, name='search_key'),
    path('revoke-key/<int:key_id>/', views.revoke_key, name='revoke_key'),
    path('confirm-revoke-key/<int:key_id>/', views.confirm_revoke_key, name='confirm_revoke_key'),
]
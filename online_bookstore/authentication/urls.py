from django.urls import path
from . import views

urlpatterns = [
    path('create_user', views.RegisterUser.as_view(http_method_names=['post']), name='create_user'),
    path('update_user', views.RegisterUser.as_view(http_method_names=['put']), name='update_user'),
    path('login', views.CustomTokenObtainPairView.as_view(), name='token obtain pair'),
    path('refresh_token', views.TokenRefresh.as_view(), name='token_refresh'),
]

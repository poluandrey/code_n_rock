from django.urls import path
from rest_framework_simplejwt import views


urlpatterns = [
    path('token/', views.TokenObtainPairView.as_view()),
    path('token/refres/', views.TokenRefreshView.as_view()),
    path('token/verify/', views.TokenVerifyView.as_view())
]

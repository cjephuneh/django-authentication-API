from django.urls import path

from api.views import UserRegisterView, UserLoginView, UserDetailView, UserLogoutView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("profile/", UserDetailView.as_view(), name="user_detail"),
]

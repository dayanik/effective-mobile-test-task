from auth_app import views
from django.urls import path


urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path(
        "password_change/",
        views.PasswordChangeView.as_view(),
        name="password_change"
    ),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]

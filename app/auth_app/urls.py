from auth_app import views
from django.urls import path
from rest_framework.routers import DefaultRouter


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

router = DefaultRouter()

router.register('role', views.RoleView)
router.register('resourse', views.ResourseView)
router.register('action', views.ActionView)
router.register('permission', views.PermissionView)
router.register('role_permission', views.RolePermissionView)
router.register('user_role', views.UserRoleView)

urlpatterns += router.urls

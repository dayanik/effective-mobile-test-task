from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework import status
from auth_app import serializers, models
from auth_app.services import AuthService
from auth_app.permissions import IsAuthenticated, RBACPermission


class SignUpView(CreateAPIView):
    serializer_class = serializers.SignUpSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = serializers.LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        try:
            tokens = AuthService.login(email, password)
        except ValueError:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return Response(tokens)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        AuthService.logout(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = serializers.ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        old_password = serializer.validated_data['old_password']
        new_password = serializer.validated_data['new_password']

        if not self.request.user.check_password(old_password):
            return Response(
                {'error': 'Старый пароль не актуальный'},
                status=status.HTTP_400_BAD_REQUEST
            )

        self.request.user.set_password(new_password)

        return Response(status=status.HTTP_201_CREATED)


class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def delete(self, request):
        AuthService.delete(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)


class RoleView(ModelViewSet):
    queryset = models.Role.objects.all()
    serializer_class = serializers.RoleSerializer
    permission_classes = [IsAuthenticated, RBACPermission]
    resourse = 'role'


class ResourseView(ModelViewSet):
    queryset = models.Resource.objects.all()
    serializer_class = serializers.ResourseSerializer
    permission_classes = [IsAuthenticated, RBACPermission]
    resourse = 'resourse'


class ActionView(ModelViewSet):
    queryset = models.Action.objects.all()
    serializer_class = serializers.ActionSerializer
    permission_classes = [IsAuthenticated, RBACPermission]
    resourse = 'action'


class PermissionView(ModelViewSet):
    queryset = models.Permission.objects.all()
    serializer_class = serializers.PermissionSerializer
    permission_classes = [IsAuthenticated, RBACPermission]
    resourse = 'permission'


class UserRoleView(ModelViewSet):
    queryset = models.UserRole.objects.all()
    serializer_class = serializers.UserRoleSerializer
    permission_classes = [IsAuthenticated, RBACPermission]
    resourse = 'user_role'


class RolePermissionView(ModelViewSet):
    queryset = models.RolePermission.objects.all()
    serializer_class = serializers.RolePermissionSerializer
    permission_classes = [IsAuthenticated, RBACPermission]
    resourse = 'role_permission'

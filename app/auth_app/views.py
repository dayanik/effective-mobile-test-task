from rest_framework.views import APIView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from rest_framework.response import Response
from rest_framework import status
from auth_app.serializers import (
    UserSerializer,
    SignUpSerializer,
    LoginSerializer,
    ChangePasswordSerializer
)
from auth_app.services import AuthService
from auth_app.permissions import IsAuthenticated


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
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
        serializer = ChangePasswordSerializer(data=request.data)
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
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    def delete(self, request):
        AuthService.delete(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)

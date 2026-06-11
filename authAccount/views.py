from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from rest_framework import generics, status
from rest_framework.response import Response
from .models import MyUser
from tweetBlog.models import content
from .emails import verifyopt_send
from django.shortcuts import redirect,render
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.decorators import login_required


def signup(request):
    return render(request, 'signup.html')

def otp(request):
    return render(request, 'otp.html')

def signin(request):
    return render(request, 'signin.html')

def dashboard(request):
    posts = content.objects.all().order_by('-created_at')
    return render(request, 'dashboard.html', {'posts': posts})




class signupview(generics.CreateAPIView):
    queryset = MyUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        verifyopt_send(user)



class loginview(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        user_data = RegisterSerializer(user)

        return Response({
            'User' : user_data.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }, status=status.HTTP_202_ACCEPTED)


class meview(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'name': user.name,
            'email': user.email,
        }, status=status.HTTP_200_OK)
    

class otpview(generics.GenericAPIView):
    serializer_class = VerifySerializer
    permission_classes =[AllowAny]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'message': 'Account verified successfully'}, status=status.HTTP_200_OK)
    

class logoutview(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({'message': "Logged out successfully"}, status=status.HTTP_200_OK)

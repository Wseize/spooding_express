from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets,status
from dj_rest_auth.registration.views import RegisterView, VerifyEmailView
from dj_rest_auth.views import LoginView,LogoutView,PasswordChangeView,PasswordResetView,PasswordResetConfirmView
from accounts.serializers import CustomUserSerializer, OTPRequestSerializer, OTPVerifySerializer
from delivery.models import Store
from delivery.serializers import StoreSerializer
from .models import CustomUser
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .utils import send_otp_sms
from twilio.rest import Client
from django.conf import settings
from rest_framework.views import APIView


# Create your views here.

class CustomRegisterView(RegisterView):
    pass


class CustomVerifyEmailView(VerifyEmailView):
    pass


class CustomLoginView(LoginView):
    pass
   


class CustomLogoutView(LogoutView):
    pass


class CustomPasswordChangeView(PasswordChangeView):
    pass


class CustomPasswordResetView(PasswordResetView):
    pass

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    pass


class UserProfileView(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


    @action(detail=True, methods=['post'])
    def add_favorite_store(self, request, pk=None):
        user = self.get_object()
        store_id = request.data.get('store_id')

        if store_id:
            store = get_object_or_404(Store, pk=store_id)
            user.favorite_stores.add(store)
            user.save()
            return Response({'detail': 'Store added to favorites'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Store ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        

    
    @action(detail=True, methods=['post'])
    def remove_favorite_store(self, request, pk=None):
        user = self.get_object()
        store_id = request.data.get('store_id')

        if store_id:
            store = get_object_or_404(Store, pk=store_id)
            user.favorite_stores.remove(store)
            user.save()
            return Response({'detail': 'Store removed from favorites'}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Store ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        

    @action(detail=True, methods=['get'])
    def favorite_stores(self, request, pk=None):
        user = self.get_object()
        favorite_stores = user.favorite_stores.all()
        serializer = StoreSerializer(favorite_stores, many=True, context={'request': request})  
        return Response(serializer.data, status=status.HTTP_200_OK)    



class RequestOTP(APIView):
    def post(self, request):
        serializer = OTPRequestSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            send_otp_sms(phone_number)
            return Response({'detail': 'OTP sent via SMS successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VerifyOTP(APIView):
    def post(self, request):
        serializer = OTPVerifySerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            verification_check = client.verify \
                .v2 \
                .services(settings.TWILIO_VERIFY_SERVICE_SID) \
                .verification_checks \
                .create(to=phone_number, code=code)
            
            if verification_check.status == "approved":
                return Response({'detail': 'OTP verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'detail': 'Invalid or expired OTP'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
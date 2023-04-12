import datetime
import random

from django.conf import settings
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from demo.utils import send_otp
from .models import UserModel, UserProfile , ResidentialAddress
from .serializers import UserSerializer, UserAccountSerializer , ResidentialAddressSerializer





class UserViewSet(viewsets.ModelViewSet):
    """
    UserModel View.
    """

    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    @action(detail=True, methods=["PATCH"])
    def verify_otp(self, request, pk=None):
        instance = self.get_object()
        if (
            not instance.is_active
            and instance.otp == request.data.get("otp")
            and instance.otp_expiry
            and timezone.now() < instance.otp_expiry
        ):
            instance.is_active = True
            instance.otp_expiry = None
            instance.max_otp_try = settings.MAX_OTP_TRY
            instance.otp_max_out = None
            instance.save()
            return Response(
                "Successfully verified the user.", status=status.HTTP_200_OK
            )

        return Response(
            "User active or Please enter the correct OTP.",
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(detail=True, methods=["PATCH"])
    def regenerate_otp(self, request, pk=None):
        """
        Regenerate OTP for the given user and send it to the user.
        """
        instance = self.get_object()
        if int(instance.max_otp_try) == 0 and timezone.now() < instance.otp_max_out:
            return Response(
                "Max OTP try reached, try after an hour",
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp = random.randint(1000, 9999)
        otp_expiry = timezone.now() + datetime.timedelta(minutes=10)
        max_otp_try = int(instance.max_otp_try) - 1

        instance.otp = otp
        instance.otp_expiry = otp_expiry
        instance.max_otp_try = max_otp_try
        if max_otp_try == 0:
            # Set cool down time
            otp_max_out = timezone.now() + datetime.timedelta(hours=1)
            instance.otp_max_out = otp_max_out
        elif max_otp_try == -1:
            instance.max_otp_try = settings.MAX_OTP_TRY
        else:
            instance.otp_max_out = None
            instance.max_otp_try = max_otp_try
        instance.save()
        send_otp(instance.phone_number, otp)
        #after successfull otp generation retrun otp with message you can use this otp for verification
        return Response( {"otp":otp,"message":"you can use this otp for verification"}, status=status.HTTP_200_OK)

        #login with phone number
    # @action(detail=True, methods=["POST"])
    # def login(self, request, pk=None):
    #     instance = self.get_object()
    #     if instance.is_active and instance.phone_number == request.data.get("phone_number"):
    #         return Response(
    #             "Successfully logged in.",
    #             status=status.HTTP_200_OK,
    #         )
        

    #     return Response(
    #         "User not active or Please enter the correct phone number.",
    #         status=status.HTTP_400_BAD_REQUEST,
    #     )
    @action(detail=False, methods=["POST"])
    def login(self, request):
        """
        Login with phone number and password.
        """
       
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        


        if phone_number and password:
            try:
                user = UserModel.objects.get(phone_number=phone_number)
                if user.is_active:
                    if user.check_password(password):
                        return Response(
                        "Successfully logged in.", status=status.HTTP_200_OK
                        )
                    else:
                        return Response(
                        "Wrong password", status=status.HTTP_400_BAD_REQUEST
                        )
            except UserModel.DoesNotExist:
                return Response(
                    "Invalid credentials.", status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                "Please provide phone number and password.",
                status=status.HTTP_400_BAD_REQUEST,
            )
              



# all information about the user

class UserAccountViewSet(viewsets.ModelViewSet):
    #after login with phone user can see all imformation about the user and update user in formation 
    # like full name, email, password

    queryset = UserProfile.objects.all()
    serializer_class = UserAccountSerializer

    
    
class ResidentialAddressViewSet(viewsets.ModelViewSet):
    queryset = ResidentialAddress.objects.all()
    serializer_class = ResidentialAddressSerializer



    



from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    Group,
    PermissionsMixin,
)
from django.core.validators import RegexValidator, validate_email
from django.db import models


phone_regex = RegexValidator(
    regex=r"^\d{10}", message="Phone number must be 10 digits only."
)


class UserManager(BaseUserManager):
    """
    User Manager.
    To create superuser.
    """

    def create_user(self, phone_number, password=None):
        if not phone_number:
            raise ValueError("Users must have a phone_number")
        user = self.model(phone_number=phone_number)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    

    def create_superuser(self, phone_number, password):
        user = self.create_user(
            phone_number=phone_number, password=password
        )
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserModel(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model.
    """

    phone_number = models.CharField(
        unique=True, max_length=10, null=False, blank=False, validators=[phone_regex]
    )
    email = models.EmailField(
        max_length=50,
        blank=True,
        null=True,
        validators=[validate_email],
    )
    password = models.CharField(max_length=50, blank=True, null=True, default="password")
    
    otp = models.CharField(max_length=6)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(blank = True , null = True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_registered_at = models.DateTimeField(auto_now_add=True)
    


    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["email , password"]

    objects = UserManager()

    def __str__(self):
        return self.phone_number
    #check password to login 
    def check_password(self, password):
        return self.password == password
    


class UserProfile(models.Model):
    """
    User profile model.

    Every user should have only one profile.
    """
    gender_choices = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other')
    ]

    user = models.OneToOneField(
        UserModel,
        related_name="profile",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    full_name = models.CharField(max_length=50, blank=True, null=True , default = "full name")
    email = models.EmailField( max_length=50, blank=True, null=True , default = "abc@gmail.com")
    occupation = models.CharField(max_length=50, blank=True, null=True , default = None)
    experience = models.CharField(max_length=50, blank=True, null=True, default = None)
    date_of_birth = models.DateField(blank=True, null=True, default = None)
    gender = models.CharField(max_length=6, choices=gender_choices, blank=True, null=True, default = None)
    profile_pic = models.ImageField(
            upload_to="profile_pics", blank=True, null=True , default = None
        )
        
    
    def __str__(self):
            return self.user.phone_number
    
    def get_full_name(self):
            return self.full_name
    
    def get_email(self):
            return self.email
    
    def get_profile_pic(self):
            return self.profile_pic
    
    def get_user_registered_at(self):
            return self.user_registered_at
    
    def get_user(self):
            return self.user
    
    def get_user_phone_number(self):
            return self.user.phone_number
    
    def get_user_otp(self):
            return self.user.otp
    
    def get_user_max_otp_try(self):
            return self.user.max_otp_try
    
    def get_user_otp_max_out(self):
            return self.user.otp_max_out
    
    def get_user_is_active(self):
            return self.user.is_active
    
    def get_user_is_staff(self):
            return self.user.is_staff
    
    def get_user_is_superuser(self):
            return self.user.is_superuser
    
    def get_user_is_verified(self):
            return self.user.is_verified
    

class ResidentialAddress(models.Model):
    """
    User residential address model.
    """

    user = models.OneToOneField(
        UserProfile, on_delete=models.CASCADE, related_name="residential_address" , primary_key=True
    )
    address = models.TextField(max_length=500, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.CharField(max_length=6, blank=True, null=True)

    
    def __str__(self):
        return self.user.phone_number
    
    def get_user(self):
            return self.user
    
    def get_user_phone_number(self):
            return self.user.phone_number




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
    otp = models.CharField(max_length=6)
    otp_expiry = models.DateTimeField(blank=True, null=True)
    max_otp_try = models.CharField(max_length=2, default=settings.MAX_OTP_TRY)
    otp_max_out = models.DateTimeField(blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    user_registered_at = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = "phone_number"

    objects = UserManager()

    def __str__(self):
        return self.phone_number


class UserProfile(models.Model):
    """
    User profile model.

    Every user should have only one profile.
    """

    user = models.OneToOneField(
        UserModel,
        related_name="profile",
        on_delete=models.CASCADE,
        primary_key=True,
    )
    full_name = models.CharField(max_length=50, null=False, blank=False)
    date_of_birth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=1, null=True, blank=True)
    address = models.TextField(null=False, blank=False)
    terms_and_conditions = models.BooleanField(default=False)



class UploadImage(models.Model):
    """
    Upload Image model.

    Every user can upload multiple images.
    """

    user = models.ForeignKey(
        UserModel,
        related_name="images",
        on_delete=models.CASCADE,
    )
    image = models.ImageField(upload_to="images", null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)


class UploadVideo(models.Model):
    """
    Upload Video model.

    Every user can upload multiple videos.
    """

    user = models.ForeignKey(
        UserModel,
        related_name="videos",
        on_delete=models.CASCADE,
    )
    video = models.FileField(upload_to="videos", null=False, blank=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
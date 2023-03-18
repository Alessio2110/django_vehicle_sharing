# from django import forms
# from registration.forms import RegistrationForm
# from .models import CustomUser

# class CustomUserRegistrationForm(RegistrationForm):


#     def save(self, *args, **kwargs):
#         user = super().save(*args, **kwargs)
#         custom_user = CustomUser.objects.create(user=user)
#         return user
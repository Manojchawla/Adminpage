from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'phone_no']

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance')  # Store the existing user instance
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        existing_user = User.objects.filter(email=email)
        if self.instance:  # If updating, exclude the current user
            existing_user = existing_user.exclude(id=self.instance.id)

        if existing_user.exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_phone_no(self):
        phone_no = self.cleaned_data.get('phone_no')
        if not phone_no.isdigit() or len(phone_no) != 10:
            raise forms.ValidationError("Phone number must be exactly 10 digits.")

        existing_user = User.objects.filter(phone_no=phone_no)
        if self.instance:  # If updating, exclude the current user
            existing_user = existing_user.exclude(id=self.instance.id)

        if existing_user.exists():
            raise forms.ValidationError("This phone number is already registered.")
        return phone_no

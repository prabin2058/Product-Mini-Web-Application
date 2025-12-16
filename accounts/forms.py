from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

ROLE_CHOICES = [
    ('user', 'User'),
    ('admin', 'Admin'),
]

class RegisterForm(UserCreationForm):
    # Role selection field
    role = forms.ChoiceField(
        choices=ROLE_CHOICES,
        required=True,
        widget=forms.Select(attrs={
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        }),
        label="Register as"
    )
    
    # Add first_name and last_name fields
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Enter your first name"
        })
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Enter your last name"
        })
    )
    
    # Enhanced email field
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Enter your email address"
        }),
        help_text="We'll never share your email with anyone else."
    )
    
    # Customize password fields
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Create a password",
            "autocomplete": "new-password",
        }),
        help_text="""
            <ul class="text-sm text-gray-600 mt-1 space-y-1">
                <li>• At least 8 characters</li>
                <li>• Can't be too similar to your other personal information</li>
                <li>• Can't be a commonly used password</li>
                <li>• Can't be entirely numeric</li>
            </ul>
        """,
    )
    
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Confirm your password",
            "autocomplete": "new-password",
        }),
        help_text="Enter the same password as before, for verification.",
    )
    
    # Terms agreement
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            "class": "h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
        }),
        error_messages={'required': 'You must accept the terms and conditions'}
    )
    
    class Meta:
        model = User
        fields = ["role", "first_name", "last_name", "email", "password1", "password2"]
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already registered. Please use a different email or try logging in.")
        return email
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        if not user.username:
            user.username = (user.email or '')[:150]
        
        # Set is_staff based on role selection
        role = self.cleaned_data.get('role')
        if role == 'admin':
            user.is_staff = True
        else:
            user.is_staff = False
        
        if commit:
            user.save()
        return user


class LoginForm(AuthenticationForm):
    # Use email instead of username
    username = forms.CharField(
        label="Email Address",
        widget=forms.EmailInput(attrs={
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Enter your email address",
            "autocomplete": "email"
        })
    )
    
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Enter your password",
            "autocomplete": "current-password"
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            "class": "h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
        }),
        label="Remember me"
    )
    
    def clean(self):
        # Override to allow login with email
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if email and password:
            # Try to get user by email
            try:
                user = User.objects.get(email=email)
                # Authenticate with username (since Django expects username)
                self.user_cache = authenticate(
                    self.request,
                    username=user.username,
                    password=password
                )
                
                if self.user_cache is None:
                    raise ValidationError(
                        "Email and password doesn't match."
                    )
                
            except User.DoesNotExist:
                # If no user with that email, try with username (backward compatibility)
                self.user_cache = authenticate(
                    self.request,
                    username=email,
                    password=password
                )
                
                if self.user_cache is None:
                    raise ValidationError(
                        "Email and password doesn't match."
                    )
            
            if not self.user_cache.is_active:
                raise ValidationError("This account is inactive.")
        
        return self.cleaned_data
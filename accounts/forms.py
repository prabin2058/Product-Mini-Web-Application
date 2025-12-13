from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
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
    
    # Customize username field
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
            "placeholder": "Choose a username"
        }),
        help_text="Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    )
    
    # Customize password fields
    # password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={
    #         "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
    #         "placeholder": "Create a password"
    #     }),
    #     help_text="""
    #         <ul class="text-sm text-gray-600 mt-1 space-y-1">
    #             <li>• At least 8 characters</li>
    #             <li>• Can't be too similar to your other personal information</li>
    #             <li>• Can't be a commonly used password</li>
    #             <li>• Can't be entirely numeric</li>
    #         </ul>
    #     """
    # )
    
    # confirm password = forms.CharField(
    #     widget=forms.PasswordInput(attrs={
    #         "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent",
    #         "placeholder": "Confirm your password"
    #     }),
    #     help_text="Enter the same password as before, for verification."
    # )
    
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
        fields = ["first_name", "last_name", "username", "email", "password1", "password2", "terms_accepted"]
    
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
                        "Please enter a correct email and password. "
                        "Note that both fields may be case-sensitive."
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
                        "Please enter a correct email and password. "
                        "Note that both fields may be case-sensitive."
                    )
            
            if not self.user_cache.is_active:
                raise ValidationError("This account is inactive.")
        
        return self.cleaned_data
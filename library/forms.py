from django import forms # type: ignore
from .models import Book, Borrowed,userProfile
from django.contrib.auth.models import User # type: ignore
from django.core.exceptions import ValidationError # type: ignore

# /////////////////////////////////////////////////////////////////////

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['isbn', 'title', 'author', 'published_year', 'publisher', 'quantity', 'category', 'language','description']
   
# /////////////////////////////////////////////////////////////////////

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class BorrowForm(forms.ModelForm):
    isbn = forms.CharField(
        max_length=13,
        widget=forms.TextInput(attrs={
            'placeholder': 'ISBN Number',
            'required': True
        }),
        label='ISBN Number',
        help_text='Enter the 13-digit ISBN number of the book.'
    )
    borrower_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Name of Borrower',
            'required': True
        }),
        label='Name of Borrower'
    )
    telephone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={
            'placeholder': 'Contact Number',
            'required': True
        }),
        label='Contact Number'
    )
    national_id = forms.CharField(
        max_length=20,
        widget=forms.TextInput(attrs={
            'placeholder': 'National ID',
            'required': True
        }),
        label='National ID',
        help_text='Enter your national identification number.'
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'placeholder': 'Start Date',
            'required': True
        }),
        label='Start Date',
        help_text='Select the start date of the borrowing period.'
    )
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'type': 'date',
            'placeholder': 'Due Date',
            'required': True
        }),
        label='Due Date',
        help_text='Select the due date for returning the book.'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Email Address',
            'required': True
        }),
        label='Email Address',
        help_text='Provide a valid email address for contact.'
    )

    class Meta:
        model = Borrowed
        fields = [
            'isbn', 'borrower_name', 'telephone', 'national_id',
            'start_date', 'due_date', 'email'
        ]

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        due_date = cleaned_data.get("due_date")

        if start_date and due_date and start_date > due_date:
            self.add_error('due_date', _("Due date should be after the start date."))

        return cleaned_data

    def clean_telephone(self):
        telephone = self.cleaned_data.get('telephone')
        if not telephone.isdigit():
            raise forms.ValidationError(_("Telephone number should contain only digits."))
        if len(telephone) < 10 or len(telephone) > 15:
            raise forms.ValidationError(_("Telephone number should be between 10 and 15 digits."))
        return telephone

    def clean_national_id(self):
        national_id = self.cleaned_data.get('national_id')
        
        if not national_id.isdigit():
            raise forms.ValidationError(_("National ID should contain only digits."))
        
        if len(national_id) != 14:
            raise forms.ValidationError(_("National ID must be exactly 14 digits long."))
        
        if len(set(national_id)) == 1:
            raise forms.ValidationError(_("National ID cannot be all the same digit."))
        if national_id.startswith('000'):
            raise forms.ValidationError(_("National ID cannot start with '000'."))
        
        return national_id
    
    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        try:
            book = Book.objects.get(isbn=isbn)
            if book.quantity <= 0:
                raise forms.ValidationError(_("This book is currently not available for borrowing."))
        except Book.DoesNotExist:
            raise forms.ValidationError(_("Book with this ISBN does not exist."))
        return isbn

# /////////////////////////////////////////////////////////////////////
import re
from django.core.exceptions import ValidationError

def validate_password_complexity(password):
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not re.search(r'[0-9]', password):
        raise ValidationError("Password must contain at least one number.")
    if not re.search(r'[@$!%*?&#]', password):
        raise ValidationError("Password must contain at least one special character (@, $, !, %, *, ?, &, #).")

class SignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'First name',
            'required': True
        })
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last name',
            'required': True
        })
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'required': True
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'placeholder': 'Enter a valid Email',
            'required': True
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Enter a complex password',
            'required': True
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'required': True
        })
    )
    phone_number = forms.CharField(
        max_length=11,
        widget=forms.TextInput(attrs={
            'placeholder': 'Ex:01001111111',
            'pattern': '[0-9]{11}',
            'required': True
        })
    )
    street_address = forms.CharField(
        max_length=255,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your street address',
            'required': True
        })
    )
    postal_code = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your postal code',
            'required': True
        })
    )
    city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your city',
            'required': True
        })
    )
    is_admin = forms.BooleanField(
        required=False,
        label='Register as Admin'
    )
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use. Please enter a different email.")
        return email
    
    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken. Please choose another.")
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')

        if password:
            validate_password_complexity(password)

        return cleaned_data


    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        user.is_staff = self.cleaned_data.get('is_admin', False)
        if commit:
            user.save()
        return user

# /////////////////////////////////////////////////////////////////////

class LoginForm(forms.Form):
    userid = forms.CharField(label='User ID')
    password = forms.CharField(widget=forms.PasswordInput)

# /////////////////////////////////////////////////////////////////////



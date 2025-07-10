# views.py
from django.shortcuts import render, redirect,get_object_or_404 # type: ignore
from django.http import HttpResponse # type: ignore
from django.template import loader # type: ignore
from datetime import date
from .models import Borrowed,Book,userProfile
from .forms import BookForm, BorrowForm,SignUpForm, LoginForm
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.contrib.auth.hashers import make_password # type: ignore
from django.http import JsonResponse # type: ignore
from .forms import validate_password_complexity
from django.core.exceptions import ValidationError

# //////////////////////////////////////////////////////////

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            phone_number = form.cleaned_data.get('phone_number')
            street_address = form.cleaned_data.get('street_address')
            postal_code = form.cleaned_data.get('postal_code')
            city = form.cleaned_data.get('city')
            is_admin = form.cleaned_data.get('is_admin')
            userProfile.objects.create(
                user=user,
                phone_number=phone_number,
                street_address=street_address,
                postal_code=postal_code,
                city=city,
                is_admin=is_admin
            )     
            return JsonResponse({'success': True, 'redirect_url': '/login'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors})
    else:
        form = SignUpForm()
    return render(request, 'SignupPage.html', {'form': form})

# //////////////////////////////////////////////////////////

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            userid = form.cleaned_data['userid']
            password = form.cleaned_data['password']
            user = authenticate(request, username=userid, password=password)
            if user is not None:
                auth_login(request, user)
                return JsonResponse({'success': True, 'redirect_url': '/'})
            else:
                return JsonResponse({'success': False, 'error': 'Invalid credentials'})
        else:
            return JsonResponse({'success': False, 'error': 'Form is not valid'})
    else:
        form = LoginForm()
    return render(request, 'LoginPage.html', {'form': form})

# //////////////////////////////////////////////////////////

def logout(request):
    auth_logout(request)
    return redirect('login')

# //////////////////////////////////////////////////////////

def home(request):
    return render(request, 'HomePage.html')

# ///////////////////////////////////////////////////////

def avaliable(request):
    books = Book.objects.all()
    return render(request, 'avaliable.html', {'books': books})

# ///////////////////////////////////////////////////////

def add(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'redirect_url': '/avaliable'})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}) 
    else:
        form = BookForm()
    return render(request, 'AddBooks.html', {'form': form})

# //////////////////////////////////////////////////////////////////////

def borrow(request):
    if request.method == 'POST':
        form = BorrowForm(request.POST)
        if form.is_valid():
            isbn_val = form.cleaned_data['isbn']
            try:
                book = Book.objects.get(isbn=isbn_val)
            except Book.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'This book does not exist.'})
            
            if book.quantity > 0:
                book.quantity -= 1
                book.save()
                
                borrowed = form.save(commit=False)
                borrowed.user = request.user
                borrowed.save()
                
                return JsonResponse({'success': True, 'redirect_url': '/borroweduser'})
            else:
                return JsonResponse({'success': False, 'message': 'This book is not available for borrowing.'})
        
        return JsonResponse({'success': False, 'errors': form.errors})
    
    else:
        form = BorrowForm()
    
    return render(request, 'borrow_book.html', {'form': form})

# ///////////////////////////////////////////////////////////////////////

def borroweduser(request):
    borrowed_books = Borrowed.objects.filter(user=request.user)
    return render(request, 'borrowed_books.html', {'borrowed_books': borrowed_books})

# //////////////////////////////////////////////////////////

def borrowedadmin(request):
    borrowed_books =Borrowed.objects.all()
    return render(request, 'borrowed_books.html', {'borrowed_books': borrowed_books})

# //////////////////////////////////////////////////////////

def password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if new_password != confirm_password:
            return JsonResponse({'success': False, 'errors': {'confirm_password': ['Passwords do not match']}})

        try:
            validate_password_complexity(new_password) 
        except ValidationError as e:
            return JsonResponse({'success': False, 'errors': {'new_password': list(e.messages)}})

        users = User.objects.filter(email=email)
        if users.exists():
            if users.count() == 1:
                user = users.first()
                user.password = make_password(new_password)
                user.save()
                return JsonResponse({'success': True, 'redirect_url': '/login'})
            else:
                return JsonResponse({'success': False, 'errors': {'email': ['Multiple users found with this email. Please contact support.']}})
        else:
            return JsonResponse({'success': False, 'errors': {'email': ['User with this email does not exist']}})
    
    return render(request, 'ForgetPassword.html')

# //////////////////////////////////////////////////////////

def edit(request, book_id):
    book_obj = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book_obj)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': True, 'redirect_url': '/avaliable'})  # Include redirect URL in response
        else:
            return JsonResponse({'success': False, 'errors': form.errors})  # Return JSON response with form errors
    else:
        form = BookForm(instance=book_obj)
    return render(request, 'edit.html', {'form': form})

# //////////////////////////////////////////////////////////

def delete(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        confirm_delete = request.POST.get('confirm_delete', False)
        if confirm_delete == 'true':
            book.delete()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False})
    return render(request, 'detail.html', {'book': book})

# //////////////////////////////////////////////////////////

def detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book,
    }
    return render(request,'detail.html', context)

# //////////////////////////////////////////////////////////

def search(request):
    query = request.GET.get('search-input', '')
    option = request.GET.get('search-option', 'title') 
    if query:
        if option == 'title':
            books = Book.objects.filter(title__icontains=query)
        elif option == 'author':
            books = Book.objects.filter(author__icontains=query)
        elif option == 'category':
            books = Book.objects.filter(category__icontains=query)
        if not books:
            return render(request, 'avaliable.html', {'message': 'The book you are searching for is not available'})
        
        return render(request, 'avaliable.html', {'books': books})
    else:
        return redirect('avaliable')
    
# //////////////////////////////////////////////////////////


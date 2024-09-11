from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book
from .forms import BookForm
from accounts.forms import UserProfileForm, PasswordChangeForm  # Correct import

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # Assign the book to the logged-in user
            book.save()
            messages.success(request, 'Book added successfully!')
            return redirect('account')  # Redirect to the account page
    else:
        form = BookForm()

    return render(request, 'add_book.html', {'form': form})

@login_required
def account(request):
    books = Book.objects.filter(user=request.user)  # Get the books added by the user
    profile_form = UserProfileForm(instance=request.user)
    password_form = PasswordChangeForm(user=request.user)
    return render(request, 'account.html', {'profile_form': profile_form, 'password_form': password_form, 'books': books})

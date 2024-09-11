from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Book, Review
from .forms import BookForm, ReviewForm
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

@login_required
def add_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST, user=request.user)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added successfully!')
            return redirect('account')
    else:
        form = ReviewForm(user=request.user)

    return render(request, 'add_review.html', {'form': form})

@login_required
def remove_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    book.delete()
    messages.success(request, 'Book removed successfully!')
    return redirect('account')

@login_required
def book_details(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    review = Review.objects.filter(book=book).first()
    return render(request, 'bookid.html', {'book': book, 'review': review})

@login_required
def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id, user=request.user)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, 'Book updated successfully!')
            return redirect('book_details', book_id=book.id)
    else:
        form = BookForm(instance=book)
    return render(request, 'update_book.html', {'form': form, 'book': book})


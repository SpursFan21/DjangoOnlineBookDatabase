from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, authenticate, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, UserProfileForm, PasswordChangeForm
from books.models import Book, Review  # Import the Book and Review models
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

# Registration view
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('home')  # Redirect to home or another page
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('account')  # Redirect to the account page after login
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

@login_required
def account(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user)
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        # Handle profile update
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')

        # Handle password change
        if password_form.is_valid():
            old_password = password_form.cleaned_data['old_password']
            new_password1 = password_form.cleaned_data['new_password1']
            if authenticate(username=request.user.username, password=old_password):
                request.user.set_password(new_password1)
                request.user.save()
                auth_login(request, request.user)  # Re-login the user
                messages.success(request, 'Your password has been updated successfully!')
                return redirect('account')
            else:
                messages.error(request, 'Old password is incorrect.')
                return render(request, 'account.html', {'profile_form': profile_form, 'password_form': password_form})

    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = PasswordChangeForm(user=request.user)

    # Fetch the books and reviews associated with the logged-in user
    books = Book.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)

    return render(request, 'account.html', {
        'profile_form': profile_form,
        'password_form': password_form,
        'books': books,  # Pass the books to the template
        'reviews': reviews,  # Pass the reviews to the template
    })

# Logout view
def logout_view(request):
    auth_logout(request)
    return redirect('login')  # Redirect to login page or another page after logout

# JWT authentication view for obtaining tokens
class TokenObtainPairView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# JWT authentication view for refreshing tokens
class TokenRefreshView(APIView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get('refresh')
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)



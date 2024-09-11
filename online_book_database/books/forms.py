from django import forms
from .models import Review, Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'publisher', 'reading_status', 'image']
        
class ReviewForm(forms.ModelForm):
    book = forms.ModelChoiceField(queryset=Book.objects.none())  # Dropdown for books

    class Meta:
        model = Review
        fields = ['book', 'text', 'rating']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')  # Extract the user from kwargs
        super().__init__(*args, **kwargs)
        self.fields['book'].queryset = Book.objects.filter(user=user)  # Filter books for the logged-in user

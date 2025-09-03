from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import User, Book, Trade, BooksInTrade, Message, Report, Rating
from .forms import MyUserRegistrationForm, MyLoginForm
from django.contrib.auth import login, authenticate
from django.shortcuts import redirect

def signup_view(request):
    if request.method == 'POST':
        form = MyUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to home after signup
    else:
        form = MyUserRegistrationForm()  # Create an empty form for GET requests
    return render(request, 'core\signup.html', {'form': form})  # Render the signup form template

def reset_password_view(request):
    # This function will handle password reset logic
    return HttpResponse("Password reset functionality is not implemented yet.")

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password) # checks if username and password are correct
        if user is not None:
            login(request, user) # logs the user in
            return redirect('home')  # Redirect to a home page 
        else:
            return HttpResponse("Invalid credentials")
    else:
        # If the request is GET, render the login form
        form = MyLoginForm()
        return render(request, 'core/login.html', {'form': form})  # Render the
    
    return render(request, 'login.html')  # Render a login form template 

def home_view(request):
    if request.user.is_authenticated != True:
        # If the user is not authenticated, redirect to the login page
        return redirect('login')
    return render(request, 'home.html')  # Render a home page template


def books_view(request):
    # Get all the books from the database
    books = Book.objects.all()
    
    # Get the genre the user picked from the filter (like "Fiction" or "Fantasy")
    genre = request.GET.get('genre')
    
    # Get what the user typed in the search box
    search = request.GET.get('search')

    # If the user picked a genre and it's not "All", only show books from that genre
    if genre and genre != 'All':
        books = books.filter(genre=genre)
    
    # If the user typed something in the search box, only show books with that word in the name
    if search:
        books = books.filter(book_name__icontains=search)

    # Make a list of all the genres so we can show them in the drop-down menu
    genres = [g[0] for g in Book.GENRE_CHOICES]
    
    # Show the page with the books, genres, and what the user picked/typed
    return render(request, 'books.html', {
        'books': books,
        'genres': genres,
        'selected_genre': genre or 'All',
        'search': search or '',
    })

def profile_view(request, id):

        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to login if not authenticated
        
        user = User.objects.get(id=id)  # Get the user by ID from the URL
        books = Book.objects.filter(is_wishlist=False, owner = id)  # Get all books owned by the user
        wishlist_books = Book.objects.filter(is_wishlist=True)  # Get all wishlist books owned by the user
        my_reviews = Rating.objects.filter(rated=user)  # Get all reviews made to the user
        total_rating =0
        for i in range(len(my_reviews)):
            total_rating = total_rating + my_reviews[i].rating
        average_rating = total_rating / len(my_reviews) if my_reviews else 0  # Calculate average rating
        num_trades = Trade.objects.filter(requester=user).count() + Trade.objects.filter(responder=user).count()  
        # Count trades involving the user
        
        return render(request, 'profile.html', {
            'user': user,
            'books': books,
            'wishlist_books': wishlist_books,
            'my_reviews': my_reviews,
            'average_rating': average_rating,
            'num_trades': num_trades,
            id: id,
        })

def upload_book_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated
    
    if request.method == 'POST':
        book_name = request.POST.get('book_name')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        description = request.POST.get('description')
        condition = request.POST.get('condition')
        is_wishlist = request.POST.get('is_wishlist')
        owner = request.user
        
        # Handle image upload
        image = request.FILES.get('image')

        # Create a new book instance
        book = Book(
            owner=owner,  # Set the owner of the book to the currently logged-in user
            book_name=book_name,
            author=author,
            genre=genre,
            description=description,
            condition=condition,
            is_wishlist=is_wishlist,
            image=image
        )
        book.save()  # Save the book to the database
        
        return redirect('books')  # Redirect to the books page after uploading
    
    return render(request, 'upload_book.html')  # Render the upload book form template
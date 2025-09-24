from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import User, Book, Trade, BooksInTrade, Message, Report, Rating
from .forms import MyUserRegistrationForm, MyLoginForm
from django.contrib.auth import login, authenticate, logout
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
    if not request.user.is_authenticated:
        # If the user is not authenticated, redirect to the login page
        return redirect('login')
    return render(request, 'core/home.html')  # Render a home page template


def books_view(request):
    # Get all genres
    # .values_list returns a list of tuples, flat=True makes it into a flat list instqead of list of lists of tuples, .distinct() removes duplicates
    genres = Book.objects.values_list('genre', flat=True).distinct()
    #request: is The current HTTP request object, which contains all data sent by the client (browser).
    #GET: A dictionary-like object on the request that contains all the URL query parameters (e.g., for /books/?genre=Fiction, GET contains {'genre': 'Fiction'})
    #.get('genre', 'All'):Looks for the key 'genre' in the GET parameters. If 'genre' is present (e.g., /books/?genre=Fiction), it returns its value (e.g., 'Fiction'). If 'genre' is not present in the URL, it returns the default value 'All'.
    selected_genre = request.GET.get('genre', 'All')
    search = request.GET.get('search', '')

    # 
    books = Book.objects.exclude(owner_id=request.user.id)
    if selected_genre != 'All':
        books = books.filter(genre=selected_genre)
    if search:
        books = books.filter(book_name__icontains=search)

    return render(request, 'core/books.html', {
        'books': books,
        'genres': genres,
        'selected_genre': selected_genre,
        'search': search,
    })

def profile_view(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated
    
    if request.method == 'GET':
        
        user = User.objects.get(id=user_id)  # Get the user's record using their ID 
        books = Book.objects.filter(is_wishlist=False, owner = user_id)  # Get all books owned by the user
        wishlist_books = Book.objects.filter(is_wishlist=True, owner = user_id)  # Get all wishlist books owned by the user
        my_reviews = Rating.objects.filter(rated_id=user_id)  # Get all reviews made to the user
        total_rating =0
        for i in range(len(my_reviews)):
            total_rating = total_rating + my_reviews[i].rating
        average_rating = total_rating / len(my_reviews) if my_reviews else 0  # Calculate average rating
        num_trades_completed = Trade.objects.filter(requester=user_id, responder_received=True, requester_received=True).count() + Trade.objects.filter(responder=user_id, responder_received=True, requester_received=True).count()  
        
        return render(request, 'core/profile.html', {
            'user': user,
            'books': books,
            'wishlist_books': wishlist_books,
            'my_reviews': my_reviews,
            'average_rating': average_rating if my_reviews else 'No ratings yet',
            'num_trades_completed': num_trades_completed,
        })
        
    return HttpResponse(f"Profile page for user ID: {user_id}")


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

def settings_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated
    
    if request.method == 'POST':
        # Here you would handle the form submission to update user settings
        # For example, updating email, password, etc.
        pass
    
    return render(request, 'core/settings.html')  # Render the settings page template

def signout_view(request):
    logout(request)
    return redirect('login')

def mytrades_view(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated
    
    user = request.user
    trades = Trade.objects.filter(requester=user) | Trade.objects.filter(responder=user)
    trades = trades.order_by('-created_at')  # Order by most recent trades first

    return render(request, 'core/mytrades.html', {
        'trades': trades,
    })

def trade_view(request, trade_id):
    HttpResponse(f"Details for trade ID: {trade_id}")
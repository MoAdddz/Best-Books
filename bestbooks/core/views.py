from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from .models import User, Book, Trade, BooksInTrade, Message, Report, Rating
from .forms import MyUserRegistrationForm, MyLoginForm, BookUploadForm, startTradeForm
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404

# ...existing code...

def profile_view(request, user_id):
    """
    Show a user's profile and that user's books.
    If the logged-in user is viewing their own profile, show upload link.
    """
    if request.method == 'GET':
        profile_user = get_object_or_404(User, id=user_id)  # person whose profile is shown
        owned_books = Book.objects.filter(owner=profile_user, is_wishlist=False).order_by('-id')
        wished_books = Book.objects.filter(owner=profile_user, is_wishlist=True).order_by('-id')
        is_owner = True if request.user.is_authenticated and request.user == profile_user else False
        
        my_reviews = Rating.objects.filter(rated_id=user_id)  # Get all reviews made to the user
        
        total_rating =0
        for i in range(len(my_reviews)):
            total_rating = total_rating + my_reviews[i].rating
        average_rating = total_rating / len(my_reviews) if my_reviews else 0  # Calculate average rating
        
        num_trades_completed = Trade.objects.filter(requester=user_id, responder_status='Completed', requester_status='Completed').count() + Trade.objects.filter(responder=user_id, responder_status='Completed', requester_status='Completed').count()
        
        date_joined = profile_user.date_joined.strftime("%d/%m/%Y")  # Format the date joined
        last_login = profile_user.last_login.strftime("%d/%m/%Y at %H:%M:%S") if profile_user.last_login else "Never"
        
        return render(request, 'core/profile.html', {
            'profile_user': profile_user,
            'owned_books': owned_books,
            'wished_books': wished_books,
            'is_owner': is_owner,
            'my_reviews': my_reviews,
            'average_rating': average_rating if my_reviews else 'No ratings yet',
            'num_trades_completed': num_trades_completed,
            'date_joined': date_joined,
            'last_login': last_login,
        })




@login_required(login_url='login')
def upload_book_view(request):
    """
    Upload a book. Owner is set to request.user.
    After successful upload redirect back to the uploader's profile.
    """
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.owner = request.user
            book.save()
            return redirect('profile', user_id=request.user.id)
    else:
        form = BookUploadForm()
    return render(request, 'core/upload_book.html', {'form': form})

def layout_view(request):
    return render(request, 'core/layout.html')  # Render a layout template

def signup_view(request):
    if request.method == 'POST':
        form = MyUserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the new user
            login(request, user)  # Log the user in
            return redirect('home')  # Redirect to home after signup
    else:
        form = MyUserRegistrationForm()  # Create an empty form for GET requests
    return render(request, 'core/signup.html', {'form': form})  # Render the signup form template

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
            # If authentication fails, re-render the login page with an error message
            form = MyLoginForm()
            return render(request, 'core/login.html', {'form': form, 'error': 'Invalid username or password.'})
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

@login_required
def start_trade_view(request, user_id):
    if request.method != 'POST':
        return redirect('profile', user_id=user_id)
    requester = request.user
    responder = get_object_or_404(User, id=user_id)
    if requester == responder:
        return redirect('profile', user_id=user_id)
    # find existing trade or create new
    trade = (Trade.objects.filter(requester=requester, responder=responder).first()
             or Trade.objects.filter(requester=responder, responder=requester).first())
    if not trade:
        trade = Trade.objects.create(requester=requester, responder=responder)
    # support AJAX: return JSON if XHR, otherwise redirect
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'trade_id': trade.id})
    return redirect('trade', trade_id=trade.id)
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if not authenticated
    
    requester = request.user
    responder = get_object_or_404(User, id=user_id)
    
    # Create a new trade
    trade = Trade.objects.create(requester=requester, responder=responder)
    
    return redirect('trade', trade_id=trade.id)

@login_required(login_url='login')
def trade_view(request, trade_id):
    if request.method == 'GET':
        trade = Trade.objects.get(id=trade_id)
        user_1 = request.user
        user_2 = trade.responder if trade.requester == user_1 else trade.requester
        books_in_trade = BooksInTrade.objects.filter(trade=trade).select_related('book')

    
        return render(request, 'core/trade.html', {
            'user_1': user_1,
            'user_2': user_2,
            'trade': trade,
            'books_in_trade': books_in_trade,
    })
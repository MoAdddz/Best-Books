from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class User(AbstractUser):
    address = models.TextField(blank=True)
    is_banned = models.BooleanField(default=False)
    def __str__(self):
        return self.username # This will return the username when the User object is printed

class Book(models.Model):
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Fantasy', 'Fantasy'),
        ('Mystery', 'Mystery'),
        ('Romance', 'Romance'),
        ('Science Fiction', 'Science Fiction'),
        ('Biography', 'Biography'),
        ('History', 'History'),
        ('Other', 'Other'),
    ]
    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Used Like New', 'Used Like New'),
        ('Good', 'Good'),
        ('Acceptable', 'Acceptable'),
        ('Poor', 'Poor'),
    ]
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books') # related_name allows reverse access to books from User
    book_name = models.CharField(max_length=255)
    author = models.CharField(max_length=100)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)  # drop-down with same value/label
    description = models.TextField(max_length=1000, blank=True, null=True) # Allows for optional description
    image = models.ImageField(upload_to='book_images/', blank=True, null=True)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    is_wishlist = models.BooleanField(default=False)
    # No need to add 'id' or 'book_id' unless you want a custom name

    def __str__(self):
        return self.book_name
    
class Trade(models.Model):
    requester = models.ForeignKey(User, related_name='requested_trades', on_delete=models.CASCADE) #Cascade delete means if the user is deleted, their trades are also deleted
    responder = models.ForeignKey(User, related_name='received_trades', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    requester_accepted = models.BooleanField(default=False)
    responder_accepted = models.BooleanField(default=False)
    requester_paid = models.BooleanField(default=False)
    responder_paid = models.BooleanField(default=False)
    time_both_paid = models.DateTimeField(default=None, null=True, blank=True)
    requester_received = models.BooleanField(default=False)
    responder_received = models.BooleanField(default=False)

    def check_and_set_both_paid(self):
        if self.requester_paid and self.responder_paid and self.time_both_paid is None:
            self.time_both_paid = timezone.now()
            self.save()
    
    def __str__(self):
        return f"Trade between {self.requester.username} and {self.responder.username} on {self.created_at} and both paid at {self.time_both_paid}"
    
class BooksInTrade(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)

class Message(models.Model):
    trade = models.ForeignKey(Trade, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Message from {self.sender.username} in trade {self.trade.id} at {self.timestamp}"
    
class Report(models.Model):
    reporter = models.ForeignKey(User, related_name='reports_made', on_delete=models.CASCADE)
    reported = models.ForeignKey(User, related_name='reports_received', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    details = models.TextField()
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Report by {self.reporter.username} against {self.reported.username} - {self.title}"
    
class Rating(models.Model):
    rater = models.ForeignKey(User, related_name='ratings_given', on_delete=models.CASCADE)
    rated = models.ForeignKey(User, related_name='ratings_received', on_delete=models.CASCADE)
    stars = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rating by {self.rater.username} for {self.rated.username} - {self.stars} stars"
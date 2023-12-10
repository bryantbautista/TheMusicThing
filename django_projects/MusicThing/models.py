from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
# class Artists(models.Model):
#     ArtistID = models.AutoField(primary_key=True)
#     Name = models.CharField(max_length=50)
#     def __str__(self):
#         return self.Name

# class Genres(models.Model):
#     GenreID = models.AutoField(primary_key=True)
#     Name = models.CharField(max_length=50)
#     def __str__(self):
#         return self.Name

# class Albums(models.Model):
#     AlbumID = models.AutoField(primary_key=True)
#     ArtistID = models.ForeignKey(Artists, on_delete=models.CASCADE)
#     GenreID = models.ForeignKey(Genres, on_delete=models.CASCADE)
#     Name = models.CharField(max_length=50)
#     ReleaseDate = models.DateField(auto_now=False, auto_now_add=False)
#     LengthMins = models.IntegerField()
#     Rating = models.DecimalField(max_digits=3, decimal_places=2)
#     def __str__(self):
#         return self.Name

class Ratings(models.Model):
    RatingID = models.AutoField(primary_key=True)
    Username = models.CharField(max_length=30)
    AlbumID = models.CharField(max_length=22)
    Rating = models.IntegerField()
    def __str__(self):
        return self.Username + ": " + str(self.Rating)

class Feedback(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback received on {self.created_at}"
<<<<<<< Updated upstream
=======

class Comment(models.Model):
    CommentID = models.AutoField(primary_key=True)
    AlbumID = models.CharField(max_length=22)
    Username = models.CharField(max_length=30)
    Text = models.TextField()
    Timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Username + ": " + self.Text
    
class UserProfileManager(models.Manager):
    pass

class UserProfile(models.Model):
    #user = models.OneToOneField(User)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default='')
    favorite_artist = models.CharField(max_length=100, default='')
    # image = models.ImageField(upload_to='profile_image' , blank=True)


    def __str__(self):
        return self.user.username
>>>>>>> Stashed changes

from django.db import models

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


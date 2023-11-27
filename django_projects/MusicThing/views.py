from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm
from MusicThing.models import Ratings
import urllib.request
import urllib.parse
import json


# Create your views here.

def getSpotifyToken():
    SPOTIFY_API_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    SPOTIFY_API_CLIENT_ID = '9aae27d322434eebbfdde75b04a301e4'
    SPOTIFY_API_CLIENT_SECRET = '1857c1bed7304fe49712638e2927111a'
    data = urllib.parse.urlencode({
        'grant_type': 'client_credentials', 
        'client_id': SPOTIFY_API_CLIENT_ID, 
        'client_secret': SPOTIFY_API_CLIENT_SECRET})
    data = data.encode('ascii')
    token = None

    with urllib.request.urlopen(SPOTIFY_API_TOKEN_URL, data) as f:
        resp = json.loads(f.read().decode('utf-8'))
        token = resp['access_token'] # {"access_token":"BQBW","token_type":"Bearer","expires_in":3600}
    return token
        
def index(request):
    return render(request, 'index.html')

def logoutView(request):
    logout(request)
    return redirect('/')

def loginView(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST": # When the submit button is pressed, this code runs
        form = LoginForm(request.POST)
        if form.is_valid(): # If the data in the form looks reasonable
            # authenticate() looks in the DB for matching username/password, user becomes null if nothing found
            user = authenticate(username = form.cleaned_data["username"], password = form.cleaned_data["password"])
            if user is not None: # If user isn't null, that means there was a matching username/password
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, "User not found.")
        else:
            messages.error(request, "Invalid input.")
    else:
        form = LoginForm()
    return render(request, "registration/login.html", {"form": form})

def registerView(request):
    if request.user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid(): # Checks that the info is valid and the username is unique
            form.save() # Updates the DB
            return redirect('/login')
    return render(request, "registration/register.html", {"form": form})

def albumView(request, albumID):
    token = getSpotifyToken()
    if token:
        req = urllib.request.Request('https://api.spotify.com/v1/albums/' + str(albumID))
        req.add_header('Authorization', 'Bearer ' + token)
        req.add_header('Accept', 'application/json')
        try:
            album = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        except:
            return HttpResponse("Album not found.")
        artist = album['artists'][0]['name']
        genres = ""
        for genre in album['genres']:
            genres += genre
        releasedate = album['release_date']
        name = album['name']
        lengthseconds = 0
        for track in album['tracks']['items']:
            lengthseconds += track['duration_ms']
        lengthseconds /= 1000
        hours = int(lengthseconds // 3600)
        minutes = int((lengthseconds % 3600) // 60)
        seconds = int(lengthseconds % 60)
        if hours != 0:
            length = "" + str(hours) + " Hours, " + str(minutes) + " Minutes, " + str(seconds) + " Seconds"
        else:
            length = "" + str(minutes) + " Minutes, " + str(seconds) + " Seconds"
        allRatings = Ratings.objects.filter(AlbumID=albumID)
        if len(allRatings) == 0:
            avgRating = "No ratings"
        else:
            avgRating = 0
            for rating in allRatings:
                avgRating += rating.Rating
            avgRating /= len(allRatings)
        return render(request, "albumPage.html", {'albumID':albumID, 'artist':artist, 'genres':genres, 'albumlink': album['external_urls']['spotify'],
                                                  'releasedate':releasedate, 'name':name, 'coverurl':album['images'][0]['url'], 'length':length, 'avgRating':avgRating})
    return HttpResponse("Connection to spotify failed.")

def updateRating(request, albumID):
    if request.user.is_authenticated is False: # If user isn't authenticated, they shouldn't be able to rate an album.
        return redirect('/login')
    
    if request.method == "POST":
        received_data = json.loads(request.body) # When a star is clicked, the rating is sent with JSON

        token = getSpotifyToken()
        if token:
            req = urllib.request.Request('https://api.spotify.com/v1/albums/' + str(albumID))
            req.add_header('Authorization', 'Bearer ' + token)
            req.add_header('Accept', 'application/json')
            try:
                album = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
            except:
                return HttpResponse("Album not found.")
            
            existingRating = Ratings.objects.filter(Username=request.user.username, AlbumID=albumID)
            if len(existingRating) == 0:
                newRating = Ratings(Username=request.user.username, AlbumID=albumID, Rating=received_data['rating']) # Create a new entry and add it to the DB
                newRating.save()
            else:
                existingRating.update(Rating=received_data['rating']) # Update the existing entry in the DB
    return redirect('/album/' + albumID)


def homeView(request):
    # TODO: Move me to external file.

    LIMIT = 10
    SPOTIFY_API_TOKEN_URL = 'https://accounts.spotify.com/api/token'
    SPOTIFY_API_NEW_RELEASES = 'https://api.spotify.com/v1/browse/new-releases?country=US&limit=%s' % LIMIT
    SPOTIFY_API_TOP_ARTISTS = 'https://api.spotify.com/v1/playlists/37i9dQZEVXbMDoHDwVN2tF/tracks?market=US&limit=%s' % LIMIT
    SPOTIFY_API_CLIENT_ID = '9aae27d322434eebbfdde75b04a301e4'
    SPOTIFY_API_CLIENT_SECRET = '1857c1bed7304fe49712638e2927111a'

    import urllib.request
    import urllib.parse
    import json

    data = urllib.parse.urlencode({
        'grant_type': 'client_credentials', 
        'client_id': SPOTIFY_API_CLIENT_ID, 
        'client_secret': SPOTIFY_API_CLIENT_SECRET})
    data = data.encode('ascii')
    token = None

    with urllib.request.urlopen(SPOTIFY_API_TOKEN_URL, data) as f:
        resp = json.loads(f.read().decode('utf-8'))
        token = resp['access_token'] # {"access_token":"BQBW","token_type":"Bearer","expires_in":3600}

    releases = None
    artists = None
    if token:
        req = urllib.request.Request(SPOTIFY_API_NEW_RELEASES)
        req.add_header('Authorization', 'Bearer ' + token)
        req.add_header('Accept', 'application/json')
        releases = urllib.request.urlopen(req).read().decode('utf-8')

        req = urllib.request.Request(SPOTIFY_API_TOP_ARTISTS)
        req.add_header('Authorization', 'Bearer ' + token)
        req.add_header('Accept', 'application/json')
        artists = urllib.request.urlopen(req).read().decode('utf-8')

    return render(request, "homePage.html", {"releases": releases, "artists": artists})

def chartsView(request):
    id_sum = {}
    id_count = {}

    for rating in Ratings.objects.all():
        id_sum[rating.AlbumID] = id_sum.get(rating.AlbumID, 0) + rating.Rating
        id_count[rating.AlbumID] = id_count.get(rating.AlbumID, 0) + 1

    id_avg = {}

    for id, sum in id_sum.items():
        id_avg[id] = round(sum / id_count[id], 2)

    print(id_avg.items())
    # token = getSpotifyToken()
    # if token:
    #     req = urllib.request.Request('https://api.spotify.com/v1/albums/' + str(albumID))
    #     req.add_header('Authorization', 'Bearer ' + token)
    #     req.add_header('Accept', 'application/json')
    #     try:
    #         album = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
    #     except:
    #         return HttpResponse("Album not found.")
    return render(request, "charts.html")
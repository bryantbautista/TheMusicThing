from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm
from MusicThing.models import Albums, Artists, Genres, Ratings
import urllib.request
import urllib.parse
import json


# Create your views here.

def index(request):
    popAlbums = Genres.objects.all()
    return render(request, 'index.html', {"popAlbums":popAlbums})

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
    album = Albums.objects.filter(AlbumID = albumID)
    if len(album) != 1:
        return HttpResponse("Album not found.")
    return render(request, "albumPage.html", {"album":album[0]})

def updateRating(request, albumID):
    if request.user.is_authenticated is False: # If user isn't authenticated, they shouldn't be able to rate an album.
        return redirect('/album/' + albumID)
    
    if request.method == "POST":
        received_data = json.loads(request.body) # When a star is clicked, the rating is sent with JSON

        matchingAlbums = Albums.objects.filter(AlbumID=albumID) # Find any albums that match the albumID in the URL. If none match, nothing should be added to the DB

        if len(matchingAlbums) == 1:
            existingRating = Ratings.objects.filter(Username=request.user.username, AlbumID=matchingAlbums[0]) # If a rating exists already, we should update it instead of adding a new entry

            if len(existingRating) == 0:
                newRating = Ratings(Username=request.user.username, AlbumID=matchingAlbums[0], Rating=received_data['rating']) # Create a new entry and add it to the DB
                newRating.save()
            else:
                Ratings.objects.filter(Username=request.user.username, AlbumID=matchingAlbums[0]).update(Rating=received_data['rating']) # Update the existing entry in the DB

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
        request.session['spotifyrefresh'] = token
        req = urllib.request.Request(SPOTIFY_API_NEW_RELEASES)
        req.add_header('Authorization', 'Bearer ' + token)
        req.add_header('Accept', 'application/json')
        releases = urllib.request.urlopen(req).read().decode('utf-8')

        req = urllib.request.Request(SPOTIFY_API_TOP_ARTISTS)
        req.add_header('Authorization', 'Bearer ' + token)
        req.add_header('Accept', 'application/json')
        artists = urllib.request.urlopen(req).read().decode('utf-8')

    return render(request, "homePage.html", {"releases": releases, "artists": artists})
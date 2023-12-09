from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import LoginForm, RegistrationForm
from MusicThing.models import Ratings, Feedback, Comment
from django.contrib.auth.models import User
import urllib.request
import urllib.parse
import json
import random


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
        genres = ", ".join([genre for genre in album['genres']])
        if len(genres) == 0:
            genres = getGenresOfArtist(album['artists'][0]['id'])
        for i in range(0, len(genres)):
            genres[i] = genres[i].title()
        releasedate = album['release_date']
        name = album['name']
        lengthseconds = sum(track['duration_ms'] for track in album['tracks']['items']) / 1000
        hours, remainder = divmod(lengthseconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        length = "{:02}:{:02}:{:02}".format(int(hours), int(minutes), int(seconds))
        
        allRatings = Ratings.objects.filter(AlbumID=albumID)
        avgRating = round(sum(rating.Rating for rating in allRatings) / len(allRatings), 2) if allRatings else "No ratings"

        comments = Comment.objects.filter(AlbumID=albumID).order_by('-Timestamp')
        
        return render(request, "albumPage.html", {'albumID':albumID, 'artist':artist, 'genres':genres, 'albumlink': album['external_urls']['spotify'],
                                                  'releasedate':releasedate, 'name':name, 'coverurl':album['images'][0]['url'], 'length':length, 'avgRating':avgRating, 'comments':comments})
    return HttpResponse("Connection to spotify failed.")

def postComment(request, albumID):
    if request.method == "POST" and request.user.is_authenticated:
        comment_text = request.POST.get('comment', '')
        if comment_text:
            new_comment = Comment(AlbumID=albumID, Username=request.user.username, Text=comment_text)
            new_comment.save()
    return redirect('/album/' + albumID)

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

def FAQView(request):
    return render(request, "FAQ.html")

def supportView(request):
    return render(request, "support.html")

def feedback_submission(request):
    if request.method == 'POST':
        feedback_content = request.POST.get('feedback')
        
        # Check if the feedback content is empty
        if not feedback_content.strip():
            # Feedback is empty, set an error message
            messages.error(request, 'Feedback box is empty! Please try again')
            return redirect('support')
        
        # Save feedback to database
        feedback = Feedback(content=feedback_content)
        feedback.save()
        
        messages.success(request, 'Thank you for the feedback!')
        
        return redirect('support')

def chartsView(request):
    id_sum = {}
    id_count = {}

    for rating in Ratings.objects.all():
        id_sum[rating.AlbumID] = id_sum.get(rating.AlbumID, 0) + rating.Rating
        id_count[rating.AlbumID] = id_count.get(rating.AlbumID, 0) + 1

    id_avg = {}
    id_avg2 = {}

    for id, sum in id_sum.items():
        id_avg[id] = round(sum / id_count[id], 2)
        id_avg2[id] = round(sum / id_count[id], 2)

    topAlbums = []

    for topAlbum in range(0, 20):
        if len(id_avg) > 0:
            newmax = max(id_avg, key= lambda x: id_avg[x])
            topAlbums.append(newmax)
            id_avg.pop(newmax)


    token = getSpotifyToken()
    if token:
        params = {
            'ids': ','.join(topAlbums)
        }
        req = urllib.request.Request('https://api.spotify.com/v1/albums' + '?' + urllib.parse.urlencode(params))
        req.add_header('Authorization', 'Bearer ' + token)
        req.add_header('Accept', 'application/json')
        try:
            response = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        except:
            return HttpResponse("Error: Album not found.")
        
        albumInfo = []
        for i in range(0, len(response['albums'])):
            albumInfo.append({'rank': i+1, 'img': response['albums'][i]['images'][0]['url'], 
                              'title': response['albums'][i]['name'], 
                              'artist': response['albums'][i]['artists'][0]['name'], 
                              'avgrating': id_avg2[response['albums'][i]['id']], 
                              'totalratings': id_count[response['albums'][i]['id']], 
                              'id': response['albums'][i]['id']})
    return render(request, "charts.html", {'albumInfo': albumInfo})

def randomView(request):
    randomRating = random.choice(Ratings.objects.all())
    return redirect('/album/' + randomRating.AlbumID)

def profileView(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return HttpResponse("User does not exist. <a href='/'>Go home</a>")
    allRatings = Ratings.objects.filter(Username=username)
    allIDs = ''
    for rating in allRatings:
        allIDs += rating.AlbumID + ','
    allIDs = allIDs[:-1]
    
    token = getSpotifyToken()
    if token:
        params = {
            'ids': allIDs
        }
        req = urllib.request.Request('https://api.spotify.com/v1/albums' + '?' + urllib.parse.urlencode(params))
        req.add_header('Authorization', 'Bearer ' + token)
        req.add_header('Accept', 'application/json')
        try:
            response = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        except:
            return HttpResponse("Error: Failed to connect to spotify. <a href='/'>Go Home</a>")
        for album in response['albums']:
            album['userRating'] = allRatings.get(AlbumID=album['id']).Rating
        print(response['albums'][0])
    return render(request, 'profile.html', {'user': user, 'allRatings': response['albums']})

def searchView(request):
    token = getSpotifyToken()
    query = request.GET['q']
    if token:
        params = {
            'q': query,
            'type': 'album'
        }
        req = urllib.request.Request('https://api.spotify.com/v1/search' + '?' + urllib.parse.urlencode(params))
        req.add_header('Authorization', 'Bearer ' + token)
        req.add_header('Accept', 'application/json')
        try:
            response = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        except:
            return HttpResponse("Error")
        for album in response['albums']['items']:
            curRatings = Ratings.objects.filter(AlbumID=album['id'])
            totalRating = 0
            for rating in curRatings:
                totalRating += rating.Rating
            if len(curRatings) == 0:
                album['avgRating'] = "n/a"
            else:
                album['avgRating'] = round(totalRating / len(curRatings), 2)
            album['numRatings'] = len(curRatings)
    return render(request, "search.html", {'albums': response['albums']['items'], 'query':query})

def getGenresOfArtist(artistID):
    token = getSpotifyToken()
    if token:
        req = urllib.request.Request('https://api.spotify.com/v1/artists/' +  artistID)
        req.add_header('Authorization', 'Bearer ' + token)
        req.add_header('Accept', 'application/json')
        try:
            response = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))
        except:
            return []
        return response['genres']
const renderTopSongs = (data) => {
    const container = document.getElementById('artists-cards');
    data.items.sort((a, b) => a.track.popularity > b.track.popularity ? -1 : 1).forEach((item) => {
        console.log(item);
        const card = container.appendChild(document.createElement('div'));
        card.className = 'artist-card';
        const img = card.appendChild(document.createElement('img'));
        img.src = item.track.album.images[0].url;
        img.width = 100;
        img.alt = '';
        // card.appendChild(document.createElement('h4')).textContent =
        //     item.track.name + ' by ' + item.track.artists[0].name;
        card.appendChild(document.createElement('br'));
        const a = card.appendChild(document.createElement('a'));
        a.appendChild(document.createTextNode(item.track.name + ' by ' + item.track.artists[0].name));
        a.title = "uhhh";
        a.href = "/album/" + item.track.album.id;
        card.appendChild(document.createElement('p')).textContent =
            'Release Date: ' + item.track.album.release_date;
        card.appendChild(document.createElement('p')).textContent =
            'Popularity: ' + item.track.popularity;
    });
};

const renderNewReleases = (data) => {
    const container = document.getElementById('releases-cards');
    data.albums.items.sort((a, b) => a.release_date > b.release_date ? -1 : 1).forEach((release) => {
        console.log(release);
        const card = container.appendChild(document.createElement('div'));
        card.className = 'song-card';
        const img = card.appendChild(document.createElement('img'));
        img.src = release.images[0].url;
        img.width = 100;
        img.alt = '';
        // card.appendChild(document.createElement('h4')).textContent =
        //     release.name + ' by ' + release.artists[0].name;
        card.appendChild(document.createElement('br'));
        const a = card.appendChild(document.createElement('a'));
        a.appendChild(document.createTextNode(release.name + ' by ' + release.artists[0].name));
        a.title = "uhhh";
        a.href = "/album/" + release.id;
        card.appendChild(document.createElement('p')).textContent =
            'Release Date: ' + release.release_date;
        card.appendChild(document.createElement('p')).textContent =
            'Total Tracks: ' + release.total_tracks;
    });
};
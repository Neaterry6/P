import requests
from bs4 import BeautifulSoup
import json

def load_cookies(filepath):
    cookies = {}
    with open(filepath, 'r') as f:
        for line in f:
            if line.startswith('#') or not line.strip():
                continue
            parts = line.strip().split('\t')
            # domain, flag, path, secure, expiry, name, value
            if len(parts) >= 7:
                name, value = parts[5], parts[6]
                cookies[name] = value
    return cookies

def get_track_page(track_id, cookies):
    url = f'https://open.spotify.com/track/{track_id}'
    response = requests.get(url, cookies=cookies, headers={'User-Agent': 'Mozilla/5.0'})
    response.raise_for_status()
    return response.text

def parse_track_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    script = soup.find('script', id='__NEXT_DATA__')
    if not script:
        raise Exception("Spotify data script not found")
    data = json.loads(script.string)
    try:
        track_data = data['props']['pageProps']['track']
        name = track_data['name']
        artists = ', '.join([a['name'] for a in track_data['artists']])
        preview_url = track_data['preview_url']
        return {
            'name': name,
            'artists': artists,
            'preview_url': preview_url
        }
    except Exception:
        raise Exception("Failed to parse track info")

def get_lyrics(artist, title):
    url = f'https://api.lyrics.ovh/v1/{artist}/{title}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('lyrics', 'No lyrics found.')
    return 'No lyrics found.'

def main():
    cookies = load_cookies('cookies.txt')
    track_id = input("Enter Spotify track ID (e.g. 7ouMYWpwJ422jRcDASZB7P): ")
    html = get_track_page(track_id, cookies)
    info = parse_track_info(html)
    print(f"\nSong: {info['name']} - {info['artists']}")
    print(f"Preview URL: {info['preview_url']}\n")
    print("Fetching lyrics...\n")
    lyrics = get_lyrics(info['artists'].split(',')[0], info['name'])
    print(lyrics)

if __name__ == '__main__':
    main(

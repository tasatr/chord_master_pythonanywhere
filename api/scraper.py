import requests
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
import re
import json
import pandas as pd
import time
requests.adapters.DEFAULT_RETRIES = 20

def simple_get(url):
    """
    Source: https://realpython.com/python-web-scraping-practical-introduction/
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                with closing(get(url, stream=True)) as resp:
                    if is_good_response(resp):
                        return resp.content
                    return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Source: https://realpython.com/python-web-scraping-practical-introduction/
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    Source: https://realpython.com/python-web-scraping-practical-introduction/
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)

def get_tabs_data(url):
    """
    Creates the bs4 object and extracts a list
    of tab info. Hits info is stored as a separate
    list in the html file so it is returned separately.
    """

    data = simple_get(url)
    data = data.decode("utf-8")

    tab_links = []

    m = re.findall('(https://tabs.ultimate-guitar.com/tab/\S+?)&', data)
    if m:
        tab_links.append(m)

    return(tab_links, [])

def get_chords(url):
    """
    Scrapes and returns the sequences of
    chords as a list as well as the fret number
    to place a capo.
    """

    data = simple_get(url)
    data = data.decode("utf-8")

    # Matching groups (open tag)(chord pitch)(base note {0 or 1})(chord type)(base note {0 or 1})(closing tag)
    pattern = "(\[ch\])([A-G]+)(\/[A-G]*[b#])*([(?m)|(?m\d)|(?b\d)|(?#\d)|(?maj\d)|(?add\d)|(?sus\d)|(?aug)|(?aug\d)|(?dim)|(?dim\d)]*)(\/[A-G]*[b#])*(\[\/ch\])"
    prog = re.compile(pattern)
    result = prog.findall(data)

    cleaned_res = result
    for i in range(len(result)):
        # Grabbing groups (chord pitch)(base note)(chord type)(base note)
        cleaned_res[i] = result[i][1] + result[i][2] + result[i][3] + result[i][4]

    # Grabbing Capo info
    capo = 0
    pattern = "&quot;capo&quot;:(\d)"
    result = re.search(pattern, data)
    if result:
        capo = result.group(1)

    artist = ''
    pattern = "artist_name&quot;:&quot;(.*?)&"
    result = re.search(pattern, data)
    if result:
        artist = result.group(1)

    song = ''
    pattern = "song_name&quot;:&quot;(.*?)&"
    result = re.search(pattern, data)
    if result:
        song = result.group(1)

    return(artist, song, cleaned_res, capo)

def get_genre(url):
    """
    Grabs the artist's categorized genre
    """
    data = get_data(url)
    genre = data['data']['artist']['genre']

    return(genre)


def get_multiple_pages(url):
    cur_tabs, cur_hits = get_tabs_data(url)

    tabs_list = cur_tabs[0]
    hits_list = cur_hits

    return(tabs_list, hits_list)

def scrape_chords_for_song(artist, song):
    string_value = artist.replace(' ', '%20') + '%20' + song.replace(' ', '%20')

    tabs, hits = get_multiple_pages("https://www.ultimate-guitar.com/search.php?search_type=title&value=" + string_value)
    df = pd.DataFrame(columns=['Artist', 'Song', 'Chords', 'Capo'])
    artist, song, chords, capo = get_chords(tabs[0])
    df.loc[0] = [artist, song, chords, capo]
    return df

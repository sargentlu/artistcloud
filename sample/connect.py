"""Spotify API requests
for specifics on the API end points check
https://beta.developer.spotify.com/console/
"""

import requests
from requests.utils import quote
import time
import sys


# Request template
def make_http_request(
    url, method='get',
    headers=None, params=None,
    data=None, auth=None
):

    try:
        request_method = requests.post if method == 'post' else requests.get
        res = request_method(
            url,
            headers=headers, params=params,
            data=data, auth=auth
        )
        responsejson = res.json()
        
        if res.status_code != 200:
            raise Exception(res.text)
    except ValueError:
        return res.text
    except Exception:
        sys.exit('Could not connect')

    return responsejson


# Generate token (through request template)
def request_access_token(client_id, client_secret):
    
    headers = {'Accept': 'application/json'}
    data = [('grant_type', 'client_credentials')]
    res = make_http_request(
        'https://accounts.spotify.com/api/token', method='post',
        headers=headers, data=data,
        auth=(client_id, client_secret)
    )

    try:
        return res['access_token']

    except (KeyError, TypeError):
        sys.exit('Error while requesting an access token')


def search_artist(access_token):
    # Search for an artist to get its uri
    headers = {'Authorization': 'Bearer ' + access_token}
    
    artist_name = input('Search for artist: ')
    artist_formatted = quote(artist_name)
    res = make_http_request(
        'https://api.spotify.com/v1/search?q={artist}&type=artist'.format(
            artist=artist_formatted
        ),
        method='get', headers=headers
    )
    
    indexes = res['artists']['items']

    print()

    for x in range(indexes.__len__()):
        args = {
                'entry':x+1,
                'artist':indexes[x]['name'],
                'followers':indexes[x]['followers']['total'],
                'popularity':indexes[x]['popularity']
            }
       
        print(
            '{entry}. {artist} '
            '({followers} followers, '
            'popularity: {popularity}%)'.format(**args)
        )
    
    print()

    if(indexes.__len__() > 1):
        chosen_index = int(
            input('Choose an index (1 - %s): ' % (indexes.__len__()))
        ) - 1
        print('Chose index %s' %(chosen_index+1))
    
    else:
        chosen_index = 0
    
    return indexes[chosen_index]


# Get up to 20 related artists
def get_related(node, access_token):
    headers = {'Authorization': 'Bearer ' + access_token}
    res = make_http_request(
        'https://api.spotify.com/v1/artists/%s/related-artists' % (node.uri),
        method='get', headers=headers
    )

    try:
        artists = res['artists']

        if artists != None:
            for index in range(artists.__len__()):
                node.related.append(artists[index]['id'])

                return artists

    except (KeyError, TypeError):
        sys.exit('Error while retrieving similar artists')
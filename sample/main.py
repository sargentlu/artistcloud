"""artistcloud
Generate a graph of related artists based on a single artist
based on the Spotify API info
"""

__version__ = '0.0.1'
__author__ = 'Sergio Martinez Lu'

import csv
import time

import structures
import connect
from credentials import my_keys

# Initialize
client_id = my_keys.client['id']
client_secret = my_keys.client['secret']

# Filter artists by follower and popularity range
min_followers = 10
max_followers = 250000
min_popularity = 10

# Create CSV files
with open('../results/nodes.csv', 'w', newline='') as nodefile:
    nodewrite = csv.writer(nodefile)
    nodewrite.writerow(['Id', 'Label', 'Followers', 'Popularity'])

with open('../results/edges.csv', 'w', newline='') as edgefile:
    edgewrite = csv.writer(edgefile)
    edgewrite.writerow(['Source', 'Target', 'Weight'])

# Get current runtime
def current_time(start):
    return time.time() - start

def workflow():
    # Request access token
    access_token = connect.request_access_token(client_id, client_secret)

    # Create graph
    artist_graph = structures.Graph()

    # Add first node
    first_artist = connect.search_artist(access_token)
    artist_graph.set_node(first_artist, None, None)

    max_nodes = int(input('Graph size: '))

    # Start counting time from here
    start_time = time.time()
    print('Current time: %s seconds ' % (current_time(start_time)))
    print('---------------')

    # Add nodes for the desired range
    for x in range(max_nodes):
        if(artist_graph.nodes[x]):
            print(artist_graph.links[x])
            artist_query = connect.get_related(
                artist_graph.nodes[x],
                access_token
            )  
            
            # Get stored node's related artists
            if(artist_query != None):
                for lookup in range(artist_query.__len__()):
                    followers = artist_query[lookup]['followers']['total']
                    popularity = artist_query[lookup]['popularity']

                    # Set every related artist in graph
                    if ((followers > min_followers) &
                    (followers < max_followers) &
                    (popularity > min_popularity)):
                        artist_graph.set_node(
                        artist_query[lookup],
                        artist_graph.nodes[x].id,
                        lookup
                    )  
                
                print('Index: %s' % (x))
                print('Current artists: %s' % (artist_graph.count))
                print('Current time: %s seconds' % (current_time(start_time)))
                print('---------------')

            else:
                print('No related artists for this one!')
    
    return None

# Run workflow only if main.py is not imported
if __name__ == "__main__":
    workflow()
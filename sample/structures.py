"""Graph definition for the artistcloud program
will be more useful when graph search is implemented
"""

import csv


# Graph class
class Graph:
    
    def __init__(self):
        # Store nodes, artist ids and graph size
        self.nodes = []
        self.links = []
        self.count = 0

    # Add new node with artist information to graph
    def set_node(self, response, parent_id, child_id):
        popularity = response['popularity']
        name = response['name']
        uri = response['id']
        
        if (response['followers']['total'] == None):
            followers = 0
        else:
            followers = response['followers']['total']
        
        if (uri in self.links) == False:
            self.nodes.append(
                Node(self.count, uri, name, followers, popularity)
            )
            self.links.append(uri)

            with open('../results/nodes.csv', 'a') as nodefile:
                nodewrite = csv.writer(nodefile)
                nodewrite.writerow([
                    self.count,
                    name.replace(',', '´'),
                    followers,
                    popularity
                ])

            self.count += 1

        if(parent_id != None):
            with open('../results/edges.csv', 'a') as edgefile:
                edgewrite = csv.writer(edgefile)
                edgewrite.writerow([
                    parent_id, self.links.index(uri), 20 - child_id
                ])


# Node class
class Node:
    
    def __init__(
        self,
        id = None,
        uri = None,
        name = None,
        followers = None,
        popularity = None,
        related = []
    ):
        self.id = id
        self.uri = uri
        self.name = name
        self.followers = followers
        self.popularity = popularity
        self.related = related
'''
Find all fields of "unstructured" metadata in ISIC
Author: Jean R. Clemenceau
Date Created: 6/8/2017
'''
import requests
import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-c','--count',default=100000,help='Limit of images checked')
ap.add_argument('-o','--output',default='all_unstructured_keys.txt',help='Output filename')
args = vars(ap.parse_args())

itemcnt = args['count']
req1 = requests.get('https://isic-archive.com/api/v1/image?limit='+str(itemcnt)+'&offset=0&sort=name&sortdir=1')
idlist = [img['_id'] for img in req1.json()]

def getDict(imgID):
    req = requests.get('https://isic-archive.com/api/v1/image/'+imgID)
    return req.json()

dictlist = list(map(getDict,idlist))

keycollection = [aDict['meta']['unstructured'].keys() for aDict in dictlist]
keylist = list(set([item for sublist in keycollection for item in sublist ]))
keylist.sort()

with open(args['output'],'w') as f:
    f.write(','.join(keylist))

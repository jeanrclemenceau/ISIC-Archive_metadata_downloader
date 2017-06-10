'''
Download metadata from ISIC Archive database
Author: Jean R. Clemenceau
Date Created: 6/8/2017
'''
import requests
import argparse
import csv

#define command line aguments
ap = argparse.ArgumentParser()
ap.add_argument('-c','--count',default=100000,type=int,help='number of entries requested')
ap.add_argument('-o','--output',default='ISIC_metadata.csv',help='path+name of output file')
ap.add_argument('-k','--keys',default=None,help='CSV file containing kunstructured keys of interest')
args = vars(ap.parse_args())

#request image ids
itemcnt = str(args['count'] +1) #make arg value inclusive
req1 = requests.get('https://isic-archive.com/api/v1/image?limit='+itemcnt+'&offset=0&sort=name&sortdir=1')
idlist = [img['_id'] for img in req1.json()]

#read unstructured fields of interest
if args['keys'] is None:
    fieldlist = []
else:
    with open(args['keys'],'r') as f:
        freader = csv.reader(f)
        fieldlist = [row for row in freader]

#define extraction function
def imgMetadataReq(imgID,keys):
    req = requests.get('https://isic-archive.com/api/v1/image/'+imgID)
    reqDict = req.json()
    outputDict = {
        'image_id':              reqDict['_id'],
        'image_name':            reqDict['name'],
        'created':               reqDict['created'],
        'dataset_id':            reqDict['dataset']['_id']  if '_id' in reqDict['dataset'] else 'NA',
        'dataset_name':          reqDict['dataset']['name']  if 'name' in reqDict['dataset'] else 'NA',
        'pixelsx':               reqDict['meta']['acquisition']['pixelsX']  if 'pixelsX' in reqDict['meta']['acquisition'] else 'NA',
        'pixelsy':               reqDict['meta']['acquisition']['pixelsY']  if 'pixelsY' in reqDict['meta']['acquisition'] else 'NA',
        'age':                   reqDict['meta']['clinical']['age_approx'] if 'age_approx' in reqDict['meta']['clinical'] else 'NA',
        'sex':                   reqDict['meta']['clinical']['sex'] if 'sex' in reqDict['meta']['clinical'] else 'NA',
        'benign_malignant':      reqDict['meta']['clinical']['benign_malignant'] if 'benign_malignant' in reqDict['meta']['clinical'] else 'NA',
        'diagnosis':             reqDict['meta']['clinical']['diagnosis'] if 'diagnosis' in reqDict['meta']['clinical'] else 'NA',
        'diagnosis_confirm_type':reqDict['meta']['clinical']['diagnosis_confirm_type'] if 'diagnosis_confirm_type' in reqDict['meta']['clinical'] else 'NA',
        'melanocytic':           reqDict['meta']['clinical']['melanocytic'] if 'melanocytic' in reqDict['meta']['clinical'] else 'NA',
        'tags':                  ';'.join(reqDict['notes']['tags'])  if ('tags' in reqDict['notes']) and (len(reqDict['notes']['tags'])>0) else 'NA',
        'updated':               reqDict['updated']  if 'updated' in reqDict else 'NA'
    }
    for keyset in keys:
        outputDict[keyset[0]] = reqDict['meta']['unstructured'][keyset[0]] if keyset[0] in reqDict['meta']['unstructured'] else 'NA'

    return outputDict

#import all data
metadata = [imgMetadataReq(_id,fieldlist) for _id in idlist]

#setup export keys
exportKeys = ['image_id','image_name','created','dataset_id','dataset_name',
    'pixelsx','pixelsy','age','sex','benign_malignant','diagnosis',
    'diagnosis_confirm_type','melanocytic','updated','tags',]
unstructured_keys = [row[0] for row in fieldlist]
exportKeys = exportKeys + unstructured_keys

#export to strings
allText=[]
for entry in metadata:
    allText.append( ','.join([str(entry[key]) for key in exportKeys] ))

with open(args['output'],'w') as f:
    f.write(','.join(exportKeys) + '\n')
    f.write('\n'.join(allText))

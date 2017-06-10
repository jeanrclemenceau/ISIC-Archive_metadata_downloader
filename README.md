# ISIC-Archive_metadata_downloader
Scripts to download image metadata from the [ISIC Archive RESTful API](https://isic-archive.com/api/v1)

The [International Skin Imaging Collaboration (ISIC) Archive](https://isic-archive.com/#) is a partnership among multiple institutions to create an image repository of skin lesions. One of its goals is to improve clinical support in the identification of skin cancer.

The website provides a straight-forward method of downloading the [archive's images](https://isic-archive.com/#images), but their metadata is only available through their RESTful API. Unfortunately they have not yet implemented a batch-download option for all the images' details. This is why I have written these python scripts.

## Files
* **ISIC_metadata_importer** Downloads metadata for images into a CSV Files.

```
usage: ISIC_metadata_importer.py [-h] [-c COUNT] [-o OUTPUT] [-k KEYS]

optional arguments:
  -h, --help            show this help message and exit
  -c COUNT, --count COUNT
                        number of entries requested
  -o OUTPUT, --output OUTPUT
                        path+name of output file
  -k KEYS, --keys KEYS  CSV file containing kunstructured keys of interest
```

* **ISIC_unstructured_fields.py** Returns all unstructured fields available into a comma-separated list. Not all image entries have all these fields, so you might need these for consistency.
* **unstructured_keys.csv** Input file that defines the unstructured fields of interest. Use the outout from [ISIC_unstructured_fields.py](ISIC_unstructured_fields.py) to create a CSV file as shown in the table belos. Make sure your internal field names are unique.

|Internal Field Names|ISIC Field Names|
|---|---|
|age|age_approx
|img_name|name
|...|...

* **all_unstructured_keys.txt** A list of unstructured keys extracted from all the images available as of 6/9/2017.

## How To
If you agree with the following:
* You want to get the metadata from all the images (max 100000)
* You think the fields I have defined look appropriate (or don't care about them)

Then clone this repo and execute this line:
```
python ISIC_metadata_importer.py -k unstructured_keys.csv
```

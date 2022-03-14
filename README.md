# UK street crimes

This repository contains tools to extract, store and access UK reported street crimes.

## Datasets

Relevant datasets can be found (generated) here: https://data.police.uk/data/ . 

1. Go to https://data.police.uk/data/ 
2. On the page select the following for the respective fields:
    - Date Range: January 2019 to March 2020
    - Forces: All forces
    - Data sets: Include crime data and Include outcomes data
3. Once you have downloaded the zip file and extracted the data, you will notice for each
district has two files.
    -   As an example for “Avon and Somerset” we have:
        - 2019-01-avon-and-somerset.csv and;
        - 2019-01-avon-and-somerset-outcomes.csv
    
## Requirements

In order to run the tools you will need the following:
- python >= 3.9 (and pip)
- docker
- docker-compose

For python, it is recommended to use virtualenv. 

## Installation

Command line script and all required python packages can be installed by running:

```
pip install .
```

## How to run

Project uses Elasticsearch to store extracted and structured data and Kibana to access it and visualize.
In order to set up basic infrastructure run:

```
docker-compose up -d
```

It will start docker containers running single Elasticsearch server and Kibana. 
After a few moments Kibana should be accessible from your browser on `localhost:5601`.

To run street crime data extraction execute the following command:
```
extract-street-crime-data {DATA_DIR}
```
Where `DATA_DIR` is a local path to extracted street crimes data from section `Datasets`.

#### Example
If your directory structure looks like this:
```
   |-uk-street-crimes
   |-data
   |---f9c22623b64f6165fb7823e8014a8a022a7ad3b8
   |-----2019-01
   |-----2019-02
   |-----2019-03
   |-----2019-04
   |-----2019-05
   |----- ...
```
Run:
```
extract-street-crime-data ../dataset/f9c22623b64f6165fb7823e8014a8a022a7ad3b8
```

## Importing Kibana dashboard

Open side Menu in Kibana and go to `Stack Management`. Then select `Saved Objects` and 
click `Import` on the top right side of the window. Select and open a `street-crimes.ndjson` file
located in the `dashboard/` directory in this repository and then click `Import`. 
After you accept all the listed items, the UK Street Crimes Dashboard should be available in Kibana,
where you can access extracted dataset. 
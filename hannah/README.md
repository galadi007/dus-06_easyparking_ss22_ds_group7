# dus-06_easyparking_ss22_ds_group7 (hannahsbranch)

We have three main scripts/notebooks:
- merge_data.ipynb: First attempt at merging various datasets. Thomas' web application uses the output of this script called `merged_data.csv`
- merge_data_including_bala.ipynb: Like merge_data.ipynb but with scraped data from Bala instead of Offene Daten Köln for parking garages. The output file is called `merged_data_with_bala.csv`
- app.py: Streamlit application to display the merged data (`merged_Data_with_bala.csv`)

## Included data in the merged dataset
- Parking garages: 

    https://offenedaten-koeln.de/dataset/parkhausbelegung


- Park & Ride:

    https://offenedaten-koeln.de/dataset/park-and-ride-anlagen-koeln
- Disabled parking:

    https://offenedaten-koeln.de/dataset/behindertenparkpl%C3%A4tze-k%C3%B6ln
- Charging stations:

    https://www.bundesnetzagentur.de/DE/Fachthemen/ElektrizitaetundGas/E-Mobilitaet/Ladesaeulenkarte/start.html
- Parking meters:

    https://offenedaten-koeln.de/dataset/parkscheinautomaten-koeln/resource/11667407-a0d4-42ea-95d8-a0c5e40017dc#{}

All data except for the scraped parking garage data were gathered from Offene Daten Köln website

## How to run streamlit application
In a terminal:

Install streamlit with pip
```
pip install streamlit
```

go to the folder where the streamlit script is and call streamlit like:
```
streamlit run app.py
```
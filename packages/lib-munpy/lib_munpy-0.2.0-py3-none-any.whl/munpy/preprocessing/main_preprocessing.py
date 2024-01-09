import argparse

from munpy import config
from munpy.preprocessing.background import process_background_v2
from munpy.preprocessing.meteo import download_meteo


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('city')
    args = parser.parse_args()

    city = args.city

    # BACKGROUND
    process_background_v2(city, config.API_KEY)

    # METEO
    download_meteo(city)

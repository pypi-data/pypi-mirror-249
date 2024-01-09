import os.path

import numpy as np
import pandas as pd

from munpy import config
from munpy.general import readBinary


def get_munich_results(city, emission=True):
    """

    :param city: folder where binary result files are being stored.
    :param emission: if True, se añaden las emisiones de PM10 y PM25. If False, se dejan tal cuál sacados de chimere.
    :return:
    """

    city_dir = os.path.join(config.LEZ_DIR, city)
    result_dir = os.path.join(city_dir, 'results')
    background_dir = os.path.join(city_dir, 'background')
    emission_dir = os.path.join(city_dir, 'emission')
    street_file = os.path.join(city_dir, 'domain/street.dat')

    street = pd.read_csv(street_file, sep=';').rename(columns={'#id': 'street_id'})
    N_street = len(street)

    results_dataframe = pd.DataFrame()
    results_dataframe['street_id'] = street['street_id']

    for gas in [config.CO_COLUMN, config.NO2_COLUMN, config.NO_COLUMN, config.O3_COLUMN]:
        gas_filename = os.path.join(result_dir, f'{gas.upper()}.bin')
        gas_results = readBinary(gas_filename, N_street)
        gas_results = np.mean(gas_results[3:], axis=0)  # media temporal a partir de la 3a iteración (estabilidad)
        results_dataframe[gas] = gas_results

    for pm in [config.PM10_COLUMN, config.PM25_COLUMN]:
        pm_result = readBinary(os.path.join(background_dir, f'{pm.upper()}.bin'), N_street)

        if emission:
            pm_emission = readBinary(os.path.join(emission_dir, f'{pm.upper()}.bin'), N_street)
            pm_result = pm_result + pm_emission / np.mean(pm_emission)

        results_dataframe[pm] = np.mean(pm_result[3:], axis=0)

    return results_dataframe


def timestamps(date):
    """
    Generates a pandas Series of timestamps for a given date hourly.

    :param date: String "YYYY-MM-DD"
    :return:
    """

    date_object = pd.to_datetime(date, format='%Y-%m-%d')
    hourly_timestamps = pd.date_range(start=date_object, periods=24, freq='H')
    formatted_timestamps = hourly_timestamps.strftime('%Y-%m-%dT%H:%M:%S')
    hourly_series = pd.Series(formatted_timestamps)
    return hourly_series


def get_munich_timeresults(city, street, date='2023-11-20'):
    """

    :param city:
    :param street:
    :param date:
    :return:
    """

    city_dir = os.path.join(config.LEZ_DIR, city)
    result_dir = os.path.join(city_dir, f'results/{date}')
    background_dir = os.path.join(city_dir, f'background/{date}')
    street_file = os.path.join(city_dir, 'domain/street.dat')

    street_df = pd.read_csv(street_file, sep=';').rename(columns={'#id': 'street_id'})
    N_street = len(street_df)

    results_dataframe = pd.DataFrame()

    for gas in [config.CO_COLUMN, config.NO2_COLUMN, config.NO_COLUMN, config.O3_COLUMN]:
        gas_filename = os.path.join(result_dir, f'{gas.upper()}.bin')
        gas_results = readBinary(gas_filename, N_street)[:, street]
        results_dataframe[gas] = gas_results

    results_dataframe = results_dataframe.groupby(results_dataframe.index // 3).agg('mean')  # Media horaria

    for pm in [config.PM10_COLUMN, config.PM25_COLUMN]:
        pm_background = readBinary(os.path.join(background_dir, f'{pm.upper()}.bin'), N_street)[:24, street]
        results_dataframe[pm] = pm_background

    # Añadir columna de timestamp
    results_dataframe.set_index(timestamps(date), inplace=True)

    return results_dataframe


if __name__ == '__main__':
    results = pd.DataFrame()

    for day in range(20, 31):
        day_results = get_munich_timeresults('lindau', 190, date=f'2023-11-{day}')
        results = pd.concat([results, day_results], axis=0)

    results.to_csv('/home/ngomariz/lindau_data.csv')

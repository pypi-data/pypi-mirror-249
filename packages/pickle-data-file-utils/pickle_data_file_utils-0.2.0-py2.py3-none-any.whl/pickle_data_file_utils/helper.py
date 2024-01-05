import csv
import logging
import json
import pickle


def pickle_to_csv(pickle_file_path: str, csv_file_path: str) -> None:
    try:
        # Load data from the pickle file
        with open(pickle_file_path, 'rb') as pickle_file:
            data = pickle.load(pickle_file)

        # Write data to the CSV file
        with open(csv_file_path, 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerows(data)

        logging.info(f"Data from '{pickle_file_path}' successfully written to '{csv_file_path}'.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")

def csv_to_pickle(csv_file_path: str, pickle_file_path: str) -> None:
    try:
        # Read CSV file and store its contents in a list
        with open(csv_file_path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            data = list(csv_reader)

        # Store the data in a pickle file
        with open(pickle_file_path, 'wb') as pickle_file:
            pickle.dump(data, pickle_file)

        logging.info(f"Data from '{csv_file_path}' successfully stored in '{pickle_file_path}'.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def json_to_pickle(json_file_path: str, pickle_file_path: str) -> None:
    try:
        # Read JSON file and store its contents
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        # Store the data in a pickle file
        with open(pickle_file_path, 'wb') as pickle_file:
            pickle.dump(data, pickle_file)

        logging.info(f"Data from '{json_file_path}' successfully stored in '{pickle_file_path}'.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def pickle_to_json(pickle_file_path: str, json_file_path: str) -> None:
    try:
        # Load data from the pickle file
        with open(pickle_file_path, 'rb') as pickle_file:
            data = pickle.load(pickle_file)

        # Store the data in a JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=2)

        logging.info(f"Data from '{pickle_file_path}' successfully stored in '{json_file_path}'.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def pickle_to_tsv(pickle_file_path: str, tsv_file_path: str) -> None:
    try:
        # Load data from the pickle file
        with open(pickle_file_path, 'rb') as pickle_file:
            data = pickle.load(pickle_file)

        # Write data to the TSV file
        with open(tsv_file_path, 'w', newline='', encoding='utf-8') as tsv_file:
            tsv_writer = csv.writer(tsv_file, delimiter='\t')
            tsv_writer.writerows(data)

        logging.info(f"Data from '{pickle_file_path}' successfully written to '{tsv_file_path}'.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


def tsv_to_pickle(tsv_file_path: str, pickle_file_path: str) -> None:
    try:
        # Read TSV file and store its contents in a list
        with open(tsv_file_path, 'r', newline='', encoding='utf-8') as tsv_file:
            tsv_reader = csv.reader(tsv_file, delimiter='\t')
            data = list(tsv_reader)

        # Store the data in a pickle file
        with open(pickle_file_path, 'wb') as pickle_file:
            pickle.dump(data, pickle_file)

        logging.info(f"Data from '{tsv_file_path}' successfully stored in '{pickle_file_path}'.")
    except Exception as e:
        logging.error(f"An error occurred: {e}")


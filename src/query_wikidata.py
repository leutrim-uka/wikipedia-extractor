"""
City Names Extractor from Wikidata

This module retrieves and processes city names from Wikidata for a specified language.
It fetches city entities with Wikipedia articles in the given language and saves the names to a pickle file.

Usage:
    python city_names_extractor.py <language_code>

Example:
    python city_names_extractor.py en

Functions:
    - fetch_citynames_for_language(language_code): Fetches city names from Wikidata.
    - extract_citynames(data): Extracts city names from the query response.
    - save_citynames(language_code, cityname_list): Saves city names to a pickle file.
    - process_citynames_for_language(language_code): Orchestrates the fetching, extraction, and saving of city names.

Args:
    language_code (str): The language code for Wikipedia (e.g., "en" for English).

Logging:
    Provides info, warning, and error messages for operations.
"""

import requests
import pickle
import logging
import argparse

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# SPARQL query endpoint
SPARQL_ENDPOINT = 'https://query.wikidata.org/sparql'


def fetch_citynames_for_language(language_code):
    """
        Fetches city names for a specified language from Wikidata.

        This function constructs and executes a SPARQL query to retrieve city names
        from Wikidata that have Wikipedia articles in the specified language. The
        query searches for entities classified as cities (wd:Q515) and retrieves
        their corresponding Wikipedia article links in the given language.

        Args:
            language_code (str): The language code for the Wikipedia edition (e.g., "en" for English, "fr" for French).

        Returns:
            dict or None: A dictionary containing the JSON response from the SPARQL endpoint if the request is successful,
                          otherwise None.
    """

    query = (
            "SELECT ?article WHERE {"
            "?city wdt:P31 / wdt:P279* wd:Q515 ."
            "?article schema:about ?city ;"
            f"schema:isPartOf <https://{language_code}.wikipedia.org/> ."
            "SERVICE wikibase:label { bd:serviceParam wikibase:language \"" + language_code + "\" . }"
                                                                                              "}"
    )

    try:
        response = requests.get(SPARQL_ENDPOINT, params={'query': query, 'format': 'json'})

        if response.ok:
            data = response.json()
            logger.info(f"Success: {language_code}")
            return data
        else:
            logger.error(f"Error {response.status_code} for language {language_code}")
            return None
    except requests.RequestException as e:
        logger.error(f"Request failed for language {language_code}: {e}")
        return None


def extract_citynames(data):
    """
        Extracts city names from the SPARQL query response data.

        This function processes the JSON response from a SPARQL query to Wikidata
        to extract city names. It expects the response to contain a list of
        Wikipedia article links for cities and extracts the city names from these
        links.

        Args:
            data (dict): The JSON response data from the SPARQL endpoint containing city Wikipedia article links.

        Returns:
            list: A list of city names extracted from the Wikipedia article links.
                  Returns an empty list if the input data is None or empty.
    """
    if not data:
        return []

    list_of_links = [item['article']['value'] for item in data['results']['bindings']]
    cityname_list = [name.split("/")[-1] for name in list_of_links]
    return cityname_list


def save_citynames(language_code, cityname_list):
    """
        Saves the list of city names to a pickle file.

        Args:
            language_code (str): The language code for the Wikipedia edition.
            cityname_list (list): The list of city names to be saved.

        Logs:
            Info message upon successful save.
            Error message if saving fails.
    """

    filename = f"../data/{language_code}_citynames.txt"
    try:
        with open(filename, "w") as f:
            for city in cityname_list:
                f.write(f"{city}\n")
        logger.info(f"City names saved to {filename}")
    except IOError as e:
        logger.error(f"Failed to save city names to {filename}: {e}")

def process_citynames_for_language(language_code):
    """
        Processes and saves city names for a specified language from Wikidata.

        Fetches city names for the given language code from Wikidata, extracts the
        city names, and saves them to a pickle file.

        Args:
            language_code (str): The language code for the Wikipedia edition.

        Logs:
            Info message when querying Wikidata.
            Warning message if no city names are found.
    """
    logger.info(f"Querying Wikidata for language: {language_code}")
    data = fetch_citynames_for_language(language_code)
    cityname_list = extract_citynames(data)
    if cityname_list:
        save_citynames(language_code, cityname_list)
    else:
        logger.warning(f"No city names found for language {language_code}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process Wikipedia city names for a given language.')
    parser.add_argument('language_code', type=str, help='The language code for Wikipedia (e.g., "en" for English).')

    args = parser.parse_args()

    process_citynames_for_language(args.language_code)

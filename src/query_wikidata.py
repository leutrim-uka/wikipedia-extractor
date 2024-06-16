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
    if not data:
        return []

    list_of_links = [item['article']['value'] for item in data['results']['bindings']]
    cityname_list = [name.split("/")[-1] for name in list_of_links]
    return cityname_list


def save_citynames(language_code, cityname_list):
    filename = f"../data/{language_code}_citynames.pkl"
    try:
        with open(filename, "wb") as f:
            pickle.dump(cityname_list, f)
        logger.info(f"City names saved to {filename}")
    except IOError as e:
        logger.error(f"Failed to save city names to {filename}: {e}")


def process_citynames_for_language(language_code):
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

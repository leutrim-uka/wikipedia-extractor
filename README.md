# Wikipedia article extractor
This project uses the Wikipedia API to download city articles as plaintext or HTML from Wikipedia. 

## Structure:
This project includes two Python scripts: 
* `query_wikidata.py`: Python script to query Wikidata for city names in a specified language.
* `extract_wikipedia.py`: Python script to extract Wikipedia articles for cities based on the results from the previous file.


## Steps
1. Clone the repository:
   ```bash
   git clone git@github.com:leutrim-uka/wikipedia-extractor.git
   ```

2. Install dependencies:
    ```bash
   pip install -r requirements.txt
   ```
   
To be able to donwload the articles from Wikipedia using the API, we need to know construct the corresponding URLs. In the URL structure, each article is identified through its title. As a result, we need to get a list of titles for the articles we want to download. We do this through Wikidata. In our usecase, we generate a list of titles corresponding to city articles:
3. Generate list of titles:
    ```bash
   cd src
   python query_wikidata.py <language_code>
   ```
   _<language_code> should be replaced with values like "en", "sq", "de", and so on, depending on the language you want the articles to be downloaded in._
4. Download articles
    ```bash
    python extract_wikipedia.py <city_list_filepath> <language> <output_format> <project_name> <email> <max_requests_per_second> [--n <number_of_cities>]
   ```
   Arguments:
- `city_list_filepath`: Path to the text file containing the list of cities.
- `language`: Language code that should match the one used in previous command.
- `output_format`: Choose between "html" or "text".
- `project_name`: Project identifier to be included in requests header for MediaWiki API.
- `email`: Your personal email address included in requests header for MediaWiki API.
- `max_requests_per_second`: Maximum requests made to WikiMedia API per second.
- `--n`: Optional argument to specify a small integer number to test a few cities at first.

## Example usage:
1. Generate list of city names (in the format they should be included in the URL):
    ```bash
   python query_wikidata.py en
   ```
   This will create a text file named `en_citynames.txt` in the `../data` directory. 

2. Download the Wikipedia article.
    ```bash
    python extract_wikipedia.py ../data/en_citynames.txt en html my_project myemail@example.com 100 --n 10
    ```
   This will create a directory named `cities` in the `data` folder. Each article will be stored in its own text file within this folder.

**Note**: To get articles for some other category (not cities), you will need to modify the SPARQL query in the `query_wikidata.py` file.
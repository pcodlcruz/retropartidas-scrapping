import pandas as pd
import requests
import os
import logging
from dotenv import load_dotenv

from src.config import config

load_dotenv()  # Loads variables from the .env file

def __set_logging_level():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def retrieve_sections_info():
    """ 
    Retrieves the sections information from the website.
    """
    if not config.get_url_paths():
        logging.error("The URL paths are not configured. Check your .env file for RETROPARTIDAS_URL_PATHS.")
        return {} 

    urls = [f"{config.get_base_url()}{path}" for path in config.get_url_paths()]
    return [{'url': url, 'output_file_name': url.split('/')[-1]} for url in urls] 

def scrape_section(section_info: list[dict]):
    """
    Scrapes all pages of the table, extracts the data, and saves it to a JSON file.
    """
    if not config.get_session_cookie():
        logging.error("The session cookie is not configured. Make sure to create a .env file with the RETROPARTIDAS_SESSION_COOKIE variable.")
        return

    cookies = {'retropartidas_session': config.get_session_cookie()}

    for section in section_info:
        
        url = section['url']
        output_file_name = f'output/{section['output_file_name']}'
        all_dataframes = []
        page_number = 1

        logging.info(f"--- Starting scrape for section: {url} ---")

        while True:
            paginated_url = f"{url}?page={page_number}"
            logging.info(f"Attempting to get data from: {paginated_url}")

            try:
                response = requests.get(paginated_url, cookies=cookies)
                response.raise_for_status()  # Raises an error for 4xx/5xx responses

                # Pandas reads the HTML content we already obtained
                tables = pd.read_html(response.text)

                if tables:
                    # If there is at least one table, we process it and continue to the next page
                    df = tables[0]
                    all_dataframes.append(df)
                    logging.info(f"  -> Success! Found {len(df)} rows on page {page_number}.")
                    page_number += 1
                else:
                    # If there are no tables, we assume we have reached the end of the pagination
                    logging.info("No more tables found. Finalizing the loop for this section.")
                    break
            except requests.exceptions.RequestException as e:
                logging.error(f"Request failed for page {page_number}: {e}. Stopping this section.")
                break
            except ValueError:
                logging.info(f"No table found on page {page_number}. Assuming it's the end of the data for this section.")
                break
            
        if all_dataframes:
            # We concatenate all dataframes into a single one
            final_df = pd.concat(all_dataframes, ignore_index=True)
            logging.info(f"Scraping completed for this section. Total rows retrieved: {len(final_df)}")

            # Ensure the output directory exists before saving the file
            output_dir = os.path.dirname(output_file_name)
            if output_dir:
                os.makedirs(output_dir, exist_ok=True)

            # We convert the DataFrame to JSON and save it to a file
            final_df.to_json(output_file_name, orient='records', indent=4, force_ascii=False)
            logging.info(f"Data saved to '{output_file_name}'")
        else:
            logging.warning(f"Could not retrieve any data for section: {url}")

if __name__ == "__main__":
    __set_logging_level()
    sections_info = retrieve_sections_info()
    if sections_info:
        scrape_section(sections_info)
    else:
        logging.info("No sections to scrape. Exiting.")
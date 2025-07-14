import pandas as pd
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Loads variables from the .env file

BASE_URL = 'https://retropartidas.inforpsico.com/admin/games/proposed'
SESSION_COOKIE = os.getenv('RETROPARTIDAS_SESSION_COOKIE')
OUTPUT_FILENAME = 'output/proposed_games.json'


def scrape_all_pages():
    """
    Scrapes all pages of the table, extracts the data, and saves it to a JSON file.
    """
    if not SESSION_COOKIE:
        print("Error: The session cookie is not configured.")
        print("Make sure to create a .env file with the RETROPARTIDAS_SESSION_COOKIE variable.")
        return

    cookies = {'retropartidas_session': SESSION_COOKIE}
    all_dataframes = []
    page_number = 1

    print("Starting the paginated scraping process...")

    while True:
        paginated_url = f"{BASE_URL}?page={page_number}"
        print(f"Attempting to get data from: {paginated_url}")

        try:
            response = requests.get(paginated_url, cookies=cookies)
            response.raise_for_status()  # Raises an error for 4xx/5xx responses

            # Pandas reads the HTML content we already obtained
            tables = pd.read_html(response.text)

            if tables:
                # If there is at least one table, we process it and continue to the next page
                df = tables[0]
                all_dataframes.append(df)
                print(f"  -> Success! Found {len(df)} rows on page {page_number}.")
                page_number += 1
            else:
                # If there are no tables, we assume we have reached the end of the pagination
                print("No more tables found. Finalizing the loop.")
                break
        except requests.exceptions.RequestException as e:
            print(f"Error making the request for page {page_number}: {e}")
            print("Stopping the process. The last page may have been reached.")
            break
        except ValueError as e:
            print(f"Error processing the table on page {page_number}: {e}")
            print("Stopping the process. The last page may have been reached.")
            break
        
    if all_dataframes:
        # We concatenate all dataframes into a single one
        final_df = pd.concat(all_dataframes, ignore_index=True)
        print(f"\nScraping completed. Total rows retrieved: {len(final_df)}")

        # We convert the DataFrame to JSON and save it to a file
        final_df.to_json(OUTPUT_FILENAME, orient='records', indent=4, force_ascii=False)
        print(f"Data has been saved in JSON format in the file: '{OUTPUT_FILENAME}'")
    else:
        print("Could not retrieve any data.")

if __name__ == "__main__":
    scrape_all_pages()
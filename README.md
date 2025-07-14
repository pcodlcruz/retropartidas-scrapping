# Retropartidas Scraper

This project contains a Python script to scrape data from tables in different sections of the `retropartidas.com` website and save it in JSON format.

## Prerequisites

-   Python 3.8 or higher
-   Git

## Installation

Follow these steps to set up the development environment.

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/your_username/retropartidas-scrapping.git
    cd retropartidas-scrapping
    ```
    *(Replace the URL with your repository's URL)*

2.  **Create a virtual environment (recommended):**

    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows usa `venv\Scripts\activate`
    ```

3.  **Install the dependencies:**

    The project uses the libraries listed in `requirements.txt`. To install them, run:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

The script requires credentials and settings that are managed through a `.env` file.

1.  **Create the `.env` file:**

    Copy the example file `.env.example` to create your own configuration file.

    ```bash
    cp .env.example .env
    ```

2.  **Configure the environment variables:**

    Open the `.env` file with a text editor and modify the following variables:

    -   `RETROPARTIDAS_SESSION_COOKIE`: To access the tables, the script needs a valid session cookie. To get it:
        1.  Log in to `https://retropartidas.com` with your browser.
        2.  Open the developer tools (usually with F12).
        3.  Go to the "Application" tab (or "Storage").
        4.  In the left-hand menu, find "Cookies" and select the `retropartidas.com` domain.
        5.  Look for the cookie named `retropartidas_session` and copy its value.
        6.  Paste that value into the `.env` file.

    -   `RETROPARTIDAS_URL_PATHS`: Defines the site sections you want to scrape. These should be the URL paths, separated by commas. For example: `/videojuegos/nes/juegos,/videojuegos/snes/juegos`.

    An example `.env` file would look like this:

    ```ini
    # Session cookie obtained from the browser after logging into retropartidas.com
    RETROPARTIDAS_SESSION_COOKIE="eyJpdiI6Im...very_long_value..."

    # Paths of the sections to be scraped, separated by commas
    RETROPARTIDAS_URL_PATHS="/videojuegos/nes/juegos,/videojuegos/snes/juegos,/videojuegos/n64/juegos"
    ```

## Usage

Once you have installed the dependencies and configured the `.env` file, you can run the main script:

```bash
python main.py
```

The script will start processing each of the paths defined in `RETROPARTIDAS_URL_PATHS`. You will see in the console the progress of the scraping for each section and each page.

## Interpretation of the Results

At the end of the execution, you will find the data files in the folder `output/`.

- A JSON file will be created for each path specified in the configuration.
- The name of each file is generated from the last segment of the URL (e.g. for the path `/video games/nes/games`, the file will be `output/games.json`).
- Important**: If you have multiple paths ending with the same name (e.g. `/nes/games` and `/snes/games`), the output file will be overwritten. Make sure the paths are unique if you want to keep all data separate or adjust the script to generate unique file names.
- Each JSON file contains a list of objects, where each object represents a row of the table extracted from the website.
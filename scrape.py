"""
Parse Apple's "Identify your model" pages and write to JSON file with year,
model identifier, and model name

Usage:
- Specific model(s): python3 scrape.py 'MacBook' 'MacBook Air'
- All models: python3 scrape.py
"""

import sys
import json
import requests
from bs4 import BeautifulSoup
from pathlib import Path

PROJECT_VERSION:   str = "1.2.0"
STORAGE_DIRECTORY: str = "models"
BASE_URL:          str = "https://support.apple.com"
LOCALIZATION:      str = "en-us"

URLS: dict = {
    "MacBook":     "HT201608",
    "MacBook Air": "HT201862",
    "MacBook Pro": "HT201300",
    "iMac":        "HT201634",
    "Mac Pro":     "HT202888",
    "Mac Studio":  "HT213073",
    "Mac mini":    "HT201894",
}


class FetchModels:

    def __init__(self, model: str) -> None:
        if model not in URLS:
            raise ValueError(f"Model {model} not found")

        print(f"Fetching {model} models...")

        self.model = model
        self.url = f"{BASE_URL}/{LOCALIZATION}/{URLS[model]}"


    def results(self) -> dict:
        """
        Return results
        """
        return self._fetch()


    def _clean(self, content: str) -> list:
        """
        Split content by multiple characters
        """
        # Note that 'U+00a0' is the difference between entries 1 and 2
        characters_to_split = [", ", ", ", "\\xa0", ";", " "]
        content_list = []

        # Note that we may be either splitting a string or a list
        for character in characters_to_split:
            if character in content:
                content = content.split(character)

        if isinstance(content, str):
            content_list.append(content)
        else:
            content_list = content

        # Clean
        for index, item in enumerate(content_list):
            content_list[index] = item.strip()

        return content_list


    def _fetch(self) -> dict:
        """
        Fetch models from Apple's website
        Returns a dict of years, model identifiers, and model names

        Structure:
        {
            Year: {
                Model Identifier: [
                    Model Name,
                    ...
                ]
            }
        }
        """
        models = {}

        response = requests.get(self.url)
        if response.status_code != 200:
            raise Exception(f"Error fetching {self.url}")

        soup = BeautifulSoup(response.text, "html.parser")
        if self.model == "MacBook Air":
            return self._fetch_air(soup)

        header = "h2" if self.model != "MacBook" else "h3"

        # Every header is the year
        for year in soup.find_all(header):
            try:
                int(year.text)
            except:
                continue

            for sibling in year.find_next_siblings("p"):

                # Separate into each model
                for model in sibling.find_all("b"):
                    model_name = model.text.strip()

                    # If the year is not in the model's name, we've gone too far
                    if year.text not in model_name:
                        break

                    if model_name == "":
                        continue

                    model_identifiers = ""

                    # Grab the next sibling of 'sibling'
                    _sibling = sibling.find_next_sibling("p")
                    while True:
                        if _sibling is None:
                            break

                        if "Model Identifier:" in _sibling.text:
                            model_identifiers = _sibling.text.split(":")[1].strip()
                            break

                        _sibling = _sibling.find_next_sibling("p")

                    # Clean
                    model_identifiers = self._clean(model_identifiers)

                    # Add to models dict
                    if year.text not in models:
                        models[year.text] = {}

                    for model_identifier in model_identifiers:
                        if model_identifier not in models[year.text]:
                            models[year.text][model_identifier] = [model_name]
                        else:
                            models[year.text][model_identifier].append(model_name)

                        print(f"  {year.text} - {model_identifier} - {model_name}")

        return models


    def _fetch_air(self, soup: BeautifulSoup) -> dict:
        """
        Apple has a different structure for the MacBook Air...
        """

        models = {}

        # Every header is a model
        for model in soup.find_all("h2"):
            model_name = model.text.strip()

            model_identifiers = ""
            year = ""

            # Grab the next sibling of 'sibling'
            _sibling = model.find_next_sibling("p")
            while True:
                if _sibling is None:
                    break

                if "Model Identifier:" in _sibling.text:
                    model_identifiers = _sibling.text.split(":")[1].strip()

                if "Year introduced:" in _sibling.text:
                    year = _sibling.text.split(":")[1].strip()

                if model_identifiers and year:
                    break

                _sibling = _sibling.find_next_sibling("p")

            # Clean
            model_identifiers = self._clean(model_identifiers)
            year = self._clean(year)[0]

            try:
                int(year)
            except:
                continue

            # Add to models dict
            if year not in models:
                models[year] = {}

            for model_identifier in model_identifiers:
                if model_identifier not in models[year]:
                    models[year][model_identifier] = [model_name]
                else:
                    models[year][model_identifier].append(model_name)

                print(f"  {year} - {model_identifier} - {model_name}")

        return models


def write(file: Path, content: str):
    """
    Write content to file
    """

    if not Path(file).parent.exists():
        Path(file).parent.mkdir(parents=True, exist_ok=True)

    with open(file, "w") as file:
        file.write(json.dumps(content, indent=4))


if __name__ == "__main__":
    if len(sys.argv) > 1:
        for model in sys.argv[1:]:
            if not model in URLS:
                raise ValueError(f"Model {model} not found")
            results = FetchModels(model).results()
            write(Path(f"{STORAGE_DIRECTORY}/{model.replace(' ', '_')}.json"), results)
    else:
        results = {
            # "MacBook":     {},
            # ...
        }
        for model in URLS:
            results[model] = FetchModels(model).results()
            write(Path(f"{STORAGE_DIRECTORY}/{model.replace(' ', '_')}.json"), results[model])

        write(Path(f"{STORAGE_DIRECTORY}/all.json"), results)




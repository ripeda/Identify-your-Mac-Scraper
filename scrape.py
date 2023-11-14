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

PROJECT_VERSION:   str = "1.0.0"
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
        self.url = f"{BASE_URL}/{LOCALIZATION}{URLS[model]}"


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

        header = "h2" if self.model != "MacBook" else "h3"

        # Every header is the year
        for year in soup.find_all(header):

            for div in year.find_next_siblings("div"):

                # Can be multiple strong's
                for strong in div.find_all("strong"):
                    model_name = strong.text.strip()

                    if model_name == "":
                        continue

                    model_identifiers = ""
                    description = ""

                    # Next few lines are the model identifier
                    # Make sure to include current line
                    description += strong.next_sibling.text
                    for br in strong.find_next_siblings("br"):
                        description += br.next_sibling

                    for line in description.split("\n"):
                        if "Model Identifier:" in line:
                            model_identifiers = line.split(":")[1].strip()

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




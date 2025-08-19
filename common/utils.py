import re
import dateparser
from bs4 import BeautifulSoup
from datetime import date

def clean_name(text: str, is_soup: bool = False, *, suffix_removal_count: int = 1):
    text = text.strip()

    if match := re.match(r"(?:\d+\.\s*)?(.*)", text):
        text = match.group(1).strip()

    for _ in range(suffix_removal_count):
        if match := re.match(r"(.*)\(.+\)\*?$", text):
            text = match.group(1).strip()

    if is_soup:
        text = f"Polévka {text[0].lower()}{text[1:]}"

    return text

def parse_date(text: str) -> date:
    result = dateparser.parse(text, languages = ["cs"]) 
    return result.date() if result else None

def parse_price(text: str) -> int:
    if match := re.match(r"(\d+)", text):
        return int(match.group(1))

def find_strings(soup: BeautifulSoup):
    return [
        string.text.strip()
        for string
        in soup.find_all(string = True)
        if not str.isspace(string)
    ]

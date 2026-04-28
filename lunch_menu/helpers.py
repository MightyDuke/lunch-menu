import re
import dateparser
from datetime import date
from bs4 import BeautifulSoup

def regex_match(regex: str, text: str) -> str:
    if match := re.match(regex, text):
        return match.group(1).strip()
    else:
        return text

def clean_name(text: str, *, remove_numbering: bool = False, prefix_removal_count: int = 0, suffix_removal_count: int = 0) -> str:
    text = text.strip()

    if remove_numbering:
        text = regex_match(r"^\d+\.\s*(.*)$", text)

    for _ in range(prefix_removal_count):
        text = regex_match(r"^\(.+?\)\s*(.*)$", text)

    for _ in range(suffix_removal_count):
        text = regex_match(r"^(.*)\s*\(.+?\).?$", text)

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

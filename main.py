import email
import glob
from pandas import DataFrame
from email.header import decode_header, make_header
from email.message import Message
from bs4 import BeautifulSoup
import json


def find_spy_pixels():
    df = DataFrame([], columns=["src", "sender", "filename", "attributes"])
    df = parse_eml_files(df)
    df = df.drop_duplicates(subset=["src"])
    df = df.sort_values(by=["sender"])
    df.to_csv("results.csv")


def parse_eml_files(df: DataFrame):
    for path in glob.glob("emails/*.eml"):
        print(f"Processing {path}...")
        with open(path, "rb") as file:
            message = email.message_from_bytes(file.read())
        sender = str(make_header(decode_header(message.get('From'))))
        if is_content_type_html(message):
            df = parse_html(df, message, path, sender)
            continue
        if message.is_multipart():
            for part in message.get_payload():
                if is_content_type_html(part):
                    df = parse_html(df, part, path, sender)
                    continue
    return df


def parse_html(df: DataFrame, message: Message, path: str, sender: str):
    html = message.get_payload(decode=True)
    soup = BeautifulSoup(html, "html.parser")
    for img in soup.find_all("img", {"height": "1", "width": "1"}):
        df = log_spy_pixel(df, img["src"], json.dumps(img.attrs), path, sender)
    return df


def is_content_type_html(message):
    return message.get_content_type() == "text/html"


def log_spy_pixel(df: DataFrame, src: str, attributes: str, filename: str, sender: str):
    print(f"Found a spy pixel: {src}")
    return df.append(
        {"src": src, "attributes": attributes, "filename": filename, "sender": sender},
        ignore_index=True
    )


if __name__ == "__main__":
    find_spy_pixels()

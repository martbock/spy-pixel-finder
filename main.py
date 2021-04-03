import email
import glob
import json
from argparse import ArgumentParser, Namespace
from email.header import decode_header, make_header
from email.message import Message
from urllib.parse import urlparse

import numpy as np
from bs4 import BeautifulSoup
from pandas import DataFrame


def find_spy_pixels():
    args = parse_arguments()
    df = DataFrame([], columns=["domain", "src", "sender", "filename", "attributes"])
    df = parse_eml_files(df)
    if args.drop_src_duplicates:
        df = df.drop_duplicates(subset=["src"])
    df = parse_domains(df, args.remove_subdomains)
    df = drop_no_domain(df)
    if args.drop_domain_duplicates:
        df = df.drop_duplicates(subset=["domain"])
    df = df.sort_values(by=["domain"])
    df.to_csv("results.csv")


def parse_arguments() -> Namespace:
    parser = ArgumentParser(description="Find spy pixels in your emails.")
    parser.add_argument("--no-drop-src-duplicates", dest="drop_src_duplicates", action="store_false",
                        help="Don't drop rows that have the same image source URL. Defaults to false.")
    parser.add_argument("-d", "--drop-domain-duplicates", dest="drop_domain_duplicates", action="store_true",
                        help="Drop rows that have a duplicate domain of the image URL. Defaults to false.")
    parser.add_argument("--remove-subdomains", dest="remove_subdomains", action="store_true",
                        help="Remove subdomains of image URLs. This way you can get rid of customer subdomains. "
                             "Defaults to false.")
    return parser.parse_args()


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


def parse_domains(df: DataFrame, remove_subdomains: bool):
    for i, row in df.iterrows():
        domain = urlparse(row["src"]).netloc
        if remove_subdomains:
            domain = '.'.join(domain.split('.')[1:])
        df.at[i, "domain"] = domain
    return df


def drop_no_domain(df: DataFrame):
    df["domain"].replace('', np.nan, inplace=True)
    df.dropna(subset=["domain"], inplace=True)
    return df


if __name__ == "__main__":
    find_spy_pixels()

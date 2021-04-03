import csv
import email
import glob
from email.message import Message
from bs4 import BeautifulSoup

spy_pixels = []


def find_spy_pixels():
    parse_eml_files()
    write_results(spy_pixels)


def parse_eml_files():
    for path in glob.glob("emails/*.eml"):
        with open(path, "rb") as file:
            message = email.message_from_bytes(file.read())
        sender = message.get('From')
        if is_content_type_html(message):
            parse_html(message, path, sender)
            continue
        if message.is_multipart():
            for part in message.get_payload():
                if is_content_type_html(part):
                    parse_html(part, path, sender)
                    continue


def parse_html(message: Message, path: str, sender: str):
    html = message.get_payload(decode=True)
    soup = BeautifulSoup(html, "html.parser")
    for img in soup.find_all("img", {"height": "1", "width": "1"}):
        log_spy_pixel(img["src"], img["alt"], img, path, sender)


def is_content_type_html(message):
    return message.get_content_type() == "text/html"


def log_spy_pixel(src: str, alt: str, raw: str, filename: str, sender: str):
    spy_pixels.append({"src": src, "alt": alt, "raw": raw, "filename": filename, "sender": sender})


def write_results(results: list):
    with open("results.csv", "w") as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["src", "alt", "raw", "filename", "sender"])
        csv_writer.writerows(
            map(lambda r: [r["src"], r["alt"], r["raw"], r["filename"], r["sender"]], results)
        )


if __name__ == "__main__":
    find_spy_pixels()

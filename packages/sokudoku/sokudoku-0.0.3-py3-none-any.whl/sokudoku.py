import time
import curses
import pytesseract
from PIL import Image
import MeCab

def display_text_rsvp(stdscr, text, speed):
    mecab = MeCab.Tagger("-Owakati")
    words = mecab.parse(text).split()
    for word in words:
        stdscr.clear()
        stdscr.addstr(0, 0, word)
        stdscr.refresh()
        time.sleep(speed)

def image_to_text(image_path):
    img = Image.open(image_path)
    text = pytesseract.image_to_string(img, lang='jpn')
    return text

image_path = input("Enter the path to the image (if not there, press Enter): ")
if image_path:
    text = image_to_text(image_path)
else:
    text = input("Please enter a sentence: ")

speed = float(input("Enter the display speed in seconds (e.g., 0.5): "))

def main(stdscr):
    display_text_rsvp(stdscr, text, speed)

def run():
    curses.wrapper(main)

if __name__ == "__main__":
    run()

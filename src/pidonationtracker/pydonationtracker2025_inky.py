""" Raspberry Pi Donation Tracker

"""
from datetime import datetime
import requests
from bs4 import BeautifulSoup
from PIL import Image, ImageFont, ImageDraw
import html
import json
import randomimagepicker
from inky.auto import auto

# Inky display settings
INKY_DISPLAY = auto()
INKY_DISPLAY.set_border(INKY_DISPLAY.BLACK)
DISPLAY_WIDTH = INKY_DISPLAY.WIDTH
DISPLAY_HEIGHT = INKY_DISPLAY.HEIGHT

ALWAYS_REFRESH = False

def get_donation_amount(url):
    """ Get the donation amount from the Tour for Life website

    Returns:
        float: The donation amount
    """

    try:
        # Send HTTP request and get response
        response = requests.get(url)

        print(f"Fetching URL: {url}")
        print(f"Response status code: {response.status_code}")

        # Check if request was successful
        if response.status_code != 200:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return None

        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')

        # The data is stored in a div with the attribute data-page
        # Find the div with the data-page attribute
        div = soup.find("div", {"data-page": True})
        raw_data = div["data-page"]
        # The data is encoded in HTML entities, so we need to decode it
        # Decode HTML entities
        decoded_data = html.unescape(raw_data)  # decode &quot; -> "

        # JSON decode the data
        data = json.loads(decoded_data)
        # The donation amount is in the "funds_raised" field
        fundsraised = data["props"]["campaign"]["funds_raised"]
        # The donatioin amount is in cents, so we need to divide by 100 to get the amount in euros
        fundsinwholeeuros = fundsraised / 100

        # print(f"Funds raised: €{fundsinwholeeuros}")

        # Return the text content if element exists
        if fundsinwholeeuros:
            return fundsinwholeeuros
        else:
            print("Could not find donation element on the page")
            return None        

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None


def giftamount_to_pillow(gift_amount, background_image):
    """ Create a Pillow image with the donation amount

    Args:
        gift_amount (float): The donation amount

    Returns:
        Image: The Pillow image
    """
    image = Image.new("P", (DISPLAY_WIDTH, DISPLAY_HEIGHT))
    text_fill = "white"
    text_stroke = 3
    text_shadow = "black"
    # header_name = "Upcoming appointments:"
    # image = Image.new('RGB', (200, 200), color=(73, 109, 137))
    with Image.open(background_image) as image:
        draw = ImageDraw.Draw(image)
        textfont_size = 100
        textfont = ImageFont.load_default(size=textfont_size)
        text_x = (DISPLAY_WIDTH / 2) - 250
        text_y = (DISPLAY_HEIGHT / 2) - 130

        gift_amount_text = f"EUR {gift_amount:.2f}"
        draw.text((text_x, text_y), gift_amount_text, text_fill, font=textfont,
                    stroke_width=text_stroke, stroke_fill=text_shadow)

        # Add TFL_logo
        tfl_logo = Image.open("TFL_Logo_ 2017_200.png")
        image.paste(tfl_logo, (50, DISPLAY_HEIGHT - 150), tfl_logo)

        # Add Daniel Den Hoed vaantje
        vaantje = Image.open("Vaantje-DanielDenHoed_300.png").convert("RGBA")
        image.paste(vaantje, (DISPLAY_WIDTH-350, DISPLAY_HEIGHT - 120), vaantje)

        return image


if __name__ == "__main__":
    # Print date and time
    print(f"Date and time: {datetime.now()}")

    # Read the previous donation amount from a file
    f = open("donation_amount.txt", "r", encoding="utf-8")
    previous_donation_amount = float(f.read())
    print(f"Previous donation amount: {previous_donation_amount}")
    f.close()

    # URL of the donation page
    personal_url = "https://supporta.cc/lfqd/z0qpn9xqox"
    team_url = "https://supporta.com/lfqd/aydkxe1g6j"
    # <strong class="text-xl font-bold text-slate-900">€ 222,50</strong>
    class_name = "strong.text-xl.font-bold.text-slate-900"

    # Get the current donation amount
    personal_donation_amount = get_donation_amount(personal_url)
    # Always show the donation amount with two decimal places. Even if the amount is a whole number.
    personal_donation_amount = round(personal_donation_amount, 2)
    print(f"Current donation_amount: € {personal_donation_amount:.2f}")

    # Compare the current donation amount with the previous donation amount
    # If the current donation amount is greater than the previous donation amount,
    # write the new donation amount to a file and update the display
    if personal_donation_amount > previous_donation_amount:
        print("New donation!")

        # Write the new donation amount to a file
        f = open("donation_amount.txt", "w", encoding="utf-8")
        f.write(str(personal_donation_amount))
        f.close()

    if personal_donation_amount > previous_donation_amount or ALWAYS_REFRESH:
        # Update the display
        background_image = randomimagepicker.pick_image(".")
        gift_image = giftamount_to_pillow(personal_donation_amount, background_image)
        gift_image.save("giftamount2025.png")

        try:
            INKY_DISPLAY.set_image(gift_image)
            INKY_DISPLAY.show()
        except ValueError as e:
            print(f"Error displaying image: {e}")
            print(f"Error occurred on image: {background_image}")
            # Show dimension of the image
            print(f"Image dimensions: {gift_image.size}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            print("Please check the display connection and try again.")

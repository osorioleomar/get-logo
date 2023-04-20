import os
import requests
from PIL import Image, UnidentifiedImageError
from io import BytesIO
from urllib.parse import urlparse

def get_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

def get_clearbit_logo(domain, size):
    url = f"https://logo.clearbit.com/{domain}?size={size}"
    response = requests.get(url)
    return response.content

def remove_white_background(image):
    image = image.convert("RGBA")
    data = image.getdata()
    new_data = []

    for item in data:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            new_data.append((255, 255, 255, 0))
        else:
            new_data.append(item)

    image.putdata(new_data)
    return image

def main():
    with open("websites.txt", "r") as file:
        links = file.readlines()

    for link in links:
        domain = get_domain(link.strip())
        logo_data = get_clearbit_logo(domain, "800")

        try:
            img = Image.open(BytesIO(logo_data))
            #img_no_white_bg = remove_white_background(img)

            img.save(f"{domain}.png")
            #img_no_white_bg.save(f"{domain}_no_white_bg.png")
        except UnidentifiedImageError:
            print(f"Cannot identify image for domain: {domain}")

if __name__ == "__main__":
    main()

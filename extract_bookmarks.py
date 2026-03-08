import pytesseract
from PIL import Image, ImageEnhance,ImageFilter
import os
import re
import csv


# Path to Tesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Repulserator\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

FOLDER = "screenshots"

# crop area for 5120x1440 screenshot
CROP = (3403, 80, 4278, 1440)

url_pattern = re.compile(r'https?://[^\s]+')

table = []
line_index = 1

title_table = []

urls = []
seen = set()


def clean_title(text):
    # stop reading title at >>
    if ">>" in text:
        text = text.split(">>")[0]

    # keep only letters, numbers, and spaces
    text = re.sub(r'[^A-Za-z0-9 ]+', ' ', text)

    # collapse multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()

    return text


def clean_url(text):
    # remove leading/trailing junk around URLs
    text = re.sub(r'^[^h]*', '', text)   # remove before http/https
    text = re.sub(r'[^0-9A-Za-z:/._\-]+$', '', text)

    return text.strip()

for file in os.listdir(FOLDER):

    # skip debug images
    if file.startswith("crop_") or file.startswith("processed_"):
        continue

    if file.lower().endswith((".png",".jpg",".jpeg")):

        path = os.path.join(FOLDER, file)

        img = Image.open(path)

        # crop bookmark region
        crop = img.crop(CROP)

        # save cropped image
        crop.save(os.path.join(FOLDER, "crop_" + file))

        # convert to grayscale
        # convert to grayscale
        crop = crop.convert("L")

        # upscale for better OCR
        crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS)

        # increase contrast
        contrast = ImageEnhance.Contrast(crop)
        crop = contrast.enhance(3)

        # slight sharpening
        crop = crop.filter(ImageFilter.SHARPEN)

        # save processed image
        crop.save(os.path.join(FOLDER, "processed_" + file))

        # OCR
        ocr_modes = [6, 4, 11]

        text = ""

        for mode in ocr_modes:

            t = pytesseract.image_to_string(
                crop,
                config=f"--psm {mode} -l eng"
            )

            text += "\n" + t

            # fix common OCR spacing issues
            text = text.replace("https ://", "https://")
            text = text.replace("https: //", "https://")
            text = text.replace("https : //", "https://")
            text = text.replace("http ://", "http://")
            text = text.replace("http: //", "http://")
            text = text.replace("http : //", "http://")

            # extract URLs
            url_pattern = re.compile(r'https?\s*:\s*/\s*/\s*[^\s]+')

            found = url_pattern.findall(text)

            for u in found:
                u = re.sub(r'\s+', '', u)

                if u not in seen:
                    urls.append(u)
                    seen.add(u)

                    # ---- TITLE EXTRACTION ----
                    try:
                        y_position = text.find(u)

                        # approximate vertical search region
                        title_region = crop.crop((
                            0,
                            max(0, int(crop.height * 0.05)),
                            crop.width,
                            int(crop.height * 0.2)
                        ))

                        title_text = pytesseract.image_to_string(
                            title_region,
                            config="--psm 6 -l eng"
                        ).strip()
                        
                        title_text = clean_title(title_text)

                    except:
                        title_text = ""

                    title_table.append((line_index, title_text, u, file))

                    table.append((line_index, u, file))
                    line_index += 1


print("URLs found:", len(urls))

# save URL list
with open("bookmarks.txt","w",encoding="utf-8") as f:
    for u in urls:
        f.write(u + "\n")

print("bookmarks.txt created")


with open("bookmark_table.csv", "w", encoding="utf-8") as f:
    f.write("index,url,screenshot\n")
    for idx, url, shot in table:
        f.write(f"{idx},{url},{shot}\n")

print("bookmark_table.csv created")


with open("bookmark_titles.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["index", "title", "url", "screenshot"])

    for idx, title, url, shot in title_table:
        writer.writerow([idx, title, url, shot])

print("bookmark_titles.csv created")




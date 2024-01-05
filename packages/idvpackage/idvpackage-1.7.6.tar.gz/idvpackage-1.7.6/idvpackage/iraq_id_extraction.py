import cv2
import numpy as np
from PIL import Image
from skimage.transform import radon
from google.cloud import vision
from google.oauth2.service_account import Credentials
from google.cloud import vision_v1
from googletrans import Translator
import re
from idvpackage.common import *
import io

translator = Translator()

creds = {
  "type": "service_account",
  "project_id": "clear-battery-409905",
  "private_key_id": "a12c9d07ccfda46d7fbc49333d4fd1168df5136e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCtRMlro9WYJ721\nYpSjkWa/acExNNFhvMHwH1coZ7cX1/ZFv4rFnWd3on+MJ+cDhsxOI47zYa3ry3BM\n3btYFnrWWLIZBsAjssNX7a9l4oSvKHkD/YIy0r/qP48ojaaFscxLQXXj5H1iYV0b\nSVw/JR5dfGfDkD+l9RTUMibK5Yx/IsMdke3dqfa+gWKRCiliYp1F+0aBVIuGBm2b\njoVJYvLB6gzYT64ZbbmQAec3BDctjTO/YJx7AqXeZBPP8mTr7TV+Ud0iMXl0daJd\nGYGVAz/CfhzQCmGFrnbSEzA2t3J4YIlya5w1x5BcUHb1WUig3ADF99psEYU7gyOq\nNy0Q4j9jAgMBAAECggEAAiP/v7ZbdNtw1Y/X5EQZ79108eWu0d/3dBRUYFRqXP9h\ntITkSFgPJ4Q4woOFBXR3Nl6WwoeqEr1bBX1ry2/OVAhD0wP+qweSBZZofKrAFuXk\nxi7Ympt4nC1C2IO/fewEvnKa6+uDvQu/jw8TS63ADUmfLTmtVPXigaieSr1r70TP\nzZ84GJ71scCmMgeStcFAcZU5FiBt2h5iFGSP5fuxWt8rmuSd+06HEiWx0z5yqprp\nPSljbWr1klAECoQQQ3S0jlwNcGZ6erFtbnMYqIUP9zp7a0UaWlECmaRfMnQx4XWt\nbTAbVahfHg/3cLVh7eJhMUCxOlRSgra0QTCXJs0uyQKBgQDYJgEw9rtxuizxVxjn\nJyQDhOQlkIQGO4DCW6zRKSiUYw2wrSOE/rEoycDHeIm2O53tWNEzOxtKU/TxVMx5\nlJT+F6PHEBlhVe8Ktq9lVi9JW4lBysPuAUXt33I0aOk0hElvVPhcqE/mTkB+9jRt\nLLHtiCtDdvIWNxNT533Sg8/p1QKBgQDNNuZNBm01OEkThynU8L5hNd2wRS1F/MXl\nZFsGQ/rroTKhtUXPi1ijiCWFC9stdPdwiO5KHVFi8A7ngOljUz5/J0Bvgv8MeMWU\nAArn/ITDnbmGd+Ihfn84iY+KCM6pxkdNe+y07f6+eCqvYMtIPZQTkYSPQcfMEXAI\nSPBC0a6oVwKBgQCtCD+L4vjLYi74RLE62qqJ5qh9KeOG2buJ27nM9xX1NBaRiQkW\nPo20CU66YFRd/fu/NYrDaF3ActVzHF9UNQ3RGzuQ7+JheVmTSgu/I+9W2mBWuut+\nbKZ+dpIGQrXtxLjE11C7XEIaLCqVeKMfgtgtPwTjTSUfg5eFY5vmGn8mwQKBgQCR\nFnKHHLcTfIL2AocJ3VfMpOfi21Xh+I/12hkc+e0qsOJ6QA5maU+29ugIA9Tnc54J\n+1X2InpLKAxxksvvhIhYH+lHreci6zRNqiYL1JYNM7NapeHD6oqJ74ADiKyMjfoV\nhztYxDdqdM1BB39RyO+rUiPVoR1gYyfBQ8hShaslqwKBgGhL8i68g1yr0ve3O6Wr\n6v0shmy0/tv22B4+654g7XL7cG/NW580WJBr0nHQ3wCekG/roAt3V7Nf4WDXod9C\n/s3Tu/ZUEFEsEVxziMdV/svY49bEElFG2vaf2XZqrZosqybPwprUuq9rc9mPMH2E\nEYWLTCGgPqjTzVnYI8jR2x3b\n-----END PRIVATE KEY-----\n",
  "client_email": "dev-testing@clear-battery-409905.iam.gserviceaccount.com",
  "client_id": "109465336651489430965",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/dev-testing%40clear-battery-409905.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

credentials = Credentials.from_service_account_info(creds)
client = vision_v1.ImageAnnotatorClient(credentials = credentials)


def rotate_image(img):
    img_array = np.array(img)
    gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    h, w = gray.shape
    if w > 640:
        gray = cv2.resize(gray, (640, int((h / w) * 640)))
    gray = gray - np.mean(gray)
    sinogram = radon(gray)
    r = np.array([np.sqrt(np.mean(np.abs(line) ** 2)) for line in sinogram.transpose()])
    rotation = np.argmax(r)
    angle = round(abs(90 - rotation) + 0.5)

    if abs(angle) > 5:
        if angle == 90:
            img = img.transpose(Image.ROTATE_270)
        else:
            img = img.rotate(angle, expand=True)

    return img


def crop_second_part(img):
    width, height = img.size
    half_width = width // 2
    second_part = img.crop((half_width, 0, width, height))
    return second_part


def crop_third_part(img):
    width, height = img.size
    part_height = height // 3
    third_part = img.crop((0, 2 * part_height, width, height))
    return third_part


def extract_text_from_image_data(image):
    """Detects text in the file."""

    with io.BytesIO() as output:
        image.save(output, format="PNG")
        content = output.getvalue()

    image = vision_v1.types.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    
    return texts[0].description


def detect_id_card(image_data, id_text, part=None):
    
    if id_text:
        vertices = id_text[0].bounding_poly.vertices
        left = vertices[0].x
        top = vertices[0].y
        right = vertices[2].x
        bottom = vertices[2].y

        padding = 30
        left -= padding
        top -= padding
        right += padding
        bottom += padding

        # img = image_data
        img = Image.open(io.BytesIO(image_data))
        id_card = img.crop((max(0, left), max(0, top), right, bottom))

        aligned_img = rotate_image(id_card)
        if part=='second':
            part_img = crop_second_part(aligned_img)
        if part=='third':
            part_img = crop_third_part(aligned_img)
        
        # 2nd call to vision AI
        part_text = extract_text_from_image_data(part_img)

        return id_card, part_img, part_text
    else:
        print('No text found in the image.')


def extract_name_fields_from_raw(text):
    generic_field_match_pattern = r':\s*([^:\n]*)'
    
    generic_field_matches = re.findall(generic_field_match_pattern, text)
    # print(f"DATA LIST: {generic_field_matches}")

    if len(generic_field_matches[0].split()) <= 2:
        given_name = generic_field_matches[0]
    else:
        given_name = ''
    
    if len(generic_field_matches[1].split()) <= 2:
        fathers_name = generic_field_matches[1]
    else:
        fathers_name = ''
        
    if len(generic_field_matches[3].split()) <= 2:
        surname = generic_field_matches[3]
    else:
        surname = ''

    try: 
        gender_ar = generic_field_matches[-2]
        gender = translator.translate(gender_ar, src='ar', dest='en').text
        if str(gender).lower() == 'feminine':
            gender = 'female'
    except:
        gender_ar, gender = '', None

    name = f"{given_name} {fathers_name} {surname}"
    if name:
        name_en = translator.translate(name, src='ar', dest='en').text.upper()

    names_data  = {
        "gender": gender,
        "gender_ar": gender_ar,
        "name": name,
        "first_name": given_name,
        "fathers_name": fathers_name,
        "last_name": surname,
        "name_en": name_en,
    }

    return names_data


def identify_front(text):
    front_id_keywords = ["The Republic of Iraq", "The Ministry of Interior", "National Card"]
    pattern = '|'.join(map(re.escape, front_id_keywords))
    
    try:
        if re.search(pattern, text, re.IGNORECASE):
            return True
        else:
            return False
    except:
        return 'error'

def extract_numeric_fields_from_raw(ar_front_data):
    front_data = translator.translate(ar_front_data, src='ar', dest='en').text 
    gender_pattern = r"Sex.*?:\s*(\w+)"
    id_number_pattern = r"\b\d{12}\b"
    rfid_number_pattern = r"\b[A-Za-z]{2}\d{7}\b|\b[A-Za-z]\d{8}\b"
        
    gender_match = re.search(gender_pattern, front_data, re.IGNORECASE)
    if gender_match:
        gender = gender_match.group(1)
    else:
         gender = ''
        
    id_number_match = re.search(id_number_pattern, front_data, re.IGNORECASE)
    if id_number_match:
        id_number = id_number_match.group(0)
    else:
        try:
            id_number_match = re.search(id_number_pattern, ar_front_data, re.IGNORECASE)
            id_number = id_number_match.group(0)
        except:
            id_number = ''
        
    rfid_number_match = re.search(rfid_number_pattern, front_data.replace(" ",""), re.IGNORECASE)
    if rfid_number_match:
        rfid_number = rfid_number_match.group(0).upper()
    else:
        rfid_number = ''
    
    front_data = {
        "gender": gender,
        "id_number": id_number,
        "card_number": rfid_number
    }
    
    return front_data


def iraq_front_id_extraction(image_data, front_id_text, front_id_text_description):
    cropped_id_card, second_part, second_part_text = detect_id_card(image_data, front_id_text, part='second')
    front_data = extract_name_fields_from_raw(second_part_text)
    numeric_fields = extract_numeric_fields_from_raw(front_id_text_description)
    filtered_data = {key: value for key, value in front_data.items() if key != 'gender' or value != ''}
    front_data.update(numeric_fields)

    return filtered_data


def handle_mrz_extraction(image_data, back_id_text):
    cropped_id_card, third_part, third_part_text = detect_id_card(image_data, back_id_text, part='third')
    mrz_pattern = r'(IDIRQA.*\n*.*\n*.*\n*.*|IDIRQA.*\n*.*\n*.*\n*.*)'
    mrz1_data_pattern = r'IDIRQ([A-Za-z]{2}\d{7}|[A-Za-z]\d{8}).*?(\d{13})'

    try:
        mrz = re.findall(mrz_pattern, third_part_text.replace(" ","").strip(), re.MULTILINE)
        mrz_str = mrz[0].replace(" ", "")
    except:
        mrz_str = ''

    mrz1 = re.search(r'(IDIRQ.*?<<<)', mrz_str, re.DOTALL)
    mrz1 = mrz1.group(1) if mrz1 else None

    mrz2 = re.search(r'\b\d{7}.*?(?:<<\d|<<\n)', mrz_str)
    mrz2 = mrz2.group(0) if mrz2 else None

    mrz3 = re.search(r'[\n](?:[a-zA-Z<]{6,})', mrz_str)
    mrz3 = mrz3.group(0).replace("\n","") if mrz3 else None

    rfid_number = ''
    id_number = ''

    mrz1_data_match = re.search(mrz1_data_pattern, mrz_str)
    if mrz1_data_match:
        rfid_number = mrz1_data_match.group(1)
        id_number = mrz1_data_match.group(2)

    rfid_number = rfid_number.upper()
    id_number = id_number[1:14] 
    
    try:
        pattern = r'(?<=[A-Z]\d{7})[A-Z]{3}'

        national = re.search(pattern, mrz[0].replace(" ", ""))
        if national:
            nationality = national.group()
        else:
            nationality = ''
    except:
        nationality = ''

    
    back_data_new = {
        "id_number": id_number,
        "card_number": rfid_number,
        "nationality": nationality,
        "mrz": [mrz_str],
        "mrz1": mrz1,
        "mrz2": mrz2,
        "mrz3": mrz3
    }

    return back_data_new


def iraq_back_id_extraction(image_data, back_id_text, back_data):
    mrz_pattern = r'(IDIRQA.*\n*.*\n*.*\n*.*|IDIRQA.*\n*.*\n*.*\n*.*)'
    mrz1_data_pattern = r'IDIRQ([A-Za-z]{2}\d{7}|[A-Za-z]\d{8}).*?(\d{13})'
    nationality_pattern = r'([A-Z]+)<<'
    place_of_birth_pattern = r'(?:محل|الولادة)[^:]*:\s*(.*?)\n'
    issuing_authority_pattern_1 = r"مديرية الجنسية والمعلومات المدنية"
    issuing_authority_pattern_2 = r"دائرة احوال -.*?(?=\n|\r|$)"

    try:
        mrz = re.findall(mrz_pattern, back_data.replace(" ","").strip(), re.MULTILINE)
        mrz_str = mrz[0].replace(" ", "")
    except:
        mrz_str = ''
    
    mrz1 = re.search(r'(IDIRQ.*?<<<)', mrz_str, re.DOTALL)
    mrz1 = mrz1.group(1) if mrz1 else None

    mrz2 = re.search(r'\b\d{7}.*?(?:<<\d|<<\n)', mrz_str)
    mrz2 = mrz2.group(0) if mrz2 else None

    mrz3 = re.search(r'[\n](?:[a-zA-Z<]{6,})', mrz_str)
    mrz3 = mrz3.group(0).replace("\n","") if mrz3 else None

    rfid_number = ''
    id_number = ''

    mrz1_data_match = re.search(mrz1_data_pattern, mrz_str)
    if mrz1_data_match:
        rfid_number = mrz1_data_match.group(1)
        id_number = mrz1_data_match.group(2)

    rfid_number = rfid_number.upper()
    id_number = id_number[1:14] 
    
    dob = func_dob(mrz_str)
    if not dob:
        matches = re.findall(r'\d{4}/\d{2}/\d{2}', back_data)
        sorted_dates = sorted(matches)
        dob = sorted_dates[0]
        
    expiry = func_expiry_date(mrz_str)
    if not expiry:
        matches = re.findall(r'\d{4}/\d{2}/\d{2}', back_data)
        sorted_dates = sorted(matches)
        expiry = sorted_dates[-1]
    
    # nationality_matches = re.search(nationality_pattern, mrz[0])
    # if nationality_matches:
    #     nationality = nationality_matches.group(1)
    # else:
    try:
        pattern = r'(?<=[A-Z]\d{7})[A-Z]{3}'
        national = re.search(pattern, back_data)
        if national:
            nationality = national.group()
        else:
            nationality = ''
    except:
        nationality = ''
    
    if len(nationality)>3:
        pattern = r'(?<=[A-Z]\d{7})[A-Z]{3}'
        national = re.search(pattern, back_data)
        if national:
            nationality = national.group()
            
#     issuing_authority_matches = re.findall(issuing_authority_pattern, back_data)
#     if issuing_authority_matches:
#         issuing_authority = issuing_authority_matches[-1][1]
#     else:
#         issuing_authority = ''
    
    issuing_authority_match_1 = re.search(issuing_authority_pattern_1, back_data)
    issuing_authority_match_2 = re.search(issuing_authority_pattern_2, back_data)

    if issuing_authority_match_1:
        issuing_authority = issuing_authority_match_1.group(0)

    if issuing_authority_match_2:
        issuing_authority = issuing_authority_match_2.group(0)
        
    place_of_birth_match = re.search(place_of_birth_pattern, back_data)
    if place_of_birth_match:
        place_of_birth = place_of_birth_match.group(1).strip()
        place_of_birth_list = place_of_birth.split(":")
        if len(place_of_birth_list)>=2:
            place_of_birth = place_of_birth_list[1].strip()
        elif len(place_of_birth_list)==1:
            place_of_birth = place_of_birth_list[0]
        else:
            place_of_birth = ''
    else:
        place_of_birth = ''
    
    if issuing_authority:
        issuing_authority_en = translator.translate(issuing_authority, src='ar', dest='en').text.upper()

    if place_of_birth:
        place_of_birth_en = translator.translate(place_of_birth, src='ar', dest='en').text.upper()

    back_data_dict = {
        "mrz": [mrz_str],
        "mrz1": mrz1,
        "mrz2": mrz2,
        "mrz3": mrz3,
        "id_number": id_number,
        "card_number": rfid_number,
        "dob": dob,
        "expiry_date": expiry,
        "nationality": nationality,
        "issuing_authority": issuing_authority,
        "place_of_birth": place_of_birth,
        "issuing_authority_en": issuing_authority_en,
        "place_of_birth_en": place_of_birth_en,
        "issuing_country": "IRQ"
    }

    non_optional_keys = ["id_number", "card_number", "nationality"]
    empty_string_keys = [key for key, value in back_data_dict.items() if key in non_optional_keys and value == '']

    if empty_string_keys or len(back_data_dict['nationality'])>3 or len(back_data_dict['id_number'])<12:
        back_res = handle_mrz_extraction(image_data, back_id_text)
        back_data_dict.update(back_res)

    return back_data_dict

import re
import traceback

import requests
from bs4 import BeautifulSoup
import pandas as pd
import openpyxl

date_regex = r'Date of the jury decision([0-9/]+)'
winner_name_regex = r'Official name: ([^\n]+)'
winner_website_regex = r'Internet address: ([^\n]+)'
address_regex = r'Postal address: ([^\n]+)'
town_regex = r'Town: ([^\n]+)'
postal_code_regex = r'Postal code: ([^\n]+)'
winner_email_regex = r'E-mail: ([^\n]+)'
buyer_name_regex = r'Official name: ([^\n]+)'
buyer_address_regex = r'Postal address: ([^\n]+)'
buyer_town_regex = r'Town: ([^\n]+)'
description_regex = r'Title ([^\n]+)'


def get_all_tender_numbers(start_date, end_date):
    full_tender_numbers_list = []
    i = 1
    while True:
        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7',
            'content-type': 'application/json',
            # 'cookie': 'GUEST_LANGUAGE_ID=en_GB; COOKIE_SUPPORT=true; cck1=%7B%22cm%22%3Afalse%2C%22all1st%22%3Afalse%2C%22closed%22%3Afalse%7D; route=1720529250.167.31.593787|726825d00aba56cccab96f4e82375684; JSESSIONID=010BE41F58198DBB10546042A91E788D.liferay-prod-1',
            'origin': 'https://ted.europa.eu',
            'priority': 'u=1, i',
            'referer': 'https://ted.europa.eu/',
            'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
        }

        json_data = {
            'query': f'(publication-date >={start_date}<={end_date}) AND (buyer-country IN (FRA)) AND (contract-nature IN (works combined services)) AND (notice-type IN (can-desg)) AND (FT ~ (esquisse, ))  SORT BY publication-number DESC',
            'page': i,
            'limit': 50,
            'fields': [
                'publication-number',
            ],
            'validation': False,
            'scope': 'ALL',
            'language': 'EN',
            'onlyLatestVersions': False,
            'facets': {
                'business-opportunity': [],
                'cpv': [],
                'contract-nature': [],
                'place-of-performance': [],
                'procedure-type': [],
                'publication-date': [],
                'buyer-country': [],
            },
        }

        response = requests.post(
            'https://api.ted.europa.eu/private-search/api/v1/notices/search',
            headers=headers,
            json=json_data,
        )

        part_tender_numbers = [tender_info.get('publication-number') for tender_info in response.json().get('notices')]
        full_tender_numbers_list.extend(part_tender_numbers)
        i += 1
        if len(part_tender_numbers) == 0:
            return full_tender_numbers_list


def get_info(tender_number):
    tender_info = dict()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'uk-UA,uk;q=0.8,en-US;q=0.5,en;q=0.3',
        # 'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Origin': 'https://ted.europa.eu',
        'Connection': 'keep-alive',
        'Referer': 'https://ted.europa.eu/',
        # 'Cookie': 'route=1720529936.665.31.50348^|726825d00aba56cccab96f4e82375684; JSESSIONID=CBE8B416DA2A4228A39CCD1CC36C17F2.liferay-prod-1; GUEST_LANGUAGE_ID=en_GB; COOKIE_SUPPORT=true; cck1=^%^7B^%^22cm^%^22^%^3Afalse^%^2C^%^22all1st^%^22^%^3Afalse^%^2C^%^22closed^%^22^%^3Afalse^%^7D',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
    }

    params = {
        'fields': [
            'family',
            'amended-by',
            'cancelled-by',
            'last-version',
            'extended-by',
            'notice-standard-version',
            'procedure-identifier',
            'main-classification-proc',
            'buyer-country',
            'buyer-profile',
            'translation-languages',
            'notice-type',
        ],
        'language': 'EN',
    }
    while True:
        try:
            response = requests.get(
                f'https://api.ted.europa.eu/viewer/api/v1/render/{tender_number}/html',
                params=params,
                headers=headers,
            )
            if response.status_code == 200:
                break
        except Exception as e:
            print(e)
            traceback.print_exc()

    soup = BeautifulSoup(response.json().get('summary'), 'html.parser')
    info_blocks = soup.find_all('div', class_='sublevel__content')
    tender_info['Link'] = f'https://ted.europa.eu/en/notice/-/detail/{tender_number}'
    for info_block in info_blocks:
        if re.findall(date_regex, info_block.text):
            tender_info['Date'] = re.findall(date_regex, info_block.text)[0]
        if 'Name(s) and address(es) of the winner' in info_block.text:
            winner_address = ''
            if re.findall(winner_name_regex, info_block.text):
                tender_info['Winner name'] = re.findall(winner_name_regex, info_block.text)[0]
            if re.findall(winner_website_regex, info_block.text):
                tender_info['Winner website'] = re.findall(winner_website_regex, info_block.text)[0]
            if re.findall(address_regex, info_block.text):
                winner_address += re.findall(address_regex, info_block.text)[0] + ', '
            if re.findall(postal_code_regex, info_block.text):
                winner_address += re.findall(postal_code_regex, info_block.text)[0] + ', '
            if re.findall(town_regex, info_block.text):
                winner_address += re.findall(town_regex, info_block.text)[0]
            if re.findall(winner_email_regex, info_block.text):
                tender_info['Winner email'] = re.findall(winner_email_regex, info_block.text)[0]
            tender_info['Winner address'] = winner_address
        elif 'Name and addresses' in info_block.text:
            if re.findall(buyer_name_regex, info_block.text):
                tender_info['Buyer name'] = re.findall(buyer_name_regex, info_block.text)[0]
            if re.findall(buyer_address_regex, info_block.text):
                tender_info['Buyer address'] = re.findall(buyer_address_regex, info_block.text)[0]
            if re.findall(buyer_town_regex, info_block.text):
                tender_info['Buyer town'] = re.findall(buyer_town_regex, info_block.text)[0]
        elif 'Title' in info_block.text:
            text = info_block.getText().replace('Title', '').strip()
            output_string = re.sub(r'\n\s*\n', '\n', text.strip(), flags=re.MULTILINE)
            tender_info['Description'] = output_string

    print(tender_info)
    return tender_info


if __name__ == '__main__':
    df = pd.DataFrame(
        columns=['Date', 'Link', 'Winner name', 'Winner website', 'Winner email', 'Winner address', 'Buyer name',
                 'Buyer address', 'Buyer town', 'Description'])
    start_date = input('Enter the starting date in YYYYMMDD format, for example 20230101: ')

    end_date = input('Enter the ending date in YYYYMMDD format, for example 20231230: ')
    tender_list = get_all_tender_numbers(start_date,end_date)
    counter = 0
    for tender_number in tender_list:
        df.loc[counter] = get_info(tender_number)
        counter += 1
    df.to_excel('tenders.xlsx', index=False)


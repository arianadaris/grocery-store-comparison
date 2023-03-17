from flask import Blueprint, request
import requests

from __main__ import db
from Models import *

import os
from dotenv import load_dotenv

api_bp = Blueprint('api', __name__)

load_dotenv()
API_KEY = os.getenv('GEOCODE_API_KEY')
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/zip?zip="

@api_bp.route('/')
def api():
    products_dict = []
    for product in products.query.all():
        products_dict.append(product.as_dict())
    return products_dict

def get_target_tcin(query):
    # Format the query if it contains spaces
    query.replace(' ', '+')
    
    # Format the target search url
    target_search_url = f'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&keyword={query}&offset=0&page=%2Fs%2Forange+juice&platform=mobile&pricing_store_id=2176&scheduled_delivery_store_id=2176&store_ids=2176%2C319%2C950%2C1429%2C1905&useragent=Mozilla%2F5.0+%28Linux%3B+Android+6.0%3B+Nexus+5+Build%2FMRA58N%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Mobile+Safari%2F537.36&visitor_id=0186C9840741020196EB42E2531CC94E&zip=85281'

    headers = {
        'authority': 'redsky.target.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'TealeafAkaSid=lDegaYvo8ZYVdPk0-clYg9N9J2COvA5-; visitorId=0186C9840741020196EB42E2531CC94E; sapphire=1; UserLocation=85281|33.420|-111.900|AZ|US; fiatsCookie=DSI_2176|DSN_Tempe%20Rio%20Salado|DSZ_85281; ci_pixmgr=other; _gcl_au=1.1.667510199.1678418123; __gads=ID=e245fe494d8f5fe9:T=1678991026:S=ALNI_MZ8zSSyD5YoaufivLIEPl8Gg6YMaQ; __gpi=UID=0000057982251a3b:T=1678991026:RT=1678991026:S=ALNI_Mbw_msBe5rJaADVCsJVZb7YKaKiMA; egsSessionId=9f409330-77d1-47d3-a2fb-094e64131175; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIzZjk3MDM1MS0xNzVlLTQyNWQtOWVhYS0yOTM2YWU2ZjZiZDUiLCJpc3MiOiJNSTYiLCJleHAiOjE2NzkwNzc0MjcsImlhdCI6MTY3ODk5MTAyNywianRpIjoiVEdULjlkZWQ4OTkxYzVmYzQ5MmRhNGM0NTQ4MjU5MzA1YWEwLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImVkMGJiYTBmMjgwN2I4ZGQ5N2RmOTE0MGEwOWZhMDNhMjJiOWI4NDZkZGRiMTVlMzgxZjBlMGFiZDRkN2Q1YjgiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.Q1dwVD3EEJl2KE2z7vSMCFzh25lAB_mYXt_6wnEsTxkTSpM3GHEaZotZ9yYPbPAjTB-1N2KAsVt3PUwTUxe8fyqs-d0p2PGQIgzwREF2ZtZElJEegLzJREh0vDde_PVSyHUY8glIG7woXmevy3zYuQ8Px8cE5k52RZeNswVTwB4QuhqyIBu0YwTpKQ7nMoKK9bD4wX8_9htN9C_p7rH_nUgAcQjY3R55Bg-4O3DzUlsNyeshc-4pjJFwL_rE6rCpswDis0ExG2Tmu6P-wUZfxjg0X-vxSqzztbZ0UFxeEZHw4-4ebbIdmEgMSAS4hAfl04Gs-wfjWq6JEgnMfbGHFQ; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiIzZjk3MDM1MS0xNzVlLTQyNWQtOWVhYS0yOTM2YWU2ZjZiZDUiLCJpc3MiOiJNSTYiLCJleHAiOjE2NzkwNzc0MjcsImlhdCI6MTY3ODk5MTAyNywiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=iu619O1eA7JCUgv7cw7lTILxxQz2T384YApRrUKUq-UerjM0dU8QmI_6kuwwmw4CG5wq6Ctp_HGWkKToUOMg2Q; crl8.fpcuid=4cde25ca-c896-4798-9858-8079e2e3494e; ffsession={%22sessionHash%22:%22116a8e84765621678991026274%22%2C%22prevPageName%22:%22grocery%22%2C%22prevPageType%22:%22level%201%22%2C%22prevPageUrl%22:%22https://www.target.com/c/grocery/-/N-5xt1a%22%2C%22sessionHit%22:13%2C%22prevSearchTerm%22:%22non-search%22}; _uetsid=b19c4420c42711ed9092034fed300ced; _uetvid=ed2832604b8711ed85a34b6171d92abd; _mitata=Zjc3OTA3OTdkNjA4NGQ3NmJiMTYzMTY4YzY5YzFlNjQ2MDg1Y2RjN2RjZDhiYzNmMGI1ZGYzOTQwZjg2ZjA5OQ==_/@#/1678991745_/@#/cOberPSY7QsR6ANE_/@#/YWFjNGNjMzJlZTA2OTQ0ZGNhNTE3ZGE1MmNmZjVjZDM0ZjRhZWY5NzdkYTlmMmYxMjQyODk4YjYzZDU4YTc4Zg==_/@#/000; TealeafAkaSid=t5LsNrklzcx-xXZenujtjgDUIA-uwamI; sapphire=1; visitorId=0186EBB5A42A0201BBA85649C0D3D985; _mitata=ZmFlOTE1NzM4YTViZWYxNzUwNmZmM2E4ZWE3MWIxMGE1MTM0MWQyOWIwODEzOTk2OWVjZDRlYzgxZDY1MDg5MA==_/@#/1678991967_/@#/cOberPSY7QsR6ANE_/@#/YjBkMzY5NDQ2Zjg0MzFiMDBhZjdkZGI1YjU4M2UzYzYxZDhjZGNmYWU3MGVhZGZjMzc1OTQ4ZTc2NjE4ZGMyYw==_/@#/000',
        'origin': 'https://www.target.com',
        'referer': 'https://www.target.com/s?searchTerm=orange+juice',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Mobile Safari/537.36'
    }
    try:
        # Get Target search results
        r = requests.request("GET", target_search_url, headers=headers, data={})
        target_products = r.json()["data"]["search"]["products"]

        
        for product in target_products:
            # Get product name and format
            name = product["item"]["product_description"]["title"]

            delimiters = [
                "&#38",
                "&#8482;"
            ]
            
            for delim in delimiters:
                name = name.replace(delim, '')

            name = name.replace(';', '&')
            
            # If product name contains size
            if " - " in name:
                # Split name into list of strings based on space
                name = name.split(' ')
                print(name)

                # Find first individual dash
                indexDash1 = name.index("-") # after removing the first dash, indexDash1 will refer to the position of the number
                name.remove("-")

                # Check if there is still another dash
                indexDash2 = len(name)-1
                if "-" in name:
                    indexDash2 = name.index("-") - 1 # indexDash2 refers to the element right before the second dash
                    name.remove("-")

                weight = ' '.join(name[indexDash1:indexDash2])
                name = ' '.join(name[0:indexDash1] + name[indexDash2:])

            # Get product tcin
            tcin = product["tcin"]

            # Format keyword
            keyword = query.replace('+', ' ')

            # Create product object
            product = products(name, keyword, weight, tcin)

            db.session.add(product)
            db.session.commit()

        return True
    except Exception as e:
        print(e)
        return False


# Helper function
# Get coordinates from zipcode input
def getCoords(zipCode):
    request_url = f'{GEOCODE_URL}{zipCode}&limit=1&appid={API_KEY}'
    r = requests.request("GET", request_url, headers={}, data={})
    zip_data = r.json()

    coords = {
        'name': zip_data['name'],
        'longitude': zip_data['lon'],
        'latitude': zip_data['lat'],
    }

    return coords

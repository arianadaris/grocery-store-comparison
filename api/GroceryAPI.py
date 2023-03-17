from flask import Blueprint, request
import requests
import json

from __main__ import db
from Models import *

import os
from dotenv import load_dotenv

api_bp = Blueprint('api', __name__)

load_dotenv()
GEOCODE_API_KEY = os.getenv('GEOCODE_API_KEY')
GEOCODE_URL = "http://api.openweathermap.org/geo/1.0/zip?zip="

"""
URL - /api/
    Returns - dictionary
"""
@api_bp.route('/', methods=['GET'])
def get_api():
    return 'api :)'

#
# ZIPCODE FUNCTIONS
#

"""
URL - /api/coords/12345
    Parameters - zipcode: int - 5 digit zipcode
    Returns - dictionary containing the location, latitude, longitude near that zipcode
"""
@api_bp.route('/coords/<int:zipcode>')
def get_coords(zipcode):
    request_url = f'{GEOCODE_URL}{zipcode}&limit=1&appid={GEOCODE_API_KEY}'
    r = requests.request("GET", request_url, headers={}, data={})
    zip_data = r.json()

    coords = {
        'name': zip_data['name'],
        'longitude': zip_data['lon'],
        'latitude': zip_data['lat'],
        'zipcode': zipcode
    } 

    return coords   

#
# PRODUCT FUNCTIONS
#

"""
URL - /api/products
    Returns - dictionary containing all of the products in the products table
"""
@api_bp.route('/products', methods=['GET'])
def get_products():
    products_dict = []
    for product in products.query.all():
        products_dict.append(product.as_dict())
    return products_dict

"""
URL - /api/products/1
    Returns - dictionary containing the product with the inputted ID
"""
@api_bp.route('/products/<int:id>')
def get_product(id):
    product = products.query.get_or_404(id)
    return product.as_dict()

"""
URL - /api/products/delete
    Deletes all products in the products table
    Returns - dictionary containing a success value and optional error string
"""
@api_bp.route('/products/delete')
def delete_all():
    try:
        db.session.query(products).delete()
        db.session.commit()
        return {
            'success': 'True',
            'error': 'N/A'
        }
    except Exception as e:
        db.session.rollback()
        return {
            'success': 'False',
            'error': str(e)
        }

"""
URL - /api/products/delete/1
    Deletes the product with the inputted ID from the products table
    Returns - dictionary containing a success value and optional error string
"""
@api_bp.route('/products/delete/<int:id>')
def delete_product(id):
    product = products.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return {
            'success': 'True',
            'error': 'N/A'
        }
    except Exception as e:
        return {
            'success': 'False',
            'error': str(e)
        }

"""
URL - /api/products/search/orange+juice
    Given a query string, it searches the query through Target and retrieves all products related to that query string.
    For each product retrieved, it formats the product into the Product model and adds it to the products table.
    Parameters - query: string - used for specifying the product search
    Returns - dictionary containing a success value and optional error string
"""
# Defines a route search that allows the user to search and add Products to the database based on a general search query
# EX. keyword = orange juice
@api_bp.route('/products/search/q=<query>')
def add_products(query):
    # Format keyword
    keyword = query.replace('+', ' ')

    def add_products_from_target():
        try:
            # Get target search url and headers
            target = get_target_search_url(query)
            target_url = target[0]
            target_headers = target[1]
            
            # Get Target search results
            r = requests.request("GET", target_url, headers=target_headers, data={})
            target_products = r.json()['data']['search']['products']

            for product in target_products:
                # Get product name and format
                name = product["item"]["product_description"]["title"]
                delimiters = [
                    "&#38",
                    "&#8482;",
                    "&#39&"
                ]
                for delim in delimiters:
                    name = name.replace(delim, '')
                name = name.replace(';', '&')
                # If product name contains size
                if " - " in name:
                    # Split name into list of strings based on space
                    name = name.split(' ')

                    # Find first individual dash
                    indexDash1 = name.index("-") # after removing the first dash, indexDash1 will refer to the position of the number
                    name.remove("-")

                    # Check if there is still another dash
                    indexDash2 = len(name)
                    if "-" in name:
                        indexDash2 = name.index("-") # indexDash2 refers to the element right before the second dash
                        name.remove("-")

                    weight = ' '.join(name[indexDash1:indexDash2])
                    name = ' '.join(name[0:indexDash1] + name[indexDash2:])

                # Get product details
                tcin = product["tcin"]
                image = product['item']['enrichment']['images']['primary_image_url']

                # Create product object
                new_product = products(name, image, keyword, weight)
                new_product.set_target_tcin(tcin)

                db.session.add(new_product)
                db.session.commit()
        except Exception as e:
            return {
                'success': 'False',
                'error': 'Target: ' + str(e)
            }

    def add_products_from_traderjoes():
        try:
            # Get trader joes search url, headers, and payload
            traderjoes = get_traderjoes_search_url(query)

            # Get Trader Joes search results
            r = requests.request('POST', traderjoes[0], headers=traderjoes[1], data=traderjoes[2])

            traderjoes_products = r.json()['data']['products']['items']

            for product in traderjoes_products:
                # Get product details
                name = product['item_title']
                sku = product['sku']
                image = product['primary_image']
                
                # Get weight
                weight_num = product['sales_size']
                weight_measure = product['sales_uom_description']
                weight = f'{weight_num} {weight_measure}'

                # Create product object
                new_product = products(name, image, keyword, weight)
                new_product.set_traderjoes_sku(sku)

                db.session.add(new_product)
                db.session.commit()
        except Exception as e:
            print(f'\n\n\nTraderJoes Error: {str(e)}\n\n\n')
            return {
                'success': 'False',
                'error': 'Trader Joes: ' + str(e)
            }

    add_products_from_target()
    add_products_from_traderjoes()

    return {
        'success': 'True',
        'error': 'N/A'
    }


#
# PRICE RETRIEVAL FUNCTIONS
#

"""
URL - /api/prices/id=1&lat=12.34&lon=12.45&zip=85201
    Given a product id, it retrieves the product's price from all appropriate stores
    Parameters -
        product_id: int - product identification number
        lat: string - latitude
        lon: string - longitude
        zipcode: string - 5 digit zipcode number
    Returns - dictionary containing product information and prices for various stores
"""
@api_bp.route('/prices/id=<int:product_id>&lat=<lat>&lon=<lon>&zip=<zipcode>')
def get_price(product_id, lat, lon, zipcode):
    product = products.query.get_or_404(product_id)

    def get_target_price(tcin):
        # Get Target store ID based on zipcode
        storeID_url = f'https://redsky.target.com/redsky_aggregations/v1/web_platform/nearby_stores_v1?limit=1&within=100&place={zipcode}&key=8df66ea1e1fc070a6ea99e942431c9cd67a80f02&channel=WEB&page=%2Fs%2F'

        r = requests.request('GET', storeID_url, headers={}, data={})

        storeID = r.json()['data']['nearby_stores']['stores'][0]['store_id']

        # Get the product's price by searching for the product on Target's website
        target = get_target_price_url(tcin, storeID)

        try:
            r = requests.request('GET', target[0], headers=target[1], data={})

            target_price_data = r.json()

            # Parse price from target
            target_price = target_price_data['data']['product']['price']['formatted_current_price']
            return target_price
        except Exception as e:
            print('Target Price Error: ' + str(e))

    def get_traderjoes_price(sku):
        # Get the product's price by searching for the product on Trader Joe's website
        traderjoes = get_traderjoes_price_url(sku)

        try:
            r = requests.request('POST', traderjoes[0], headers=traderjoes[1], data=traderjoes[2])
            traderjoes_price_data = r.json()['data']['products']['items']

            # Parse price from trader joes
            traderjoes_price = traderjoes_price_data[0]['retail_price']

            return traderjoes_price
        except Exception as e:
            print('Trader Joes Price Error: ' + str(e))
    
    if product.target_tcin != 0:
        target_price = get_target_price(product.target_tcin)
    if product.traderjoes_sku != 0:
        traderjoes_price = get_traderjoes_price(product.traderjoes_sku)

    prices = {
        'name': product.name,
        'image': product.image,
        'id': product_id,
        'target_price': target_price if target_price != None else 'N/A',
        'traderjoes_price': traderjoes_price if traderjoes_price != None else 'N/A'
    }

    return prices


#
# API HELPER FUNCTIONS
#

"""
    Getter function used for formatting the target query url and retrieving the appropriate headers
    Parameters - query: string - used for specifying the product search
    Returns - list (length 2)-
        list[0] - contains the formatted target URL string
        list[1] - contains the target headers dictionary
"""
def get_target_search_url(query):
    target_search_url = f'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&keyword={query}&offset=0&page=%2Fs%2F{query}&platform=mobile&pricing_store_id=2176&scheduled_delivery_store_id=2176&store_ids=2176%2C319%2C950%2C1429%2C1905&useragent=Mozilla%2F5.0+%28Linux%3B+Android+6.0%3B+Nexus+5+Build%2FMRA58N%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Mobile+Safari%2F537.36&visitor_id=0186C9840741020196EB42E2531CC94E&zip=85281'

    target_headers = {
        'authority': 'redsky.target.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'TealeafAkaSid=LpZdmzjbHlKiarchtElASxEpG9_4zFuj; visitorId=0186DC431E3C02018F5C06CF78CED296; sapphire=1; UserLocation=85287|33.430|-111.930|AZ|US; __gads=ID=120f7a5f2b5ab553:T=1678732634:S=ALNI_Ma6Fq-UViOJPGJJJIAsqKBPGAAY8A; ci_pixmgr=other; _gcl_au=1.1.1294459899.1678732636; fiatsCookie=DSI_2176|DSN_Tempe%20Rio%20Salado|DSZ_85281; 3YCzT93n=A0CHRdyGAQAA5GA1FaU6DNITRuGuT8xXEm8qhUTut-gRn4ZBK2nFfwBF7_6sAYHbCHKucuFZwH9eCOfvosJeCA|1|1|7db79e8eb748cf56ba796f1cb0ad5eccd543eb84; egsSessionId=8f4fe2d1-846c-43ce-8ba5-7c98626a73d3; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI1OTg1NjA2Ni1lNjg5LTRlNTMtODZjNC01YzYwMmU3MWUyOWUiLCJpc3MiOiJNSTYiLCJleHAiOjE2NzkxNjc0MTksImlhdCI6MTY3OTA4MTAxOSwianRpIjoiVEdULmY0YTI3NTBiOTkxODRkZDY5YWVkZmUxOGQxMTRlNzUwLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImUwMTc5NjY4ZGJkYjJiMzk4YzlmNzgyMDExNzA2ODNkNmIwMjhmZjEyMGQ2MWZlZTllMTdmZjgxZDk4NmYwNjYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.ZL-yDtnt6dYw36h2aLDU0N5OFpeFwQDVkdV4iR8Af0K2YIHApvrUIH2OeKWGzizy7EsnnwEsCu3lHvlpLbJpzF5HNidmNSOoPpSTb_zq4BXngluxQYZRpb0gxGz4ZKZoaA5zTgbjHtC-GwYUvwiNgwOkC1zEO9UyRW4kKl991Rb1drjuej9dZbXii_j6PIgQbldVlsaMzSujhlub7IR9hucw--tqU_ZqDZVtrogoUby2w9QoMgw5oncRSJAQulz3wyQ-gmbwNDoQnVFOV20UR3DcFMscXKodrTvw942dCvHkq1fJXCQly7Gz1reAptncYpMCUTZgfvc3rHe2-cVDiQ; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiI1OTg1NjA2Ni1lNjg5LTRlNTMtODZjNC01YzYwMmU3MWUyOWUiLCJpc3MiOiJNSTYiLCJleHAiOjE2NzkxNjc0MTksImlhdCI6MTY3OTA4MTAxOSwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=FA2cK4QZERCa4glb8QNtX2FBdPxPE7KBZvfwE-eqA5yHLqj6soe_ny5NbPKFzLyPRCq1m9LcZL5pw3LrHqHvKg; __gpi=UID=0000095e2f068964:T=1678732634:RT=1679081020:S=ALNI_MaECc4Qi0ArYNn9pTKXs6jHD4P0yQ; _mitata=NzdhNWMyM2RkMTgyZTExMDg1OTk2ZmJmZjY1MjcxNTI5Njg3NzkxZGYwM2Q4Yzk3N2EzNDY1NjRjMWNhMTVmYQ==_/@#/1679081082_/@#/cgYqer8FiS6bofbc_/@#/N2Y3ZDBlOGRhYzNhMTE2NWUzNTFmZjE0NmVlYjMxMGQzZGY5NTFiZDBlMWNmMGUxNjhiMjA0OGUyODQ1OWFkNA==_/@#/000; crl8.fpcuid=bb1a7b80-05dc-4e85-828b-a5a4d6e0c242; _uetsid=3a938d80c4f911edb6faa3cc1d09158a; _uetvid=9285ba10288c11ed98bdf7f69ea87e59',
        'origin': 'https://www.target.com',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    return [
        target_search_url,
        target_headers
    ]

"""

"""
def get_target_price_url(tcin, storeID):
    # Format product tcin and storeID in Target product URL
    product_url = f'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin={tcin}&is_bot=false&member_id=0&pricing_store_id={storeID}&has_pricing_store_id=true&scheduled_delivery_store_id={storeID}&has_financing_options=true&visitor_id=0186DC431E3C02018F5C06CF78CED296&has_size_context=true&skip_personalized=false&channel=WEB&page=%2Fp%2FA-83880304'

    product_headers = {
        'authority': 'redsky.target.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': 'TealeafAkaSid=LpZdmzjbHlKiarchtElASxEpG9_4zFuj; visitorId=0186DC431E3C02018F5C06CF78CED296; sapphire=1; UserLocation=85287|33.430|-111.930|AZ|US; __gads=ID=120f7a5f2b5ab553:T=1678732634:S=ALNI_Ma6Fq-UViOJPGJJJIAsqKBPGAAY8A; ci_pixmgr=other; _gcl_au=1.1.1294459899.1678732636; fiatsCookie=DSI_2176|DSN_Tempe%20Rio%20Salado|DSZ_85281; 3YCzT93n=A0CHRdyGAQAA5GA1FaU6DNITRuGuT8xXEm8qhUTut-gRn4ZBK2nFfwBF7_6sAYHbCHKucuFZwH9eCOfvosJeCA|1|1|7db79e8eb748cf56ba796f1cb0ad5eccd543eb84; egsSessionId=8f4fe2d1-846c-43ce-8ba5-7c98626a73d3; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI1OTg1NjA2Ni1lNjg5LTRlNTMtODZjNC01YzYwMmU3MWUyOWUiLCJpc3MiOiJNSTYiLCJleHAiOjE2NzkxNjc0MTksImlhdCI6MTY3OTA4MTAxOSwianRpIjoiVEdULmY0YTI3NTBiOTkxODRkZDY5YWVkZmUxOGQxMTRlNzUwLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImUwMTc5NjY4ZGJkYjJiMzk4YzlmNzgyMDExNzA2ODNkNmIwMjhmZjEyMGQ2MWZlZTllMTdmZjgxZDk4NmYwNjYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.ZL-yDtnt6dYw36h2aLDU0N5OFpeFwQDVkdV4iR8Af0K2YIHApvrUIH2OeKWGzizy7EsnnwEsCu3lHvlpLbJpzF5HNidmNSOoPpSTb_zq4BXngluxQYZRpb0gxGz4ZKZoaA5zTgbjHtC-GwYUvwiNgwOkC1zEO9UyRW4kKl991Rb1drjuej9dZbXii_j6PIgQbldVlsaMzSujhlub7IR9hucw--tqU_ZqDZVtrogoUby2w9QoMgw5oncRSJAQulz3wyQ-gmbwNDoQnVFOV20UR3DcFMscXKodrTvw942dCvHkq1fJXCQly7Gz1reAptncYpMCUTZgfvc3rHe2-cVDiQ; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiI1OTg1NjA2Ni1lNjg5LTRlNTMtODZjNC01YzYwMmU3MWUyOWUiLCJpc3MiOiJNSTYiLCJleHAiOjE2NzkxNjc0MTksImlhdCI6MTY3OTA4MTAxOSwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=FA2cK4QZERCa4glb8QNtX2FBdPxPE7KBZvfwE-eqA5yHLqj6soe_ny5NbPKFzLyPRCq1m9LcZL5pw3LrHqHvKg; __gpi=UID=0000095e2f068964:T=1678732634:RT=1679081020:S=ALNI_MaECc4Qi0ArYNn9pTKXs6jHD4P0yQ; _mitata=NzdhNWMyM2RkMTgyZTExMDg1OTk2ZmJmZjY1MjcxNTI5Njg3NzkxZGYwM2Q4Yzk3N2EzNDY1NjRjMWNhMTVmYQ==_/@#/1679081082_/@#/cgYqer8FiS6bofbc_/@#/N2Y3ZDBlOGRhYzNhMTE2NWUzNTFmZjE0NmVlYjMxMGQzZGY5NTFiZDBlMWNmMGUxNjhiMjA0OGUyODQ1OWFkNA==_/@#/000; crl8.fpcuid=bb1a7b80-05dc-4e85-828b-a5a4d6e0c242; ffsession={%22sessionHash%22:%22fcae812a6964e1678732633039%22%2C%22prevPageName%22:%22grocery:%20product%20detail%22%2C%22prevPageType%22:%22product%20details%22%2C%22prevPageUrl%22:%22https://www.target.com/p/tropicana-pure-premium-no-pulp-calcium-vitamin-d-orange-juice-89-fl-oz/-/A-13193658#lnk=sametab%22%2C%22sessionHit%22:14%2C%22prevSearchTerm%22:%22orange%20juice%22}; _uetsid=3a938d80c4f911edb6faa3cc1d09158a; _uetvid=9285ba10288c11ed98bdf7f69ea87e59',
        'origin': 'https://www.target.com',
        'referer': 'https://www.target.com/p/tropicana-pure-premium-no-pulp-calcium-vitamin-d-orange-juice-89-fl-oz/-/A-13193658',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    return [
        product_url,
        product_headers
    ]

"""

"""
def get_traderjoes_search_url(query):
    traderjoes_search_url = "https://www.traderjoes.com/api/graphql"

    search = query.replace('+', ' ')
    traderjoes_payload = json.dumps({
        "operationName": "SearchProducts",
        "variables": {
            "storeCode": "91",
            "availability": "1",
            "published": "1",
            "search": search,
            "currentPage": 1,
            "pageSize": 15
        },
        "query": "query SearchProducts($search: String, $pageSize: Int, $currentPage: Int, $storeCode: String = \"91\", $availability: String = \"1\", $published: String = \"1\") {\n  products(\n    search: $search\n    filter: {store_code: {eq: $storeCode}, published: {eq: $published}, availability: {match: $availability}}\n    pageSize: $pageSize\n    currentPage: $currentPage\n  ) {\n    items {\n      category_hierarchy {\n        id\n        url_key\n        description\n        name\n        position\n        level\n        created_at\n        updated_at\n        product_count\n        __typename\n      }\n      item_story_marketing\n      product_label\n      fun_tags\n      primary_image\n      primary_image_meta {\n        url\n        metadata\n        __typename\n      }\n      other_images\n      other_images_meta {\n        url\n        metadata\n        __typename\n      }\n      context_image\n      context_image_meta {\n        url\n        metadata\n        __typename\n      }\n      published\n      sku\n      url_key\n      name\n      item_description\n      item_title\n      item_characteristics\n      item_story_qil\n      use_and_demo\n      sales_size\n      sales_uom_code\n      sales_uom_description\n      country_of_origin\n      availability\n      new_product\n      promotion\n      price_range {\n        minimum_price {\n          final_price {\n            currency\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      retail_price\n      nutrition {\n        display_sequence\n        panel_id\n        panel_title\n        serving_size\n        calories_per_serving\n        servings_per_container\n        details {\n          display_seq\n          nutritional_item\n          amount\n          percent_dv\n          __typename\n        }\n        __typename\n      }\n      ingredients {\n        display_sequence\n        ingredient\n        __typename\n      }\n      allergens {\n        display_sequence\n        ingredient\n        __typename\n      }\n      created_at\n      first_published_date\n      last_published_date\n      updated_at\n      related_products {\n        sku\n        item_title\n        primary_image\n        primary_image_meta {\n          url\n          metadata\n          __typename\n        }\n        price_range {\n          minimum_price {\n            final_price {\n              currency\n              value\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        retail_price\n        sales_size\n        sales_uom_description\n        category_hierarchy {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    total_count\n    page_info {\n      current_page\n      page_size\n      total_pages\n      __typename\n    }\n    __typename\n  }\n}\n"
    })

    traderjoes_headers = {
    'authority': 'www.traderjoes.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': 'affinity="df4886cec282cfe9"; AMCVS_B5B4708F5F4CE8D80A495ED9%40AdobeOrg=1; s_cc=true; _gid=GA1.2.1134831241.1679088538; _ga=GA1.2.163748476.1676671506; _ga_PVSN19270R=GS1.1.1679088537.1.1.1679088552.45.0.0; AMCV_B5B4708F5F4CE8D80A495ED9%40AdobeOrg=-2121179033%7CMCIDTS%7C19434%7CMCMID%7C57315252713871509590103316776093705003%7CMCAAMLH-1679693353%7C9%7CMCAAMB-1679693353%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1679095753s%7CNONE%7CvVersion%7C5.3.0; s_vncm=1680332399452%26vn%3D1; s_ivc=true; s_lv_s=More%20than%207%20days; s_visit=1; s_dur=1679088553460; s_inv=2416761;  _gat_UA-15671700-1=1; s_ips=1080; s_tp=1080; s_sq=%5B%5BB%5D%5D; s_nr30=1679089191277-Repeat; s_lv=1679089191278; s_ppv=www.traderjoes.com%257Chome%257Csearch%2C100%2C100%2C1080%2C1%2C1; s_tslv=1679089191281; s_ptc=%5B%5BB%5D%5D; s_pvs=%5B%5BB%5D%5D; s_tps=%5B%5BB%5D%5D; affinity="ee8cf7d1b67e17e0"',
        'origin': 'https://www.traderjoes.com',
        'referer': f'https://www.traderjoes.com/home/search?q={query}&section=products&global=no',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    return [
        traderjoes_search_url,
        traderjoes_headers,
        traderjoes_payload
    ]

"""

"""
def get_traderjoes_price_url(sku):
    product_url = "https://www.traderjoes.com/api/graphql"

    product_headers = {
        'authority': 'www.traderjoes.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': 'affinity="df4886cec282cfe9"; AMCVS_B5B4708F5F4CE8D80A495ED9%40AdobeOrg=1; s_cc=true; _gid=GA1.2.1134831241.1679088538; _ga=GA1.2.163748476.1676671506; _ga_PVSN19270R=GS1.1.1679088537.1.1.1679088552.45.0.0; AMCV_B5B4708F5F4CE8D80A495ED9%40AdobeOrg=-2121179033%7CMCIDTS%7C19434%7CMCMID%7C57315252713871509590103316776093705003%7CMCAAMLH-1679693353%7C9%7CMCAAMB-1679693353%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1679095753s%7CNONE%7CvVersion%7C5.3.0; s_vncm=1680332399452%26vn%3D2; s_ivc=true; s_lv_s=Less%20than%201%20day; s_visit=1; s_dur=1679091830375; s_inv=2639; gpv_c51=https%3A%2F%2Fwww.traderjoes.com%2Fhome%2Fproducts%2Fpdp%2F100-orange-juice-no-pulp-066569; _gat_UA-15671700-1=1; s_nr30=1679092385374-Repeat; s_lv=1679092385376; s_ips=1080; s_tp=1080; s_tslv=1679092385381; s_ptc=%5B%5BB%5D%5D; s_pvs=%5B%5BB%5D%5D; s_tps=%5B%5BB%5D%5D; s_sq=%5B%5BB%5D%5D; affinity="ee8cf7d1b67e17e0"',
        'origin': 'https://www.traderjoes.com',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    product_payload = json.dumps({
        "operationName": "SearchProduct",
        "variables": {
            "storeCode": "91",
            "published": "1",
            "sku": sku
        },
        "query": "query SearchProduct($sku: String, $storeCode: String = \"91\", $published: String = \"1\") {\n  products(\n    filter: {sku: {eq: $sku}, store_code: {eq: $storeCode}, published: {eq: $published}}\n  ) {\n    items {\n      category_hierarchy {\n        id\n        url_key\n        description\n        name\n        position\n        level\n        created_at\n        updated_at\n        product_count\n        __typename\n      }\n      item_story_marketing\n      product_label\n      fun_tags\n      primary_image\n      primary_image_meta {\n        url\n        metadata\n        __typename\n      }\n      other_images\n      other_images_meta {\n        url\n        metadata\n        __typename\n      }\n      context_image\n      context_image_meta {\n        url\n        metadata\n        __typename\n      }\n      published\n      sku\n      url_key\n      name\n      item_description\n      item_title\n      item_characteristics\n      item_story_qil\n      use_and_demo\n      sales_size\n      sales_uom_code\n      sales_uom_description\n      country_of_origin\n      availability\n      new_product\n      promotion\n      price_range {\n        minimum_price {\n          final_price {\n            currency\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      retail_price\n      nutrition {\n        display_sequence\n        panel_id\n        panel_title\n        serving_size\n        calories_per_serving\n        servings_per_container\n        details {\n          display_seq\n          nutritional_item\n          amount\n          percent_dv\n          __typename\n        }\n        __typename\n      }\n      ingredients {\n        display_sequence\n        ingredient\n        __typename\n      }\n      allergens {\n        display_sequence\n        ingredient\n        __typename\n      }\n      created_at\n      first_published_date\n      last_published_date\n      updated_at\n      related_products {\n        sku\n        item_title\n        primary_image\n        primary_image_meta {\n          url\n          metadata\n          __typename\n        }\n        price_range {\n          minimum_price {\n            final_price {\n              currency\n              value\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        retail_price\n        sales_size\n        sales_uom_description\n        category_hierarchy {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    total_count\n    page_info {\n      current_page\n      page_size\n      total_pages\n      __typename\n    }\n    __typename\n  }\n}\n"
    })

    return [
        product_url,
        product_headers,
        product_payload
    ]
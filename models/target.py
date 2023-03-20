import requests

class Target:
    def __init__(self):
        self.cookie = 'TealeafAkaSid=lDegaYvo8ZYVdPk0-clYg9N9J2COvA5-; visitorId=0186C9840741020196EB42E2531CC94E; sapphire=1; UserLocation=85281|33.420|-111.900|AZ|US; fiatsCookie=DSI_2176|DSN_Tempe%20Rio%20Salado|DSZ_85281; ci_pixmgr=other; _gcl_au=1.1.667510199.1678418123; __gads=ID=e245fe494d8f5fe9:T=1678991026:S=ALNI_MZ8zSSyD5YoaufivLIEPl8Gg6YMaQ; crl8.fpcuid=4cde25ca-c896-4798-9858-8079e2e3494e; _ga=GA1.2.40211601.1678998013; egsSessionId=d0f6c929-f275-44e3-a579-c9ed29af7790; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiIzZjk3MDM1MS0xNzVlLTQyNWQtOWVhYS0yOTM2YWU2ZjZiZDUiLCJpc3MiOiJNSTYiLCJleHAiOjE2NzkzMzYxMjUsImlhdCI6MTY3OTI0OTcyNSwianRpIjoiVEdULmNiODI4YmIxOWRiMjQ2NmVhZDgzYmMwNzAzN2IzYjYyLWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImVkMGJiYTBmMjgwN2I4ZGQ5N2RmOTE0MGEwOWZhMDNhMjJiOWI4NDZkZGRiMTVlMzgxZjBlMGFiZDRkN2Q1YjgiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.b3DFrcr2rGOgGdC2rLomcIO7paFOFupzIfNyVQqUfAFKIhkqDIXO1KvmXhEfd62iPNvFwjUwJ7AxoYiD4hoSJJtXlaFo3v3CRIKxPwZE-1I5mQ5gEYodFJp2N5NVtwAYNCOB3RpaDhRpdaMyQ13RzyXrkV1fXhuehZpYoGZHu_Mp15zpOuSI6Tmm4AE7nXOb7ruRroAfHLXN-kGOECVYQP7SDKAAZkAyln1OLg06d3jHVgopCj9XNDgZ-Ix7iM5AsHyLs0dt_ElOZWBnaHUyZJfx7pYaZ8xv-hm6u42h3P0y-XyvZFUYipmpCrVYLXmFoexu9tJl4Y2e_6XUiCGAqw; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiIzZjk3MDM1MS0xNzVlLTQyNWQtOWVhYS0yOTM2YWU2ZjZiZDUiLCJpc3MiOiJNSTYiLCJleHAiOjE2NzkzMzYxMjUsImlhdCI6MTY3OTI0OTcyNSwiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=XTZDJf6ZwkhzhwBZIamnAuAyav-qJZcPcOalARVlizdnwAX8ghxH-fbNiNs7Ewyv4OEOMT1GiwIH17_UlcpCbg; __gpi=UID=0000057982251a3b:T=1678991026:RT=1679249725:S=ALNI_Mbw_msBe5rJaADVCsJVZb7YKaKiMA; _mitata=YTZmZDY4ZWU5OGIzMDg4ODg1ZjliNGI2YmY2MDc0MmVmNzcxYjE2NjE1OGI1NjRkZTE4NTVhMWM4Yzk0NTkwMg==_/@#/1679249786_/@#/cKnWewNfrYl4PVz3_/@#/ZjUyODJmOTk4ZjY5MDVjNzBiNDIxMzk2YWM5ZDk0NzdkNzQ0N2JmMjhiMTE1YWQ3MTViZDM3OTE4NzgyNDM5Yg==_/@#/000; ffsession={%22sessionHash%22:%221c550e00e921c81679249724840%22%2C%22prevPageName%22:%22grocery:%20product%20detail%22%2C%22prevPageType%22:%22product%20details%22%2C%22prevPageUrl%22:%22https://www.target.com/p/tropicana-pure-premium-no-pulp-calcium-vitamin-d-orange-juice-89-fl-oz/-/A-13193658#lnk=sametab%22%2C%22sessionHit%22:3%2C%22prevSearchTerm%22:%22orange%20juice%22}; _uetsid=062641b0c68211edb48b0f80a9c15cf5; _uetvid=ed2832604b8711ed85a34b6171d92abd'

        self.query_headers = {
        'authority': 'redsky.target.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': self.cookie,
        'origin': 'https://www.target.com',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

        self.price_headers = {
        'authority': 'redsky.target.com',
        'accept': 'application/json',
        'accept-language': 'en-US,en;q=0.9',
        'cookie': self.cookie,
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

    def get_products(self, query):
        # Return a list of products
        products = []

        # Format and make a request to retrieve product data from Target
        target = self.get_query_url(query)
        
        # Get Target search results
        r = requests.request("GET", target["query_url"], headers=target["query_headers"], data={})
        resp = r.json()

        try:
            query_products = r.json()['data']['search']['products']

            for product in query_products:
                # Get product details
                tcin = product["tcin"]
                image = product["item"]["enrichment"]["images"]["primary_image_url"]
                temp_name = product["item"]["product_description"]["title"]
                result = self.format_name(temp_name)
                name = result["name"]
                weight = result["weight"]
                keyword = query.replace("+", ' ')

                products.append({
                    'name': name,
                    'image': image,
                    'keyword': keyword,
                    'weight': weight,
                    'tcin': tcin
                })
        except Exception as e:
            print(f'Target Get Products Failed: {str(e)}')
            print(resp)

        return products

    def get_storeID(self, zipcode):
        # Get Target store ID based on zipcode
        store_url = self.format_storeID_url(zipcode)

        r = requests.request('GET', store_url, headers={}, data={})
        store_ID = r.json()["data"]["nearby_stores"]["stores"][0]["store_id"]

        return store_ID

    def get_price(self, tcin, zipcode):
        target_price = {}

        storeID = self.get_storeID(zipcode)

        # Get product's price by searching for the product individually on Target's website
        url = self.get_price_url(tcin, storeID)
        r = requests.request("GET", url['price_url'], headers=url['price_headers'], data={})

        target_price_data = r.json()

        # Parse price from target
        try:
            target_price = target_price_data['data']['product']['price']['formatted_current_price']
        except Exception as e:
            print(f'Target Get Price Failed (Likely Due to Expired Token): {str(e)}')
            print(target_price_data)

        return target_price

    def get_query_url(self, query):
        return {
            'query_url': self.format_query_url(query),
            'query_headers': self.query_headers
        }
    
    def get_price_url(self, tcin, storeID):
        return {
            'price_url': self.format_price_url(tcin, storeID),
            'price_headers': self.price_headers
        }
    
    def format_name(self, name):
        weight = ""
        # Remove delimiters
        delimiters = [
            "&#38",
            "&#8482;",
            "&#39&",
            ";"
        ]
        for delim in delimiters:
            name = name.replace(';', '&') if delim == ";" else name.replace(delim, '')

        # If the product name contains the size, separate it from the name
        if " - " in name:
            name = name.split(' ')
            indexDash1 = name.index("-")
            name.remove("-")
            indexDash2 = len(name)

            # If there is another dash
            if "-" in name:
                index2 = name.index("-")
                name.remove("-")
                
            weight = ' '.join(name[indexDash1:indexDash2])
            name = ' '.join(name[0:indexDash1] + name[indexDash2:])

        return {
            'name': name,
            'weight': weight if weight != "" else "N/A"
        }
    
    def format_query_url(self, query):
        return f'https://redsky.target.com/redsky_aggregations/v1/web/plp_search_v2?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&channel=WEB&count=24&default_purchasability_filter=true&include_sponsored=true&keyword={query}&offset=0&page=%2Fs%2F{query}&platform=mobile&pricing_store_id=2176&scheduled_delivery_store_id=2176&store_ids=2176%2C319%2C950%2C1429%2C1905&useragent=Mozilla%2F5.0+%28Linux%3B+Android+6.0%3B+Nexus+5+Build%2FMRA58N%29+AppleWebKit%2F537.36+%28KHTML%2C+like+Gecko%29+Chrome%2F111.0.0.0+Mobile+Safari%2F537.36&visitor_id=0186C9840741020196EB42E2531CC94E&zip=85281'

    def format_price_url(self, tcin, storeID):
        return f'https://redsky.target.com/redsky_aggregations/v1/web/pdp_client_v1?key=9f36aeafbe60771e321a7cc95a78140772ab3e96&tcin={tcin}&is_bot=false&member_id=0&pricing_store_id={storeID}&has_pricing_store_id=true&scheduled_delivery_store_id={storeID}&has_financing_options=true&visitor_id=0186DC431E3C02018F5C06CF78CED296&has_size_context=true&skip_personalized=false&channel=WEB&page=%2Fp%2FA-83880304'
    
    def format_storeID_url(self, zipcode):
        return f'https://redsky.target.com/redsky_aggregations/v1/web_platform/nearby_stores_v1?limit=1&within=100&place={zipcode}&key=8df66ea1e1fc070a6ea99e942431c9cd67a80f02&channel=WEB&page=%2Fs%2F'
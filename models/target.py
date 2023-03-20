import requests

class Target:
    def __init__(self):
        self.cookie = 'TealeafAkaSid=LpZdmzjbHlKiarchtElASxEpG9_4zFuj; visitorId=0186DC431E3C02018F5C06CF78CED296; sapphire=1; UserLocation=85287|33.430|-111.930|AZ|US; __gads=ID=120f7a5f2b5ab553:T=1678732634:S=ALNI_Ma6Fq-UViOJPGJJJIAsqKBPGAAY8A; ci_pixmgr=other; _gcl_au=1.1.1294459899.1678732636; 3YCzT93n=A0CHRdyGAQAA5GA1FaU6DNITRuGuT8xXEm8qhUTut-gRn4ZBK2nFfwBF7_6sAYHbCHKucuFZwH9eCOfvosJeCA|1|1|7db79e8eb748cf56ba796f1cb0ad5eccd543eb84; crl8.fpcuid=bb1a7b80-05dc-4e85-828b-a5a4d6e0c242; ffpersistent=%7B%22channelStack%22%3A%5B%7B%22channel%22%3A%22%22%2C%22timestamp%22%3A%222023-03-17T20%3A09%3A50.156Z%22%7D%5D%7D; fiatsCookie=DSI_1429|DSN_Mesa%20West|DSZ_85202; egsSessionId=01450a41-6f2b-4d5e-838b-edb043df7eff; accessToken=eyJraWQiOiJlYXMyIiwiYWxnIjoiUlMyNTYifQ.eyJzdWIiOiI1OTg1NjA2Ni1lNjg5LTRlNTMtODZjNC01YzYwMmU3MWUyOWUiLCJpc3MiOiJNSTYiLCJleHAiOjE2Nzk0MjUxNzMsImlhdCI6MTY3OTMzODc3MywianRpIjoiVEdULjlhY2IzMzIzNzdkZDRkNmQ4MjVkOTJjODY3ZmNiZDc4LWwiLCJza3kiOiJlYXMyIiwic3V0IjoiRyIsImRpZCI6ImUwMTc5NjY4ZGJkYjJiMzk4YzlmNzgyMDExNzA2ODNkNmIwMjhmZjEyMGQ2MWZlZTllMTdmZjgxZDk4NmYwNjYiLCJzY28iOiJlY29tLm5vbmUsb3BlbmlkIiwiY2xpIjoiZWNvbS13ZWItMS4wLjAiLCJhc2wiOiJMIn0.gJTI_NkT5ru9I_Q4oegK-oNIvNEUzsSvxWky6ZBc65l4eFTpNuRaW3iKk2jOnkYd5WfxFGvPRyti56jo8EW4IpncHkz7KuScso7T0eJ9QOHJLw76r579n2_i_Hq2mAnp0nje6SHtb8G-tN6tNkJazo1HAx0q-x9c2C0VN_UvPehYKLHrTU71OSOkSx9ZNAb0Cv6o0c-crxW18dFqDreBl9_cW7p5SmyyvTtFBdys-p334TZmwyu-K7RWZIP17LxpTAePucJVByNMRYTHtb0DZK2eO08BtHBbW2DSfe4uJ7wxtYNX5weryfZQjr7u21rzDA6YkOO92jfSxkvMELeJLg; idToken=eyJhbGciOiJub25lIn0.eyJzdWIiOiI1OTg1NjA2Ni1lNjg5LTRlNTMtODZjNC01YzYwMmU3MWUyOWUiLCJpc3MiOiJNSTYiLCJleHAiOjE2Nzk0MjUxNzMsImlhdCI6MTY3OTMzODc3MywiYXNzIjoiTCIsInN1dCI6IkciLCJjbGkiOiJlY29tLXdlYi0xLjAuMCIsInBybyI6eyJmbiI6bnVsbCwiZW0iOm51bGwsInBoIjpmYWxzZSwibGVkIjpudWxsLCJsdHkiOmZhbHNlfX0.; refreshToken=eGyhyV2anpJ9Fl5G7zVOyikqOzc8nfoAGC4zohiZsYGuFegayJUYHX36kkrYi7vVzM0bGgBMUOF4QjFLemTpqQ; __gpi=UID=0000095e2f068964:T=1678732634:RT=1679338774:S=ALNI_MaECc4Qi0ArYNn9pTKXs6jHD4P0yQ;  _uetsid=5b6b80f0c75111ed9ef75b14d7fb4ca8; _uetvid=9285ba10288c11ed98bdf7f69ea87e59; _mitata=NWFjOGMzMzM4MjY2MzYxNWQ3YWQ0NjBjY2RlMzEyOGY1NWUwYWJiM2E4YjY3OTJmYTIwMTAxZDYxM2JiODVlYg==_/@#/1679338898_/@#/cbApWHFpQCPmcnDe_/@#/OGZlZWFkMGFjYTcxZGZhZjU3YTFmYzNhMjFmZTRlMTViYzhmYTNkNzJiMjQ0NGFkMzY4Yzc0ZTAwY2Q5NjUzNg==_/@#/000'

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
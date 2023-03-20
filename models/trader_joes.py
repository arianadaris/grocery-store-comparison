import json
import requests

class Trader_Joes:
    def __init__(self):
        self.url = "https://www.traderjoes.com/api/graphql"

        self.price_cookie = 'affinity="3e6faca53c5e6b7f"; AMCVS_B5B4708F5F4CE8D80A495ED9%40AdobeOrg=1; AMCV_B5B4708F5F4CE8D80A495ED9%40AdobeOrg=-2121179033%7CMCIDTS%7C19436%7CMCMID%7C80377640608433832790735918013757241503%7CMCAAMLH-1679854699%7C9%7CMCAAMB-1679854699%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1679257099s%7CNONE%7CvVersion%7C5.3.0; s_vncm=1680332399841%26vn%3D1; s_ivc=true; s_lv_s=First%20Visit; s_visit=1; s_dur=1679249899852; s_inv=0; s_cc=true; _ga=GA1.2.80229188.1679249900; _gid=GA1.2.2031793707.1679249900; _gat_UA-15671700-1=1; s_tps=8; s_pvs=11; s_nr30=1679249908770-New; s_lv=1679249908770; s_ips=908; s_tp=908; s_ptc=%5B%5BB%5D%5D'

        self.price_headers = {
        'authority': 'www.traderjoes.com',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'cookie': self.price_cookie,
        'origin': 'https://www.traderjoes.com',
        'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
    }

    def get_products(self, query):
        # Return a list of products
        products = []

        # Format and make a request to retrieve product data from Trader Joes
        trader_joes = self.get_query_url(query)

        # Get Trader Joes search results
        r = requests.request("POST", trader_joes["query_url"], headers=trader_joes["query_headers"], data=trader_joes["query_payload"])
        resp = r.json()

        try:
            query_products = r.json()['data']['products']['items']

            for product in query_products:
                # Get product details
                name = product['item_title']
                sku = product['sku']
                image = 'https://www.traderjoes.com' + product['primary_image']
                keyword = query.replace("+", ' ')

                # Get weight
                weight_num = product['sales_size']
                weight_measure = product['sales_uom_description']
                weight = f'{weight_num} {weight_measure}'

                products.append({
                    'name': name,
                    'image': image,
                    'keyword': keyword,
                    'weight': weight,
                    'sku': sku
                })
        except Exception as e:
            print(f'Trader Joes Get Products Failed: {str(e)}')
            print(resp)

        return products

    def get_price(self, sku):
        url = self.get_price_url(sku)

        r = requests.request("POST", url['price_url'], headers=url['price_headers'], data=url['price_payload'])
        resp = r.json()

        try:
            trader_joes_price_data = r.json()['data']['products']['items']

            # Parse price from trader joes
            trader_joes_price = trader_joes_price_data[0]['retail_price']
        except Exception as e:
            print(f'Trader Joes Get Price Failed: {str(e)}')
            print(resp)

        return trader_joes_price


    def get_query_url(self, query):
        return {
            'query_url': self.url,
            'query_payload': self.format_query_payload(query),
            'query_headers': self.format_query_headers(query)
        }
    
    def get_price_url(self, sku):
        return {
            'price_url': self.url,
            'price_headers': self.price_headers,
            'price_payload': self.format_price_payload(sku)
        }


    def format_query_payload(self, query):
        search = query.replace('+', ' ')
        return json.dumps({
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

    def format_query_headers(self, query):
        return {
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

    def format_price_payload(self, sku):
        return json.dumps({
        "operationName": "SearchProduct",
        "variables": {
            "storeCode": "91",
            "published": "1",
            "sku": sku
        },
        "query": "query SearchProduct($sku: String, $storeCode: String = \"91\", $published: String = \"1\") {\n  products(\n    filter: {sku: {eq: $sku}, store_code: {eq: $storeCode}, published: {eq: $published}}\n  ) {\n    items {\n      category_hierarchy {\n        id\n        url_key\n        description\n        name\n        position\n        level\n        created_at\n        updated_at\n        product_count\n        __typename\n      }\n      item_story_marketing\n      product_label\n      fun_tags\n      primary_image\n      primary_image_meta {\n        url\n        metadata\n        __typename\n      }\n      other_images\n      other_images_meta {\n        url\n        metadata\n        __typename\n      }\n      context_image\n      context_image_meta {\n        url\n        metadata\n        __typename\n      }\n      published\n      sku\n      url_key\n      name\n      item_description\n      item_title\n      item_characteristics\n      item_story_qil\n      use_and_demo\n      sales_size\n      sales_uom_code\n      sales_uom_description\n      country_of_origin\n      availability\n      new_product\n      promotion\n      price_range {\n        minimum_price {\n          final_price {\n            currency\n            value\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      retail_price\n      nutrition {\n        display_sequence\n        panel_id\n        panel_title\n        serving_size\n        calories_per_serving\n        servings_per_container\n        details {\n          display_seq\n          nutritional_item\n          amount\n          percent_dv\n          __typename\n        }\n        __typename\n      }\n      ingredients {\n        display_sequence\n        ingredient\n        __typename\n      }\n      allergens {\n        display_sequence\n        ingredient\n        __typename\n      }\n      created_at\n      first_published_date\n      last_published_date\n      updated_at\n      related_products {\n        sku\n        item_title\n        primary_image\n        primary_image_meta {\n          url\n          metadata\n          __typename\n        }\n        price_range {\n          minimum_price {\n            final_price {\n              currency\n              value\n              __typename\n            }\n            __typename\n          }\n          __typename\n        }\n        retail_price\n        sales_size\n        sales_uom_description\n        category_hierarchy {\n          id\n          name\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    total_count\n    page_info {\n      current_page\n      page_size\n      total_pages\n      __typename\n    }\n    __typename\n  }\n}\n"
    })
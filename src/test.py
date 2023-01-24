from dotenv import dotenv_values
from notion_client import Client
import requests
import json
import yfinance as yf
from pprint import pprint
from datetime import date

config = dotenv_values(".env")
token = config.get('NOTION_TOKEN')
stockDBid= '1b31ecd513f444299d85b90d818c7e99'
notion = Client(auth=token)

headers = {
    "accept": "application/json",
    "Notion-Version": "2022-06-28",
    "content-type": "application/json",
    "Authorization": f"Bearer {token}",
}

def stock_price_refresh():
    query_url = f'https://api.notion.com/v1/databases/{stockDBid}/query'
    r = requests.post(query_url, headers=headers)

    result_dict = r.json().get("results")

    patch_url = "https://api.notion.com/v1/pages/"


    for item in result_dict:
        prop = item["properties"]
        ticker = prop.get("Ticker").get("title")[0].get("plain_text")
        id = item.get("url").split("-")[1]    
        ticker_stock = yf.Ticker(ticker).info    
        market_price = ticker_stock['regularMarketPrice']
        item['properties']['현재가']['number'] = market_price
        response = requests.patch(patch_url + id, headers=headers, data=json.dumps(item))
        if response.status_code == 200:
            print(ticker + " is Updated")
    

stock_price_refresh()
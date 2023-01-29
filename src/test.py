from dotenv import dotenv_values
from notion_client import Client
import requests
import json
import yfinance as yf
from pprint import pprint
from datetime import date

config = dotenv_values(".env")
token = config.get('NOTION_TOKEN')
stockDBid= config.get('STOCK_DB_ID')
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
        ticker_stock = yf.Ticker(ticker).fast_info    
        market_price = ticker_stock['last_price']
        item['properties']['현재가']['number'] = market_price
        response = requests.patch(patch_url + id, headers=headers, data=json.dumps(item))
        if response.status_code == 200:
            print(ticker + " is Updated")
    
    refresh_updated_date()


def refresh_updated_date():
    block_id = config.get("STOCK_UPDATE_DATE_BLOCK_ID")
    block_url = "https://api.notion.com/v1/blocks/" + block_id
    block = requests.get(block_url, headers=headers).json()
    today = date.today()
    d1 = today.strftime("%Y-%m-%d")
    block['paragraph']['rich_text'][0]['mention']['date']['start'] = d1
    response = requests.patch(block_url, headers=headers, data=json.dumps(block))

stock_price_refresh()
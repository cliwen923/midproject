import requests
import json
import csv
from datetime import datetime
import os

def scrape_bitcoin_price():
    url = "https://www.okx.com/api/v5/market/ticker"
    params = {"instId": "BTC-USDT"}  # Specify the trading pair

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data.get('code') == '0' and data.get('msg') == '':
            ticker_data = data['data'][0]
            price = ticker_data['last']
            timestamp = datetime.now().isoformat()
            return {"timestamp": timestamp, "price": price}
        else:
            print(f"Error from OKX API: {data.get('code')}, {data.get('msg')}")
            return None

    except requests.exceptions.RequestException as e:
        print(f"抓取 OKX API 時發生錯誤：{e}")
        return None
    except (KeyError, IndexError):
        print("無法在 OKX API 回應中找到比特幣價格。請檢查 API 回應格式。")
        return None

def save_to_json(data, filename="static.json"):
    existing_data = []
    if os.path.exists(filename):
        try:
            with open(filename, 'r') as f:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
        except json.JSONDecodeError:
            print(f"警告：無法解碼 {filename} 中的現有 JSON。將覆寫為新資料。")
            existing_data = []
        except FileNotFoundError:
            pass

    existing_data.append(data)

    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=4)
    print(f"從 OKX 獲取的比特幣價格已附加至 {filename}")

def save_to_csv(data, filename="static.csv"):
    file_exists = os.path.exists(filename)
    with open(filename, 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["timestamp", "price"])
        writer.writerow([data["timestamp"], data["price"]])
    print(f"從 OKX 獲取的比特幣價格已附加至 {filename}")

if __name__ == "__main__":
    bitcoin_data = scrape_bitcoin_price()
    if bitcoin_data:
        save_to_json(bitcoin_data)
        save_to_csv(bitcoin_data)
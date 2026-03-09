#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TasaVe - Exchange Rate Scraper
Fetches BCV official rates and Binance P2P USDT rates
Generates data.json for the webapp
"""

import json
import requests
from datetime import datetime
import time
import sys
import io

# Fix Windows console encoding for Unicode characters
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def get_bcv_rates():
    """
    Fetch BCV official rates for USD and EUR using pydolarvenezuela-api
    Returns: dict with bcv_usd and bcv_eur
    """
    try:
        url = "https://pydolarvenezuela-api.vercel.app/api/v1/dollar/page?page=bcv"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        usd_rate = float(data['monitors']['usd']['price'])
        eur_rate = float(data['monitors']['eur']['price'])
        
        return {
            'bcv_usd': usd_rate,
            'bcv_eur': eur_rate
        }
        
    except Exception as e:
        print(f"Error fetching BCV rates: {e}")
        return {
            'bcv_usd': 0.0,
            'bcv_eur': 0.0
        }


def get_binance_p2p_rates():
    """
    Fetch Binance P2P USDT/VES rates
    Returns: dict with usdt_buy, usdt_sell, and usdt_avg
    """
    try:
        url = "https://p2p.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        # Get BUY orders (people selling USDT - parallel reference)
        buy_payload = {
            "asset": "USDT",
            "fiat": "VES",
            "merchantCheck": False,
            "page": 1,
            "payTypes": [],
            "publisherType": None,
            "rows": 5,
            "tradeType": "BUY"
        }
        
        buy_response = requests.post(url, headers=headers, json=buy_payload, timeout=10)
        buy_response.raise_for_status()
        buy_data = buy_response.json()
        
        # Get SELL orders (people buying USDT)
        sell_payload = {
            "asset": "USDT",
            "fiat": "VES",
            "merchantCheck": False,
            "page": 1,
            "payTypes": [],
            "publisherType": None,
            "rows": 5,
            "tradeType": "SELL"
        }
        
        sell_response = requests.post(url, headers=headers, json=sell_payload, timeout=10)
        sell_response.raise_for_status()
        sell_data = sell_response.json()
        
        # Calculate averages
        buy_prices = []
        sell_prices = []
        
        if 'data' in buy_data and buy_data['data']:
            for ad in buy_data['data'][:5]:
                if 'adv' in ad and 'price' in ad['adv']:
                    buy_prices.append(float(ad['adv']['price']))
        
        if 'data' in sell_data and sell_data['data']:
            for ad in sell_data['data'][:5]:
                if 'adv' in ad and 'price' in ad['adv']:
                    sell_prices.append(float(ad['adv']['price']))
        
        if not buy_prices or not sell_prices:
            print("Warning: Could not get enough Binance P2P prices")
            return None
        
        usdt_buy = sum(buy_prices) / len(buy_prices)
        usdt_sell = sum(sell_prices) / len(sell_prices)
        usdt_avg = (usdt_buy + usdt_sell) / 2
        
        return {
            'usdt_buy': round(usdt_buy, 2),
            'usdt_sell': round(usdt_sell, 2),
            'usdt_avg': round(usdt_avg, 2)
        }
        
    except Exception as e:
        print(f"Error fetching Binance P2P rates: {e}")
        return None


def generate_data_json():
    """
    Main function to fetch all rates and generate data.json
    """
    print("Starting exchange rate fetch...")
    
    # Get BCV rates
    print("Fetching BCV rates...")
    bcv_rates = get_bcv_rates()
    
    # Get Binance P2P rates
    print("Fetching Binance P2P rates...")
    binance_rates = get_binance_p2p_rates()
    
    # Prepare data object
    data = {
        'bcv_usd': 0,
        'bcv_eur': 0,
        'usdt_buy': 0,
        'usdt_sell': 0,
        'usdt_avg': 0,
        'last_update': datetime.now().isoformat(),
        'source': 'BCV + Binance P2P',
        'error': None
    }
    
    # Update with fetched data
    if bcv_rates:
        data['bcv_usd'] = bcv_rates['bcv_usd']
        data['bcv_eur'] = bcv_rates['bcv_eur']
        print(f"✓ BCV rates: USD={bcv_rates['bcv_usd']}, EUR={bcv_rates['bcv_eur']}")
    else:
        data['error'] = 'Failed to fetch BCV rates'
        print("✗ Failed to fetch BCV rates")
    
    if binance_rates:
        data['usdt_buy'] = binance_rates['usdt_buy']
        data['usdt_sell'] = binance_rates['usdt_sell']
        data['usdt_avg'] = binance_rates['usdt_avg']
        print(f"✓ Binance P2P rates: Buy={binance_rates['usdt_buy']}, Sell={binance_rates['usdt_sell']}, Avg={binance_rates['usdt_avg']}")
    else:
        if data['error']:
            data['error'] += ' | Failed to fetch Binance rates'
        else:
            data['error'] = 'Failed to fetch Binance rates'
        print("✗ Failed to fetch Binance P2P rates")
    
    # Write to JSON file
    try:
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ data.json generated successfully at {data['last_update']}")
    except Exception as e:
        print(f"✗ Error writing data.json: {e}")
        raise


if __name__ == "__main__":
    generate_data_json()

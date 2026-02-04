import requests

# bitcoin
headers = {"X-Api-Key": "Nuh uh uh"} # API Ninjas
btc_response = requests.get("https://api.api-ninjas.com/v1/bitcoin", headers=headers)

def btc(): # makes the price a float
    data = btc_response.json()
    return float(data["price"])

# exchange rates
exchange_key = "Nuh uh uh" # exhcange rates api
exchange_url = f"https://api.exchangeratesapi.io/v1/latest?access_key= Nuh uh uh &format=1"

def exchange_rates():
    response = requests.get(exchange_url)
    data = response.json()
    return data

def converter(usd_price):
    # the exchange rates is kinda sucky and it converting from euro
    # so i have to convert euro to aud then euro to usd, then usd to aud

    exchange_data = exchange_rates()
    usd = exchange_data["rates"]["USD"]  # euro to usd rate
    aud = exchange_data["rates"]["AUD"]  # euro to aud rate

    usd_to_aud_rate = aud / usd
    
    aud_price = usd_price * usd_to_aud_rate
    return aud_price


btc_usd = btc() # get bitcoin price in usd
btc_aud = converter(btc_usd) # convert to aud

print(f'The Current Price of BTC is ${btc_usd} USD and ${btc_aud} AUD')
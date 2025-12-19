from django.shortcuts import render, redirect
from django.core.cache import cache
import requests
from .models import *
from django.core.paginator import Paginator
from django.conf.urls import handler404, handler500

# Create your views here.
def home(request):
    post=Post.objects.all()
    coins = ["bitcoin", "ethereum", "binancecoin"]
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&ids={','.join(coins)}"
    response = requests.get(url)
    cryptos = response.json()  # list of dicts with price, market_cap, etc.
    affiliate_links = {
        "bitcoin": "https://www.binance.com/en/register?ref=1117749884",
        "ethereum": "https://www.binance.com/en/register?ref=1117749884",
        "binancecoin": "https://www.binance.com/en/register?ref=1117749884",
    }
    
    return render(request, "index.html", {"post":post,'cryptos': cryptos,'affiliate_links': affiliate_links})

def cryptos(request):
    AFFILIATE_LINKS = {
        "bitcoin": "https://www.binance.com/en/register?ref=1117749884",
        "ethereum": "https://www.binance.com/en/register?ref=1117749884",
        "binancecoin": "https://www.binance.com/en/register?ref=1117749884",
    }

    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 50,
        "page": 1,
        "sparkline": False
    }

    cryptos = []
    error_message = None
    last_prices = cache.get("last_prices", {})

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        cryptos_data = response.json()

        for crypto in cryptos_data:
            last_price = last_prices.get(crypto["id"], crypto["current_price"])
            price_change = crypto["current_price"] - last_price
            price_change_percent = (
                round(price_change / last_price * 100, 2) if last_price != 0 else 0
            )

            cryptos.append({
                "id": crypto["id"],
                "name": crypto["name"],
                "symbol": crypto["symbol"],
                "current_price": crypto["current_price"],
                "market_cap": crypto["market_cap"],
                "price_change": price_change,
                "price_change_percent": price_change_percent,
                "is_up": price_change > 0,
                "is_down": price_change < 0,
            })

            last_prices[crypto["id"]] = crypto["current_price"]

        cache.set("last_prices", last_prices, 60 * 5)

    except requests.RequestException:
        error_message = "Network/API issue: showing last known prices if available."
        for coin_id, price in last_prices.items():
            cryptos.append({
                "id": coin_id,
                "name": coin_id.capitalize(),
                "symbol": coin_id[:3].upper(),
                "current_price": price,
                "market_cap": 0,
                "price_change": 0,
                "price_change_percent": 0,
                "is_up": False,
                "is_down": False,
            })

    # ---------------------------
    # 🔥 ADD PAGINATION HERE
    # ---------------------------
    paginator = Paginator(cryptos, 10)  # 10 cryptos per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "cryptos.html", {
        "cryptos": page_obj,     # tumia page_obj
        "affiliate_links": AFFILIATE_LINKS,
        "error_message": error_message
    })


def cryptoNews(request):
    url = "https://cryptopanic.com/api/v1/posts/"
    params = {
        "auth_token": "d450e92a32ffd94df3349bf56807a9261e3b257a",
        "public": "true"
    }

    response = requests.get(url, params=params)

    try:
        data = response.json()
        news = data.get("results", [])
    except:
        news = []

    return render(request, "crypto_news.html", {
        "news": news
    })
def analysis(request):
    # --- Get coins ---
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": False
    }
    coins = requests.get(url, params=params).json()

    for coin in coins:
        change = coin.get("price_change_percentage_24h", 0)
        if change > 5:
            coin["analysis"] = "Strong bullish momentum."
        elif change > 0:
            coin["analysis"] = "Mild uptrend."
        elif change > -5:
            coin["analysis"] = "Minor correction."
        else:
            coin["analysis"] = "Bearish trend."

    # --- Get crypto news ---
    news_url = "https://api.coingecko.com/api/v3/news"
    news_data = requests.get(news_url).json()
    news_list = news_data.get("data", [])[:5]  # Top 5 news

    return render(request, "analysis.html", {"cryptos": coins, "news_list": news_list})


def aboutUs(request):
	about=About.objects.all()
	if request.method == 'POST':
		ideals=Ideals.objects.create()
		name=request.POST.get('name')
		ideal=request.POST.get('ideas')
		ideals.name=name
		ideals.ideal=ideal
		ideals.save()
		return redirect("about_us")
	return render(request, "about_us.html", {'about':about})

def buy_crypto(request, coin):

    # Redirect to affiliate link
    links = {
        "bitcoin": "https://www.binance.com/en/register?ref=1117749884",
        "ethereum": "https://www.binance.com/en/register?ref=1117749884",
        "binancecoin": "https://www.binance.com/en/register?ref=1117749884",
    }
    target = links.get(coin, "https://www.binance.com")
    return redirect(target)
    return render(request, 'buy.html', {'crypto': crypto})

import requests
from textblob import TextBlob

class MarketAnalyzer:
    def __init__(self, api_key, news_api_key):
        self.base_url = "https://www.alphavantage.co/query"
        self.api_key = api_key
        self.news_api_key = news_api_key       

    def get_historical_prices(self, symbol, interval='daily', outputsize='compact'):
        pass
    '''
        params = {
            "function": "TIME_SERIES_INTRADAY" if interval == 'intraday' else "TIME_SERIES_DAILY",
            "symbol": symbol,
            "apikey": self.api_key,
            "outputsize": outputsize
        }
        response = requests.get(self.base_url, params=params)
        data = response.json()

        if "Time Series (Daily)" in data:
            return data["Time Series (Daily)"]
        elif "Time Series (60min)" in data:
            return data["Time Series (60min)"]
        else:
            print("Error:", data["Error Message"])
            return None

    def calculate_moving_averages(self, closing_prices):
        short_term_ma = sum(closing_prices[-5:]) / 5
        long_term_ma = sum(closing_prices[-20:]) / 20
        return short_term_ma, long_term_ma

    def calculate_rsi(self, closing_prices, period=14):
        deltas = [closing_prices[i + 1] - closing_prices[i] for i in range(len(closing_prices) - 1)]
        gain = [d if d > 0 else 0 for d in deltas]
        loss = [abs(d) if d < 0 else 0 for d in deltas]

        avg_gain = sum(gain[:period]) / period
        avg_loss = sum(loss[:period]) / period

        for i in range(period, len(closing_prices) - 1):
            avg_gain = ((period - 1) * avg_gain + gain[i]) / period
            avg_loss = ((period - 1) * avg_loss + loss[i]) / period

        if avg_loss != 0:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        else:
            rsi = 100

        return rsi

    def analyze_market_trend(self, symbol, market_type='stock'):
        prices = self.get_historical_prices(symbol)
        if not prices:
            return None

        closing_prices = [float(price_data['4. close']) for price_data in prices.values()]
        short_term_ma, long_term_ma = self.calculate_moving_averages(closing_prices)
        rsi = self.calculate_rsi(closing_prices)

        if market_type == 'stock':
            if short_term_ma > long_term_ma and rsi < 30:  # Buy signal if short-term MA > long-term MA and RSI is low
                return "Buy"
            elif short_term_ma < long_term_ma and rsi > 70:  # Sell signal if short-term MA < long-term MA and RSI is high
                return "Sell"
            else:
                return "Hold"
'''
    def calculate_sentiment(self, symbol):
        # Fetch news headlines related to the symbol
        news_url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={self.news_api_key}"
        response = requests.get(news_url)
        news_data = response.json()

        if news_data["totalResults"] > 0:
            headlines = [article["title"] for article in news_data["articles"]]
            sentiment_scores = [TextBlob(headline).sentiment.polarity for headline in headlines]
            avg_sentiment = sum(sentiment_scores) / len(sentiment_scores)
            return avg_sentiment
            return headlines
        else:
            print("No news headlines found for", symbol)
            return 0

    def get_news_headlines(self, symbol):
        news_url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={self.news_api_key}"
        response = requests.get(news_url)
        news_data = response.json()

        headlines = []
        if news_data["totalResults"] > 0:
            headlines = [article["title"] for article in news_data["articles"]]
        else:
            print("No news headlines found for", symbol)
        
        return headlines

def main():
    api_key = 'WO0CMAJSK0KCEMNS'  # Replace 'YOUR_API_KEY' with your actual Alpha Vantage API key
    news_api_key = '14b30024c8704b3d80da49e10eee15b2'  # Replace 'YOUR_NEWS_API_KEY' with your News API key
    market_analyzer = MarketAnalyzer(api_key, news_api_key)

    # Example usage for analyzing market trend of a stock (e.g., AAPL)
    symbol = input("Stock Symbol: ")
#    trend = market_analyzer.analyze_market_trend(symbol)
    sentiment = market_analyzer.calculate_sentiment(symbol)
    headlines = market_analyzer.get_news_headlines(symbol)
#    if trend:
#        print(f"Market trend for {symbol}: {trend}")
    print(f"Sentiment anlaysis for {symbol}: {sentiment}")
    
    if headlines:
        print("Some headlines:")
        for headline in headlines[:5]:  # Print the first 5 headlines
            print("- ", headline)

if __name__ == "__main__":
    main()

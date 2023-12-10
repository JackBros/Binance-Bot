from binance.client import Client
import time

api_key = 'your_testnet_api_key'  # Kendi testnet API anahtarınızı buraya ekleyin
api_secret = 'your_testnet_api_secret'  # Kendi testnet API sırrınızı buraya ekleyin
client = Client(api_key, api_secret, testnet=True)

symbol = 'BTCUSDT'
quantity = 0.001
min_price_difference = 0.00000002
stop_loss_threshold = 0.00000002
take_profit_threshold = 0.00000002

price_history = []
buy_price = 0  # Satın alma fiyatını takip etmek için eklenen yeni değişken

while True:
    try:
        ticker = client.get_ticker(symbol=symbol)
        current_price = float(ticker['lastPrice'])

        price_history.append(current_price)

        if len(price_history) > 15:
            min_price = min(price_history)
            max_price = max(price_history)

            price_difference = max_price - min_price

            print(f"Min Price: {min_price}, Max Price: {max_price}, Price Difference: {price_difference}")

            # Satın alma işlemi
            if price_difference <= min_price_difference and buy_price == 0:
                print(f"Buying {quantity} {symbol} at {min_price}")
                order = client.create_test_order(
                    symbol=symbol,
                    side='BUY',
                    type='LIMIT',
                    quantity=quantity,
                    price=min_price
                )
                print(order)
                buy_price = min_price  # Satın alma yapıldığında buy_price'i güncelle

            # Satış işlemi
            if current_price >= (buy_price - stop_loss_threshold) or current_price >= (buy_price + take_profit_threshold):
                print(f"Selling {quantity} {symbol} at {current_price}")
                sell_order = client.create_test_order(
                    symbol=symbol,
                    side='SELL',
                    type='LIMIT',
                    quantity=quantity,
                    price=current_price
                )
                print(sell_order)

                # Satış gerçekleştiğinde alım fiyatını sıfırla
                buy_price = 0

            price_history = []  # 15 dakika bittiğinde fiyat geçmişini sıfırla

        time.sleep(60)

    except Exception as e:
        print(f"Hata oluştu: {e}")
        time.sleep(60)  # Hata durumunda 1 dakika bekleyip tekrar dene

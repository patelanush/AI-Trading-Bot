
from lumibot.brokers import Alpaca
from lumibot.backtesting import YahooDataBacktesting
from lumibot.strategies.strategy import Strategy
from lumibot.traders import Trader
from datetime import datetime 
from alpaca_trade_api import REST 
from timedelta import Timedelta 
from finbert_utils import estimate_sentiment
import mysql.connector
from mysql.connector import Error


DB_HOST = 'localhost'
DB_USER = 'root'
DB_PASSWORD = 'my_password'
DB_NAME = 'trading_bot_db'

def insert_trade(trade_id, symbol, action, quantity, price, sentiment, probability, last_trade_action, take_profit_price, stop_loss_price):
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        cursor = connection.cursor()
        sql = """INSERT INTO trades (symbol, action, quantity, price, sentiment, probability, last_trade_action, take_profit_price, stop_loss_price) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        values = (symbol, action, quantity, price, sentiment, probability, last_trade_action, take_profit_price, stop_loss_price)
        cursor.execute(sql, values)
        connection.commit()
    except Error as e:
        print(f"ErrorSQL: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()



API_KEY = "API KEY" 
API_SECRET = "API_SECRET" 
BASE_URL = "https://paper-api.alpaca.markets/v2"

ALPACA_CREDS = {
    "API_KEY":API_KEY, 
    "API_SECRET": API_SECRET, 
    "PAPER": True
}

class MLTrader(Strategy): 
    def initialize(self, symbol:str="SPY", cash_at_risk:float = 0.5): 
        self.symbol = symbol
        self.sleeptime = "24H" 
        self.last_trade = None 
        self.cash_at_risk = cash_at_risk
        self.api = REST(base_url=BASE_URL, key_id=API_KEY, secret_key= API_SECRET)

    def position_sizing(self): 
        cash = self.get_cash() 
        last_price = self.get_last_price(self.symbol)
        quantity = round(cash * self.cash_at_risk / last_price,0)
        return cash, last_price, quantity
    
    def get_dates(self):
        today = self.get_datetime()
        days_prior = today - Timedelta(days = 5)
        return today.strftime('%Y-%m-%d'), days_prior.strftime('%Y-%m-%d')

    def get_sentiment(self): 
        today, days_prior = self.get_dates()
        news = self.api.get_news(symbol=self.symbol, start=days_prior,  end=today) 
        news = [ev.__dict__["_raw"]["headline"] for ev in news]
        probability, sentiment = estimate_sentiment(news)
        return probability, sentiment 
    
    def on_trading_iteration(self):
        cash, last_price, quantity = self.position_sizing() 
        probability, sentiment = self.get_sentiment()

        if cash > last_price: 
            if sentiment == "positive" and probability > .999: 
                if self.last_trade == "sell": 
                    self.sell_all() 
                order = self.create_order(self.symbol, quantity, "buy", type="bracket", take_profit_price=last_price*1.25, stop_loss_price=last_price*0.95)
                self.submit_order(order) 
                self.last_trade = "buy"

                try:
                    insert_trade(self.symbol, "buy", quantity, last_price, sentiment, probability, self.last_trade, last_price*1.25, last_price*0.95)
                except Exception as e:
                    print(f"erorr inserting trade: {e}")
            
            elif sentiment == "negative" and probability > .999: 
                if self.last_trade == "buy": 
                    self.sell_all() 
                order = self.create_order(self.symbol, quantity, "sell", type="bracket", take_profit_price=last_price*0.8, stop_loss_price=last_price*1.05)
                self.submit_order(order) 
                self.last_trade = "sell"

                try:
                   insert_trade(self.symbol, "sell", quantity, last_price, sentiment, probability, self.last_trade, last_price*0.8, last_price*1.05)
                except Exception as e:
                   print(f"erorr inserting trade: {e}")

        

start_date = datetime(2024,7,24)   
end_date = datetime(2024,7,28) 

broker = Alpaca(ALPACA_CREDS) 
strategy = MLTrader(name='mlstrat', broker=broker, parameters={"symbol" : "SPY", "cash_at_risk" : 0.5})
strategy.backtest(YahooDataBacktesting, start_date, end_date,  parameters={"symbol":"SPY", "cash_at_risk":.5})
 
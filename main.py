#importing libraries first 
import requests
from binance.client import Client 
import talib 
import time 
import numpy as np 

# importing configuration 
from config import TELEGRAM_TOKEN, TELEGRAM_CHANNEL , INTERVAL, SHORT_EMA , LONG_EMA 

# initializing binance client 
client = Client("<random api key>","<random secret key>")
#SYMBOLS TO LOOK FOR ALERTS 
SYMBOLS = [
    "ETHUSDT",
    "BTCUSDT",
    "ATOMUSDT",
    "BUSDUSDT",
    "FTMBUSD",
    "ENJUSDT",
    "WAXPUSDT"
]

# defining helper functions 

#sending alerts to telegram 
def send_message(message):
    url = "https://api.telegram.org/bot{}/sendMessage?chat_id={}&text={}&parse_mode=markdown".format(TELEGRAM_TOKEN,TELEGRAM_CHANNEL,message)
    res = requests.get(url);print(url);
    return res

# getting klines data to process
def get_klines(symbol):
    data = client.get_klines(symbol=symbol,interval=INTERVAL,limit=300) # more data means more precision but at the trade off between speed and time 
    return_data = []
    # taking closing data for each kline 
    for each in data:
        return_data.append(float(each[4])) # 4 is the index of the closing data in each kline 
    return np.array(return_data) # returning as numpy array for better precision and performance 




# entry point for file 
def main(): 
    # making a infinite loop that keeps checking for condition 
    while True:
        #looping through each coin 
        for each in SYMBOLS:
            data = get_klines(each)
            ema_short = talib.EMA(data,int(SHORT_EMA))
            ema_long = talib.EMA(data,int(LONG_EMA))
            
            last_ema_short  = ema_short[-2]
            last_ema_long = ema_long[-2]

            ema_short = ema_short[-1]
            ema_long = ema_long[-1]
        
            # conditions for alerts 
            if(ema_short > ema_long and last_ema_short < last_ema_long):
                message  = each + " "+ str(SHORT_EMA) + " over "+str(LONG_EMA);print(each ,"alert came");
                send_message(message);
            time.sleep(0.5);

        



# calling the function 
if __name__ == "__main__":
    main()

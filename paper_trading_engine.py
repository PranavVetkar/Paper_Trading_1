import asyncio
import json
import websockets

class PaperTrader:
    def __init__(self):
        self.balance = 1000
        self.position = 0
        self.prices = []
        self.in_position = False

    def get_signal(self):
        if len(self.prices) < 10: return "WAIT"
        
        avg_price = sum(self.prices[-10:]) / 10
        current_price = self.prices[-1]
        
        if current_price > avg_price and not self.in_position:
            return "BUY"
        elif current_price < avg_price and self.in_position:
            return "SELL"
        return "HOLD"

    async def start(self):
        url = "wss://stream.binance.com:9443/ws/btcusdt@ticker"
        async with websockets.connect(url) as ws:
            print("--- Paper Trading Session Started ---")
            print(f"Initial Balance: ${self.balance}")

            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                price = float(data['c'])
                self.prices.append(price)

                signal = self.get_signal()
                
                if signal == "BUY":
                    self.position = self.balance / price
                    self.balance = 0
                    self.in_position = True
                    print(f"🚀 BUY at ${price:,.2f} | Holding: {self.position:.6f} BTC")
                
                elif signal == "SELL":
                    self.balance = self.position * price
                    self.position = 0
                    self.in_position = False
                    print(f"💰 SELL at ${price:,.2f} | New Balance: ${self.balance:,.2f}")

if __name__ == "__main__":
    trader = PaperTrader()
    asyncio.run(trader.start())
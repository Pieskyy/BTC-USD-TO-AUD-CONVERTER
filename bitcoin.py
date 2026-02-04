import requests
import sys
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget,QVBoxLayout, QLabel)
from PySide6.QtCore import Qt

BTC_KEY = "#Put your api key here" # API-Ninjas key for bitcoin price
EXCHANGE_KEY = "# put you api key here" # EXCHANGE RATES API key for currency conversion


def btc(): #  gets the bitcoin price in USD
    headers = {"X-Api-Key": BTC_KEY}
    response = requests.get("https://api.api-ninjas.com/v1/bitcoin", headers=headers,timeout=5)
    data = response.json()
    return float(data["price"]) # returns the bitcoin price in USD as a float


def exchange_rates(): # gets exchange rates
    url = f"https://api.exchangeratesapi.io/v1/latest?access_key={EXCHANGE_KEY}&format=1"
    response = requests.get(url, timeout=5)
    return response.json()


def converter(usd_price): # converts the EUR to USD then EUR to AUD then USD to AUD
    exchange_data = exchange_rates()
    usd = exchange_data["rates"]["USD"]
    aud = exchange_data["rates"]["AUD"]

    usd_to_aud_rate = aud / usd
    return usd_price * usd_to_aud_rate


# Main window class
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bitcoin Price Tracker") # Title
        self.setFixedSize(420, 220)  # window size

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        
        main_layout.setAlignment(Qt.AlignCenter)  # Center everything
        main_layout.setSpacing(12)  # Space between widgets
        main_layout.setContentsMargins(30, 30, 30, 30)  # Margins around edges
        
        self.title_label = QLabel("CURRENT BITCOIN PRICE") # Title label
        self.title_label.setAlignment(Qt.AlignCenter)  # Center the text
        
        self.usd_price_label = QLabel("Getting price...") # if it takes a bit to load
        self.usd_price_label.setAlignment(Qt.AlignCenter) # Center the text

        self.aud_price_label = QLabel("Loading . . .") # if it takes a bit to load 
        self.aud_price_label.setAlignment(Qt.AlignCenter)
        
        main_layout.addWidget(self.title_label) # adds all these widgets to the main layout
        main_layout.addWidget(self.usd_price_label)
        main_layout.addWidget(self.aud_price_label)
        
        self.setCentralWidget(central_widget) # sets the center widget
        self.setup_styles() # sets styles
        self.get_bitcoin_prices() # gets the bitcoin prices and updates the labels
    
    def setup_styles(self):
        self.setStyleSheet("""
        QMainWindow {
            background-color: #2b2b2b;
        }
        
        QLabel {
            color: #d1d5db;
            font-family: Arial;
        }
        """)

        self.title_label.setStyleSheet("""
            font-size: 22px;
            font-weight: bold;
            letter-spacing: 1px;
        """)
        
        self.usd_price_label.setStyleSheet("""
            color: #22c55e;
            font-size: 26px;
            font-weight: bold;
        """)
        
        self.aud_price_label.setStyleSheet("""
            color: #22c55e;
            font-size: 18px;
        """)
    
    def get_bitcoin_prices(self):
        bitcoin_usd_price = btc()
        bitcoin_aud_price = converter(bitcoin_usd_price)
        
        # puts price on labels
        self.usd_price_label.setText(f"${bitcoin_usd_price:,.2f} USD") # :,.2f puts commas and 2 decimal places
        self.aud_price_label.setText(f"${bitcoin_aud_price:,.2f} AUD")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    exit_code = app.exec()
    sys.exit(exit_code)

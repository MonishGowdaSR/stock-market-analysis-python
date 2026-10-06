import yfinance as yf  # type: ignore
import pandas as pd  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore
import tkinter as tk  # For GUI
from tkinter import Toplevel, PhotoImage  # For custom message box and images


# Function to create a custom message box
def custom_messagebox(title, message):
    # Create a new window
    msg_window = Toplevel()
    msg_window.title(title)
    msg_window.geometry("500x300")  # Set larger size
    msg_window.config(bg="lightyellow")  # Custom background color

    # Add a message label
    label = tk.Label(
        msg_window,
        text=message,
        font=("Helvetica", 14, "bold"),
        bg="lightyellow",
        wraplength=450,
    )
    label.pack(pady=20)

    # Add an OK button to close the window
    ok_button = tk.Button(
        msg_window,
        text="OK",
        font=("Helvetica", 12, "bold"),
        bg="green",
        fg="white",
        command=msg_window.destroy,
    )
    ok_button.pack(pady=20)

    # Keep the message box modal
    msg_window.transient()
    msg_window.grab_set()
    msg_window.wait_window()


# Function to download stock data
def download_data(ticker, start, end):
    try:
        data = yf.download(ticker, start=start, end=end)
        data = data[data.index <= pd.to_datetime(end)]  # Filter data by end date
        if data.empty:
            return None
        return data
    except Exception as e:
        print(f"Error downloading data for '{ticker}': {e}")
        return None


# Visualization Functions
def plot_stock_price(data, ticker):
    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'], label='Close Price', color='blue')
    plt.title(f'{ticker} Closing Prices', fontsize=14, color='darkblue')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Close Price', fontsize=12)
    plt.legend()
    plt.grid()
    plt.show()


def plot_moving_averages(data, ticker):
    data['50_MA'] = data['Close'].rolling(window=50).mean()
    data['200_MA'] = data['Close'].rolling(window=200).mean()
    plt.figure(figsize=(10, 6))
    plt.plot(data['Close'], label='Close Price', color='blue')
    plt.plot(data['50_MA'], label='50-Day MA', color='orange')
    plt.plot(data['200_MA'], label='200-Day MA', color='green')
    plt.title(f'{ticker} Moving Averages', fontsize=14, color='darkblue')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price', fontsize=12)
    plt.legend()
    plt.grid()
    plt.show()


def plot_daily_returns(data, ticker):
    data['Daily Return'] = data['Close'].pct_change()
    plt.figure(figsize=(10, 6))
    plt.plot(data['Daily Return'], label='Daily Returns', color='purple')
    plt.title(f'{ticker} Daily Returns', fontsize=14, color='darkblue')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Daily Return', fontsize=12)
    plt.legend()
    plt.grid()
    plt.show()


def plot_correlation_heatmap(tickers, start_date, end_date):
    stock_data = pd.DataFrame()
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        if not data.empty:
            stock_data[ticker] = data['Close']

    if stock_data.empty:
        print("Error: No valid data for any tickers to generate the heatmap.")
        return

    corr_matrix = stock_data.corr()
    plt.figure(figsize=(10, 7))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title('Stock Price Correlation', fontsize=14, color='darkblue')
    plt.show()


# Function to handle user input
def get_user_input():
    window = tk.Tk()
    window.title("Stock Market Analysis")
    window.geometry("800x500")
    window.config(bg="lightblue")

    # Load and place the logos
    try:
        first_logo = PhotoImage(file="assets/92328-carnivoran-art-nse-market-stock-free-download-image-thumb.png")
        

        first_logo_label = tk.Label(window, image=first_logo, bg="lightblue")
        first_logo_label.grid(row=0, column=0, padx=10, pady=10, columnspan=4)

       

    except Exception as e:
        print(f"Error loading logos: {e}")

    # Input fields
    tk.Label(window, text="Enter Stock Ticker (e.g., AAPL, TSLA):", font=('Helvetica', 12, 'bold'), bg="lightblue").grid(row=1, column=0, pady=10)
    ticker_entry = tk.Entry(window, font=('Helvetica', 12), width=25)
    ticker_entry.grid(row=1, column=1, pady=10)

    tk.Label(window, text="Enter Start Year (YYYY):", font=('Helvetica', 12, 'bold'), bg="lightblue").grid(row=2, column=0, pady=10)
    start_year_entry = tk.Entry(window, font=('Helvetica', 12), width=25)
    start_year_entry.grid(row=2, column=1, pady=10)

    tk.Label(window, text="Enter End Year (YYYY):", font=('Helvetica', 12, 'bold'), bg="lightblue").grid(row=3, column=0, pady=10)
    end_year_entry = tk.Entry(window, font=('Helvetica', 12), width=25)
    end_year_entry.grid(row=3, column=1, pady=10)

    # Submit function
    def submit():
        ticker = ticker_entry.get().strip()
        start_year = start_year_entry.get().strip()
        end_year = end_year_entry.get().strip()

        if not ticker or not start_year.isdigit() or not end_year.isdigit():
            custom_messagebox("Invalid Input", "Please enter valid inputs for all fields.")
            return

        start_date = f"{start_year}-01-01"
        end_date = f"{end_year}-12-31"
        stock_data = download_data(ticker, start_date, end_date)
        if stock_data is None:
            custom_messagebox("Error", f"No data found for ticker '{ticker}'.")
            return

        plot_stock_price(stock_data, ticker)
        plot_moving_averages(stock_data, ticker)
        plot_daily_returns(stock_data, ticker)
        comparison_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', ticker]
        plot_correlation_heatmap(comparison_tickers, start_date, end_date)

        custom_messagebox("THANK  YOU", "Thanks for using this platform. \n\n MONISH GOWDA SR ")
        window.quit()

    # Submit button
    submit_button = tk.Button(window, text="Submit", font=('Helvetica', 14, 'bold'), bg="green", fg="white", command=submit)
    submit_button.grid(row=4, column=0, columnspan=2, pady=20)

    window.mainloop()


if __name__ == "__main__":
    get_user_input()

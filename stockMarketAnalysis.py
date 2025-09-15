import pandas as pd
import yfinance as yf
import re
import questionary
import sys
import webbrowser
import plotly.graph_objects as go

def main():
    """
    Main loop for the stock market analysis tool.
    Presents a menu, handles user selection, and calls the appropriate functions.
    """
    while True:
        selection = ask_menu()
        if selection == "5":
            # Open a web page with a list of stock tickers
            webbrowser.open('https://stockanalysis.com/stocks/')
            continue
        elif selection == "6":
            # Exit the program
            sys.exit()

        tickers = get_tickers()
        if not tickers:
            continue

        data = download_data(tickers)
        if not data:
            continue

        # Call the appropriate charting function based on user selection
        if selection == "1":
            show_line_chart(data)
        elif selection == "2":
            show_area_chart(data)
        elif selection == "3":
            show_moving_averages(data)
        elif selection == "4":
            show_candlestick_chart(data)
        sys.exit()

def ask_menu():
    """
    Display the main menu and return the user's selection.
    """
    action = questionary.select(
        "What do you want to do?",
        choices=[
            "1. Show Line Chart",
            "2. Show Area Chart",
            "3. Analyze Moving Averages",
            "4. View Candlestick Chart",
            "5. Open List of Stock Tickers",
            "6. Exit Program"
        ],
    ).ask()
    return action[0]  # Return the number as a string

def get_tickers():
    """
    Prompt the user to enter one or more stock tickers.
    Returns a list of valid tickers or None to go back.
    """
    while True:
        user_input = input("Enter Stock Ticker(s), or type 'Return' to go back: ").upper()
        if user_input == "RETURN":
            return None
        # Split input by non-word characters (spaces, commas, etc.)
        tickers = [t for t in re.split(r"\W+", user_input) if t]
        valid_tickers = []
        for ticker in tickers:
            try:
                yf.Ticker(ticker)  # Validate ticker format
                valid_tickers.append(ticker)
            except Exception:
                print(f"Invalid stock ticker: {ticker}")
        if valid_tickers:
            return valid_tickers
        print("Please enter at least one valid ticker.")

def get_date(prompt):
    """
    Prompt the user for a date and validate the format.
    Returns the date string or None to go back.
    """
    while True:
        date_input = input(prompt)
        if date_input.upper() == "RETURN":
            return None
        try:
            pd.to_datetime(date_input)
            return date_input
        except ValueError:
            print("Invalid date format. Please enter a valid date (YYYY-MM-DD).")

def download_data(tickers):
    """
    Download historical stock data for the given tickers and date range.
    Returns a dictionary of DataFrames keyed by ticker.
    """
    start_date = get_date("Enter start date (YYYY-MM-DD), or 'Return' to go back: ")
    if not start_date:
        return None
    end_date = get_date("Enter end date (YYYY-MM-DD), or 'Return' to go back: ")
    if not end_date:
        return None

    data = {}
    for ticker in tickers:
        try:
            df = yf.download(ticker, start=start_date, end=end_date)
            if df.empty:
                print(f"No data found for {ticker}.")
                continue
            df = df.reset_index()
            data[ticker] = df
        except Exception as e:
            print(f"Error downloading {ticker}: {e}")
    return data if data else None

def show_line_chart(data):
    """
    Display a line chart of the closing prices for the selected tickers.
    """
    fig = go.Figure()
    for ticker, df in data.items():
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['Close'],
            mode='lines', name=ticker,
            showlegend=True, hoverinfo='all'
        ))
    fig.update_layout(
        title='Stock Market Performance',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=True
    )
    fig.show()

def show_area_chart(data):
    """
    Display an area chart of the closing prices for the selected tickers.
    """
    fig = go.Figure()
    for ticker, df in data.items():
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['Close'],
            mode='lines', name=ticker,
            showlegend=True, hoverinfo='all',
            fill="tonexty"
        ))
    fig.update_layout(
        title='Stock Market Performance',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=True
    )
    fig.show()

def show_moving_averages(data):
    """
    Display a line chart with 10-day and 20-day moving averages for each ticker.
    """
    fig = go.Figure()
    for ticker, df in data.items():
        df['MA10'] = df['Close'].rolling(window=10).mean()
        df['MA20'] = df['Close'].rolling(window=20).mean()
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['Close'],
            mode='lines', name=ticker,
            showlegend=True, hoverinfo='all'
        ))
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['MA10'],
            mode='lines', name=f'{ticker} 10-Day Avg',
            line=dict(color='#004d00', dash='longdash'),
            showlegend=True, hoverinfo='all'
        ))
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['MA20'],
            mode='lines', name=f'{ticker} 20-Day Avg',
            line=dict(color='#800000', dash='longdash'),
            showlegend=True, hoverinfo='all'
        ))
    fig.update_layout(
        title='Stock Market Performance',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=True
    )
    fig.show()

def show_candlestick_chart(data):
    """
    Display a candlestick chart for each ticker, with closing price overlay.
    """
    fig = go.Figure()
    for ticker, df in data.items():
        fig.add_trace(go.Candlestick(
            x=df["Date"], open=df["Open"], high=df["High"],
            low=df["Low"], close=df["Close"],
            name=ticker, showlegend=True
        ))
        fig.add_trace(go.Scatter(
            x=df['Date'], y=df['Close'],
            mode='lines', name=f"{ticker} Close",
            showlegend=True, hoverinfo='all'
        ))
    fig.update_layout(
        title='Stock Market Performance',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=True
    )
    fig.show()

if __name__ == "__main__":
    main()
import pandas as pd
import yfinance as yf
import re, questionary, sys, webbrowser
import plotly.graph_objects as go

def main():
    user_inputs()

def user_inputs():
    selection_input = ask()

    if selection_input == "5":
        webbrowser.open('https://stockanalysis.com/stocks/')
        return user_inputs()
    elif selection_input == "6":
        sys.exit()

    tickers = stock_input()
    if tickers == None:
        return user_inputs()
        
    df_tickers = stock_download(tickers)
    if df_tickers == None:
        return user_inputs()
    
    if selection_input == "1":
        line_chart(df_tickers)
    elif selection_input == "2":
        area_chart(df_tickers)
    elif selection_input == "3":
        moving_area(df_tickers)
    elif selection_input == "4":
        candlestick_graph(df_tickers)
    sys.exit()
    
def stock_input():
    ticker_list = []

    while True:
        try:
            tickers = re.split(r"\W+", input("Enter Stock Ticker(s), 'Return' to return to selection screen: ").upper())

            if 'RETURN' in tickers:
                return None

            for ticker in tickers:
                yf.Ticker(ticker)
                ticker_list.append(ticker)

        except Exception:
            print("Invalid stock ticker. Please enter a valid ticker.")

        return ticker_list

def valid_date(date_check):
    while True:
        try:
            date_input = input(date_check)
            if date_input.upper() == 'RETURN':
                return None
                
            pd.to_datetime(date_input)

        except ValueError:
            print("Invalid date format. Please enter a valid date.")
            continue

        return date_input
        
def stock_download(tickers):
    df_list = {}
    start_date = valid_date("Enter start date (YYYY-MM-DD), 'Return' to return to selection screen: ")
    if start_date == None:
        return user_inputs()
    end_date = valid_date("Enter end date (YYYY-MM-DD), 'Return' to return to selection screen: ")
    if end_date == None:
        return user_inputs()

    while True:
        try:
            for ticker in tickers:
                stock_data = yf.download(ticker, start=start_date, end=end_date, group_by='ticker')
                stock_data = stock_data.reset_index()
                df_list[ticker] = stock_data 
        except (ValueError or TypeError or Exception) as e:
            print(f"Error: {e}. Please enter a valid input.")

        return df_list
   
def line_chart(tickers): 
    fig = go.Figure()

    for ticker, df in tickers.items():
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Close'],
            mode='lines',
            name=ticker,
            showlegend=True,
            hoverinfo='all',
            ))
    
    fig.update_layout(
        title='Stock Market Performance',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=True)
    fig.show()
  
def area_chart(tickers):
    fig = go.Figure()

    for ticker, df in tickers.items():
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Close'],
            mode='lines',
            name=ticker,
            showlegend=True,
            hoverinfo='all',
            fill="tonexty"
            ))
    
    fig.update_layout(
        title='Stock Market Performance',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=True)
    fig.show()

def moving_area(tickers):
    fig = go.Figure()

    for ticker, df in tickers.items():
        df['MA10'] = df['Close'].rolling(window=10).mean().reset_index(0, drop=True)
        df['MA20'] = df['Close'].rolling(window=20).mean().reset_index(0, drop=True)

    for ticker, df in tickers.items():
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Close'],
            mode='lines',
            name=ticker,
            showlegend=True,
            hoverinfo='all',
            ))
        
    for ticker, df in tickers.items():
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['MA10'],
            mode='lines',
            name=f'{ticker} 10-Day Average',
            line=dict(
                color='#004d00',
                dash='longdash'
            ),
            showlegend=True,
            hoverinfo='all',
            ))
        
    for ticker, df in tickers.items():
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['MA20'],
            mode='lines',
            name=f'{ticker} 20-Day Average',
            line=dict(
                color='#800000',
                dash='longdash'
            ),
            showlegend=True,
            hoverinfo='all',
            ))
        
    fig.update_layout(
        title='Stock Market Performance',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=True)

    fig.show()

def candlestick_graph(tickers):
    fig = go.Figure()

    for ticker, df in tickers.items():
        fig.add_trace(go.Candlestick(
            x=df["Date"],
            open=df["Open"], 
            high=df["High"],
            low=df["Low"], 
            close=df["Close"],
            name=ticker,
            showlegend=True))

    for ticker, df in tickers.items():
        fig.add_trace(go.Scatter(
            x=df['Date'],
            y=df['Close'],
            mode='lines',
            name=ticker,
            showlegend=True,
            hoverinfo='all',
            ))
          
    fig.update_layout(
        title='Stock Market Performance',
        xaxis_title='Date',
        yaxis_title='Price',
        xaxis_rangeslider_visible=True)

    fig.show()

def ask():
    action = (
        questionary.select(
            "What do you want to do?",
            choices=["1. Show Line Chart", "2. Show Area Chart", "3. Analyze Moving Averages", "4. View Candlestick Chart", "5. Open List of Stock Tickers", "6. Exit Program"],
        ).ask())

    return action[0]

if __name__=="__main__":
    main()
from fastapi import FastAPI, HTTPException
import yfinance as yf
import pandas as pd

app = FastAPI(title="Advanced Financial Data API")

@app.get("/api/stock/{ticker}")
async def get_stock_data(ticker: str, period: str = "1mo", interval: str = "1d"):
    """
    Fetches historical stock data and basic metadata.
    """
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period, interval=interval)
        
        if hist.empty:
            raise HTTPException(status_code=404, detail="Ticker not found or no data available.")

        # Convert index to string for JSON serialization
        hist.index = hist.index.strftime('%Y-%m-%d %H:%M:%S')
        
        data = {
            "history": hist.reset_index().to_dict(orient="records"),
            "info": {
                "name": stock.info.get("longName"),
                "sector": stock.info.get("sector"),
                "summary": stock.info.get("longBusinessSummary")[:300] + "...",
                "current_price": stock.info.get("currentPrice")
            }
        }
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

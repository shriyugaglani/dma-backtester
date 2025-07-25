from fastapi import APIRouter, Body, HTTPException
from core.backtest import run_full_backtest
from models.schemas import BacktestSummary, BacktestRequest, BacktestResponse
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1", tags=["backtest"])

@router.get("/")
async def root():
    """Root endpoint for API v1"""
    return {"message": "Backtesting SMA APIs - Server is running!"}

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "message": "API is running"}

@router.post("/run-backtest", response_model=BacktestResponse, summary="Run SMA Backtest")
async def run_backtest(request: BacktestRequest = Body(...)):
    """
    Run a Simple Moving Average (SMA) crossover backtest.
    
    - **ticker**: Stock symbol (e.g., AAPL, TSLA)
    - **startDate**: Start date in YYYY-MM-DD format
    - **endDate**: End date in YYYY-MM-DD format  
    - **amount**: Initial investment amount
    
    Returns backtest results including portfolio values, summary statistics, and yearly returns.
    """
    try:
        logger.info(f"Starting backtest for {request.ticker} from {request.startDate} to {request.endDate}")
        
        df, summary, yearly_return = run_full_backtest(
            request.ticker, 
            request.startDate, 
            request.endDate, 
            request.amount
        )
        
        results_df = df[["Date","Portfolio Value", "Cumulative Return"]].copy()
        results_df.columns = ["date", "portfolio_value", "cumulative_return"]
        results_df["date"] = results_df["date"].dt.strftime("%Y-%m-%d")
        
        logger.info(f"Backtest completed for {request.ticker}. Total return: {summary.total_return}")
        
        return {
            "results": results_df.to_dict(orient="records"),
            "summary": summary,
            "yearly_return": yearly_return
        }
        
    except Exception as e:
        logger.error(f"Backtest failed for {request.ticker}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Backtest failed: {str(e)}")
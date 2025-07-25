from pydantic import BaseModel
from typing import List, Dict

class BacktestSummary(BaseModel):
    total_return:str
    annualized_return:str
    max_drawdown:str
    sharpe_ratio:str
    win_rate:str
    num_trades:int
    start_date:str
    end_date:str
    years:str

class BacktestEntry(BaseModel):
    date:str
    portfolio_value:float
    cumulative_return:float
class BacktestRequest(BaseModel):
    ticker:str
    startDate:str
    endDate:str
    amount:int

class BacktestResponse(BaseModel):
    results: List[BacktestEntry]
    summary:BacktestSummary
    yearly_return: Dict[int,float]
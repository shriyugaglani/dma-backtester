# DMA Backtester

A FastAPI application for backtesting Simple Moving Average (SMA) crossover trading strategies, deployed on AWS Lambda using SAM.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Features

- **SMA Crossover Strategy**: Implements a simple moving average crossover trading strategy
- **Real-time Data**: Fetches stock data using yfinance
- **Backtest Analysis**: Provides comprehensive backtest results including:
  - Portfolio value over time
  - Total and annualized returns
  - Maximum drawdown
  - Sharpe ratio
  - Win rate and number of trades
  - Yearly return breakdown
- **RESTful API**: Clean API endpoints for easy integration
- **AWS Lambda**: Serverless deployment for scalability and cost-effectiveness

## API Endpoints

### Health Check
```
GET /health
```
Returns API health status and environment information.

### Run Backtest
```
POST /api/v1/run-backtest
```
Run a SMA crossover backtest with the following parameters:

```json
{
  "ticker": "AAPL",
  "startDate": "2023-01-01",
  "endDate": "2023-12-31",
  "amount": 10000
}
```

Returns:
- `results`: Daily portfolio values and cumulative returns
- `summary`: Backtest statistics (total return, Sharpe ratio, etc.)
- `yearly_return`: Yearly return breakdown

## Local Development

### Prerequisites
- Python 3.11+
- AWS SAM CLI
- pip

### Setup
1. Clone the repository
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```

### Running Locally
```bash
# Using uvicorn (for development)
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Using SAM (for testing Lambda environment)
sam build
sam local start-api
```

### Testing
```bash
# Health check
curl http://localhost:8000/health

# Run backtest
curl -X POST "http://localhost:8000/api/v1/run-backtest" \
  -H "Content-Type: application/json" \
  -d '{"ticker": "AAPL", "startDate": "2023-01-01", "endDate": "2023-12-31", "amount": 10000}'
```

## Deployment

### AWS Deployment
1. Configure AWS credentials
2. Deploy using SAM:
   ```bash
   sam build
   sam deploy --guided
   ```

### Environment Variables
- `ENV`: Environment (development/production)
- `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins

### Frontend Integration
Update the frontend API URL to point to your deployed endpoint:
```javascript
const API_BASE_URL = 'https://your-api-gateway-url.amazonaws.com/Prod';
```

## Project Structure
```
├── app/
│   ├── api/
│   │   └── routes.py          # API endpoints
│   ├── backtest/
│   │   └── engine.py          # Backtesting engine
│   ├── core/
│   │   └── backtest.py        # Core backtest logic
│   ├── data/
│   │   └── fetch_data.py      # Data fetching utilities
│   ├── models/
│   │   └── schemas.py         # Pydantic models
│   ├── strategies/
│   │   └── sma_crossover.py   # SMA strategy implementation
│   ├── main.py                # FastAPI application
│   └── requirements.txt       # Python dependencies
├── dma-dashboard/             # React frontend
├── template.yaml              # SAM template
└── README.md
```

## API Documentation
Once deployed, visit:
- Swagger UI: `https://your-api-url/docs`
- ReDoc: `https://your-api-url/redoc`

## Contributing
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
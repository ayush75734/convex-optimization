"""Market Data Handler"""
import numpy as np
import pandas as pd
import yfinance as yf
from typing import Tuple, Optional
import logging
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class DataHandler:
    """Handles fetching and processing market data."""
    
    def __init__(self, period: str = '5y'):
        """
        Initialize data handler.
        
        Args:
            period: Historical period to fetch ('1mo', '3mo', '1y', '5y', etc.)
        """
        self.period = period
        self.logger = logging.getLogger(__name__)
    
    def get_market_data(
        self,
        symbols: list,
        period: Optional[str] = None
    ) -> Tuple[Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Fetch market data and calculate returns and covariance matrix.
        
        Args:
            symbols: List of asset tickers (e.g., ['AAPL', 'GOOGL', 'MSFT'])
            period: Historical period (uses default if None)
        
        Returns:
            Tuple of (expected_returns, covariance_matrix)
        """
        try:
            if period is None:
                period = self.period
            
            self.logger.info(f"Fetching data for {symbols} with period {period}")
            
            # Download historical price data
            data = yf.download(
                symbols,
                period=period,
                progress=False,
                threads=False
            )
            
            # Handle single symbol case
            if len(symbols) == 1:
                data = data.to_frame(name=symbols[0])
            
            # Get adjusted close prices
            prices = data['Adj Close']
            
            # Calculate daily returns
            returns = prices.pct_change().dropna()
            
            # Handle any missing data
            returns = returns.dropna()
            
            if returns.empty:
                self.logger.error("No valid return data after cleaning")
                return None, None
            
            # Calculate expected returns (annualized)
            expected_returns = returns.mean() * 252  # 252 trading days
            
            # Calculate covariance matrix (annualized)
            cov_matrix = returns.cov() * 252
            
            self.logger.info(f"Successfully processed data for {len(symbols)} assets")
            self.logger.info(f"Expected returns: {expected_returns.to_dict()}")
            
            return expected_returns.values, cov_matrix.values
            
        except Exception as e:
            self.logger.error(f"Error fetching market data: {str(e)}")
            return None, None
    
    def validate_symbols(self, symbols: list) -> bool:
        """
        Validate that symbols exist and have data.
        
        Args:
            symbols: List of tickers to validate
        
        Returns:
            True if all symbols are valid
        """
        try:
            for symbol in symbols:
                data = yf.download(symbol, period='1d', progress=False, threads=False)
                if data.empty:
                    self.logger.warning(f"No data found for symbol {symbol}")
                    return False
            return True
        except Exception as e:
            self.logger.error(f"Validation error: {str(e)}")
            return False

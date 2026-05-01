"""Flask API for Portfolio Optimization"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from optimizer import PortfolioOptimizer
from data_handler import DataHandler
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize handlers
optimizer = PortfolioOptimizer()
data_handler = DataHandler()


@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200


@app.route('/api/optimize', methods=['POST'])
def optimize_portfolio():
    """
    Optimize portfolio given:
    - symbols: list of asset symbols
    - target_return: target expected return
    - risk_free_rate: risk-free rate (default 0.02)
    - allow_short_selling: boolean (default False)
    
    Returns:
    - optimal_weights: optimal portfolio weights
    - expected_return: portfolio expected return
    - volatility: portfolio standard deviation
    - sharpe_ratio: Sharpe ratio
    """
    try:
        data = request.json
        symbols = data.get('symbols', [])
        target_return = data.get('target_return', 0.10)
        risk_free_rate = data.get('risk_free_rate', 0.02)
        allow_short_selling = data.get('allow_short_selling', False)
        
        # Validate input
        if not symbols or len(symbols) < 2:
            return jsonify({'error': 'At least 2 symbols required'}), 400
        
        # Fetch market data
        logger.info(f"Fetching data for symbols: {symbols}")
        returns_data, cov_matrix = data_handler.get_market_data(symbols)
        
        if returns_data is None:
            return jsonify({'error': 'Failed to fetch market data'}), 500
        
        # Run optimization
        logger.info(f"Running optimization for {len(symbols)} assets")
        result = optimizer.optimize(
            returns_data,
            cov_matrix,
            target_return,
            risk_free_rate,
            allow_short_selling
        )
        
        if result is None:
            return jsonify({'error': 'Optimization failed'}), 500
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in optimize_portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/efficient-frontier', methods=['POST'])
def efficient_frontier():
    """
    Calculate efficient frontier for given assets.
    
    Returns multiple portfolios along the efficient frontier.
    """
    try:
        data = request.json
        symbols = data.get('symbols', [])
        num_points = data.get('num_points', 20)
        risk_free_rate = data.get('risk_free_rate', 0.02)
        
        if not symbols or len(symbols) < 2:
            return jsonify({'error': 'At least 2 symbols required'}), 400
        
        # Fetch market data
        logger.info(f"Calculating efficient frontier for {symbols}")
        returns_data, cov_matrix = data_handler.get_market_data(symbols)
        
        if returns_data is None:
            return jsonify({'error': 'Failed to fetch market data'}), 500
        
        # Calculate frontier
        frontier = optimizer.efficient_frontier(
            returns_data,
            cov_matrix,
            risk_free_rate,
            num_points
        )
        
        return jsonify(frontier), 200
        
    except Exception as e:
        logger.error(f"Error in efficient_frontier: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/sharpe-ratio-portfolio', methods=['POST'])
def sharpe_ratio_portfolio():
    """
    Find portfolio with maximum Sharpe ratio.
    """
    try:
        data = request.json
        symbols = data.get('symbols', [])
        risk_free_rate = data.get('risk_free_rate', 0.02)
        allow_short_selling = data.get('allow_short_selling', False)
        
        if not symbols or len(symbols) < 2:
            return jsonify({'error': 'At least 2 symbols required'}), 400
        
        # Fetch market data
        logger.info(f"Finding max Sharpe ratio portfolio for {symbols}")
        returns_data, cov_matrix = data_handler.get_market_data(symbols)
        
        if returns_data is None:
            return jsonify({'error': 'Failed to fetch market data'}), 500
        
        # Find max Sharpe portfolio
        result = optimizer.max_sharpe_ratio(
            returns_data,
            cov_matrix,
            risk_free_rate,
            allow_short_selling
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in sharpe_ratio_portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500


@app.route('/api/min-variance-portfolio', methods=['POST'])
def min_variance_portfolio():
    """
    Find portfolio with minimum variance.
    """
    try:
        data = request.json
        symbols = data.get('symbols', [])
        allow_short_selling = data.get('allow_short_selling', False)
        
        if not symbols or len(symbols) < 2:
            return jsonify({'error': 'At least 2 symbols required'}), 400
        
        # Fetch market data
        logger.info(f"Finding minimum variance portfolio for {symbols}")
        returns_data, cov_matrix = data_handler.get_market_data(symbols)
        
        if returns_data is None:
            return jsonify({'error': 'Failed to fetch market data'}), 500
        
        # Find min variance portfolio
        result = optimizer.min_variance(
            returns_data,
            cov_matrix,
            allow_short_selling
        )
        
        return jsonify(result), 200
        
    except Exception as e:
        logger.error(f"Error in min_variance_portfolio: {str(e)}")
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)

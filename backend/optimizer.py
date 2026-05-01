"""Portfolio Optimization using Convex Optimization"""
import numpy as np
import cvxpy as cp
from typing import Dict, List, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class PortfolioOptimizer:
    """Solves portfolio optimization problems using convex optimization."""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def optimize(
        self,
        returns: np.ndarray,
        cov_matrix: np.ndarray,
        target_return: float,
        risk_free_rate: float = 0.02,
        allow_short_selling: bool = False
    ) -> Optional[Dict]:
        """
        Minimize portfolio variance subject to:
        - Target expected return constraint
        - Budget constraint (weights sum to 1)
        - Optional: Non-negativity constraint (no short selling)
        
        This is a convex quadratic program:
        minimize:    w^T * Σ * w
        subject to:  μ^T * w >= target_return
                     1^T * w = 1
                     w >= 0 (if no_short_selling)
        
        where:
          w: portfolio weights
          Σ: covariance matrix (convex objective)
          μ: expected returns
        """
        try:
            n_assets = len(returns)
            
            # Define optimization variable
            weights = cp.Variable(n_assets)
            
            # Objective: minimize portfolio variance
            # Portfolio variance = w^T * Σ * w (quadratic, convex)
            portfolio_variance = cp.quad_form(weights, cov_matrix)
            objective = cp.Minimize(portfolio_variance)
            
            # Constraints
            constraints = [
                cp.sum(weights) == 1,  # Budget constraint
                returns @ weights >= target_return,  # Return constraint
            ]
            
            # Non-negativity constraint (no short selling)
            if not allow_short_selling:
                constraints.append(weights >= 0)
            
            # Solve convex optimization problem
            problem = cp.Problem(objective, constraints)
            problem.solve(solver=cp.ECOS, verbose=False)
            
            if problem.status != cp.OPTIMAL:
                self.logger.warning(f"Optimization status: {problem.status}")
                return None
            
            # Extract results
            w = weights.value
            expected_return = float(returns @ w)
            volatility = float(np.sqrt(w @ cov_matrix @ w))
            sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility > 0 else 0
            
            return {
                'status': 'success',
                'weights': w.tolist(),
                'expected_return': expected_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'variance': float(w @ cov_matrix @ w)
            }
            
        except Exception as e:
            self.logger.error(f"Optimization error: {str(e)}")
            return None
    
    def efficient_frontier(
        self,
        returns: np.ndarray,
        cov_matrix: np.ndarray,
        risk_free_rate: float = 0.02,
        num_points: int = 20
    ) -> Dict:
        """
        Calculate multiple points along the efficient frontier.
        
        Returns a list of portfolios with varying risk-return profiles.
        """
        try:
            # Get min and max possible returns
            min_return = np.min(returns)
            max_return = np.max(returns)
            
            # Generate target returns
            target_returns = np.linspace(min_return, max_return, num_points)
            
            frontier_data = {
                'efficient_frontier': [],
                'status': 'success'
            }
            
            for target_ret in target_returns:
                result = self.optimize(returns, cov_matrix, target_ret, risk_free_rate)
                if result and result['status'] == 'success':
                    frontier_data['efficient_frontier'].append({
                        'return': result['expected_return'],
                        'volatility': result['volatility'],
                        'sharpe_ratio': result['sharpe_ratio']
                    })
            
            return frontier_data
            
        except Exception as e:
            self.logger.error(f"Efficient frontier error: {str(e)}")
            return {'status': 'error', 'error': str(e)}
    
    def max_sharpe_ratio(
        self,
        returns: np.ndarray,
        cov_matrix: np.ndarray,
        risk_free_rate: float = 0.02,
        allow_short_selling: bool = False
    ) -> Optional[Dict]:
        """
        Maximize Sharpe ratio: (μ^T*w - rf) / sqrt(w^T*Σ*w)
        
        Equivalent to finding the tangency portfolio.
        This is solved via convex optimization transformation.
        """
        try:
            n_assets = len(returns)
            
            # Use change of variables: y = w / (w^T*1) for portfolio weights
            # Maximize Sharpe = (μ^T*y - rf) / sqrt(y^T*Σ*y)
            # Equivalent to minimizing y^T*Σ*y subject to μ^T*y = 1
            
            y = cp.Variable(n_assets)
            
            # Objective: minimize variance of normalized portfolio
            objective = cp.Minimize(cp.quad_form(y, cov_matrix))
            
            # Constraints
            constraints = [
                (returns - risk_free_rate) @ y == 1,  # Normalization
            ]
            
            if not allow_short_selling:
                constraints.append(y >= 0)
            
            problem = cp.Problem(objective, constraints)
            problem.solve(solver=cp.ECOS, verbose=False)
            
            if problem.status != cp.OPTIMAL:
                return None
            
            # Recover original weights
            y_val = y.value
            weights = y_val / np.sum(y_val)
            
            expected_return = float(returns @ weights)
            volatility = float(np.sqrt(weights @ cov_matrix @ weights))
            sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility > 0 else 0
            
            return {
                'status': 'success',
                'weights': weights.tolist(),
                'expected_return': expected_return,
                'volatility': volatility,
                'sharpe_ratio': sharpe_ratio,
                'portfolio_type': 'max_sharpe_ratio'
            }
            
        except Exception as e:
            self.logger.error(f"Max Sharpe ratio error: {str(e)}")
            return None
    
    def min_variance(
        self,
        returns: np.ndarray,
        cov_matrix: np.ndarray,
        allow_short_selling: bool = False
    ) -> Optional[Dict]:
        """
        Find minimum variance portfolio.
        
        minimize:    w^T * Σ * w
        subject to:  1^T * w = 1
                     w >= 0 (if no_short_selling)
        """
        try:
            n_assets = len(returns)
            weights = cp.Variable(n_assets)
            
            # Objective: minimize variance
            objective = cp.Minimize(cp.quad_form(weights, cov_matrix))
            
            # Constraints
            constraints = [cp.sum(weights) == 1]
            
            if not allow_short_selling:
                constraints.append(weights >= 0)
            
            problem = cp.Problem(objective, constraints)
            problem.solve(solver=cp.ECOS, verbose=False)
            
            if problem.status != cp.OPTIMAL:
                return None
            
            w = weights.value
            expected_return = float(returns @ w)
            volatility = float(np.sqrt(w @ cov_matrix @ w))
            
            return {
                'status': 'success',
                'weights': w.tolist(),
                'expected_return': expected_return,
                'volatility': volatility,
                'portfolio_type': 'min_variance'
            }
            
        except Exception as e:
            self.logger.error(f"Min variance error: {str(e)}")
            return None

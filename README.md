# Convex Optimization: Portfolio Optimizer

A real-world application of convex optimization principles to solve the portfolio optimization problem - minimizing investment risk while achieving target returns.

## 📊 Problem Statement

Given:
- N assets with historical returns and volatilities
- Target expected return
- Risk-free rate
- Budget constraint (weights sum to 1)
- Optional: No short-selling constraint (weights ≥ 0)

Find: Optimal portfolio weights that minimize risk (variance) subject to constraints

## 🎯 Key Concepts

### Convex Optimization Properties:
1. **Objective Function**: Portfolio variance (convex quadratic)
2. **Constraints**: Linear (budget, non-negativity)
3. **Solver**: Interior-point methods
4. **Guarantee**: Any local minimum is global minimum

## 🏗️ Project Structure

```
convex-optimization/
├── backend/              # Python Flask API
│   ├── app.py           # Main application
│   ├���─ optimizer.py     # Convex optimization logic
│   ├── data_handler.py  # Market data processing
│   └── requirements.txt
├── frontend/            # React Dashboard
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── services/
│   └── package.json
└── docs/               # Documentation
```

## 🚀 Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

## ✨ Features

- ✅ Efficient frontier calculation
- ✅ Minimum variance portfolio
- ✅ Maximum Sharpe ratio portfolio
- ✅ Risk-Return visualization
- ✅ Real market data integration
- ✅ Constraint handling (budget, bounds)
- ✅ Portfolio performance metrics

## 🔧 Technologies

- **Backend**: Python, CVXPY, NumPy, Flask
- **Frontend**: React, Plotly, TypeScript
- **Data**: yfinance for real market data
- **Optimization**: CVXPY (supports multiple solvers)

## 📚 References

- Markowitz Portfolio Theory
- Convex Optimization (Boyd & Vandenberghe)
- Modern Portfolio Theory

import React, { useState } from 'react';
import PortfolioForm from './components/PortfolioForm';
import PortfolioResults from './components/PortfolioResults';
import EfficientFrontier from './components/EfficientFrontier';
import './App.css';

interface PortfolioData {
  status: string;
  weights: number[];
  expected_return: number;
  volatility: number;
  sharpe_ratio: number;
}

interface FrontierData {
  efficient_frontier: Array<{
    return: number;
    volatility: number;
    sharpe_ratio: number;
  }>;
}

function App() {
  const [portfolioResult, setPortfolioResult] = useState<PortfolioData | null>(null);
  const [frontierData, setFrontierData] = useState<FrontierData | null>(null);
  const [symbols, setSymbols] = useState<string[]>(['AAPL', 'GOOGL', 'MSFT']);
  const [loading, setLoading] = useState(false);

  const handleOptimize = async (data: {
    symbols: string[];
    targetReturn: number;
    riskFreeRate: number;
    allowShortSelling: boolean;
  }) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/optimize', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbols: data.symbols,
          target_return: data.targetReturn,
          risk_free_rate: data.riskFreeRate,
          allow_short_selling: data.allowShortSelling,
        }),
      });
      const result = await response.json();
      setPortfolioResult(result);
      setSymbols(data.symbols);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFrontier = async (data: { symbols: string[]; riskFreeRate: number }) => {
    setLoading(true);
    try {
      const response = await fetch('http://localhost:5000/api/efficient-frontier', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          symbols: data.symbols,
          risk_free_rate: data.riskFreeRate,
          num_points: 20,
        }),
      });
      const result = await response.json();
      setFrontierData(result);
      setSymbols(data.symbols);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🎯 Portfolio Optimizer</h1>
        <p>Convex Optimization for Efficient Portfolio Management</p>
      </header>

      <div className="container">
        <div className="sidebar">
          <PortfolioForm
            onOptimize={handleOptimize}
            onFrontier={handleFrontier}
            loading={loading}
          />
        </div>

        <div className="main-content">
          {portfolioResult && <PortfolioResults result={portfolioResult} symbols={symbols} />}
          {frontierData && <EfficientFrontier data={frontierData} />}
          {!portfolioResult && !frontierData && (
            <div className="placeholder">
              <p>Fill in the form and click optimize to see results</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;

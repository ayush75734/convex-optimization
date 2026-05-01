import React, { useState } from 'react';

interface PortfolioFormProps {
  onOptimize: (data: any) => void;
  onFrontier: (data: any) => void;
  loading: boolean;
}

function PortfolioForm({ onOptimize, onFrontier, loading }: PortfolioFormProps) {
  const [symbols, setSymbols] = useState<string>('AAPL,GOOGL,MSFT,AMZN');
  const [targetReturn, setTargetReturn] = useState(0.12);
  const [riskFreeRate, setRiskFreeRate] = useState(0.02);
  const [allowShortSelling, setAllowShortSelling] = useState(false);

  const handleOptimizeClick = () => {
    const symbolArray = symbols.split(',').map(s => s.trim().toUpperCase());
    onOptimize({
      symbols: symbolArray,
      targetReturn,
      riskFreeRate,
      allowShortSelling,
    });
  };

  const handleFrontierClick = () => {
    const symbolArray = symbols.split(',').map(s => s.trim().toUpperCase());
    onFrontier({
      symbols: symbolArray,
      riskFreeRate,
    });
  };

  return (
    <form className="portfolio-form">
      <h2>Portfolio Configuration</h2>

      <div className="form-group">
        <label htmlFor="symbols">Asset Symbols (comma-separated)</label>
        <input
          id="symbols"
          type="text"
          value={symbols}
          onChange={(e) => setSymbols(e.target.value)}
          placeholder="e.g., AAPL,GOOGL,MSFT"
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="targetReturn">Target Return: {(targetReturn * 100).toFixed(1)}%</label>
        <input
          id="targetReturn"
          type="range"
          min="0"
          max="0.5"
          step="0.01"
          value={targetReturn}
          onChange={(e) => setTargetReturn(parseFloat(e.target.value))}
          disabled={loading}
        />
      </div>

      <div className="form-group">
        <label htmlFor="riskFreeRate">Risk-Free Rate: {(riskFreeRate * 100).toFixed(2)}%</label>
        <input
          id="riskFreeRate"
          type="range"
          min="0"
          max="0.1"
          step="0.001"
          value={riskFreeRate}
          onChange={(e) => setRiskFreeRate(parseFloat(e.target.value))}
          disabled={loading}
        />
      </div>

      <div className="form-group checkbox">
        <label>
          <input
            type="checkbox"
            checked={allowShortSelling}
            onChange={(e) => setAllowShortSelling(e.target.checked)}
            disabled={loading}
          />
          Allow Short Selling
        </label>
      </div>

      <button
        type="button"
        onClick={handleOptimizeClick}
        disabled={loading}
        className="btn btn-primary"
      >
        {loading ? 'Optimizing...' : 'Optimize Portfolio'}
      </button>

      <button
        type="button"
        onClick={handleFrontierClick}
        disabled={loading}
        className="btn btn-secondary"
      >
        {loading ? 'Loading...' : 'Show Efficient Frontier'}
      </button>
    </form>
  );
}

export default PortfolioForm;

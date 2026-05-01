import React from 'react';

interface PortfolioResultsProps {
  result: {
    status: string;
    weights: number[];
    expected_return: number;
    volatility: number;
    sharpe_ratio: number;
  };
  symbols: string[];
}

function PortfolioResults({ result, symbols }: PortfolioResultsProps) {
  if (!result || result.status !== 'success') {
    return <div>Error: Invalid result</div>;
  }

  return (
    <div className="results-panel">
      <h2>Optimal Portfolio</h2>

      <div className="metrics-grid">
        <div className="metric">
          <span className="metric-label">Expected Return</span>
          <span className="metric-value">{(result.expected_return * 100).toFixed(2)}%</span>
        </div>
        <div className="metric">
          <span className="metric-label">Volatility (Risk)</span>
          <span className="metric-value">{(result.volatility * 100).toFixed(2)}%</span>
        </div>
        <div className="metric">
          <span className="metric-label">Sharpe Ratio</span>
          <span className="metric-value">{result.sharpe_ratio.toFixed(3)}</span>
        </div>
      </div>

      <h3>Portfolio Allocation</h3>
      <div className="allocation-table">
        <table>
          <thead>
            <tr>
              <th>Asset</th>
              <th>Weight</th>
              <th>Allocation</th>
            </tr>
          </thead>
          <tbody>
            {symbols.map((symbol, idx) => (
              <tr key={symbol}>
                <td>{symbol}</td>
                <td>{(result.weights[idx] * 100).toFixed(2)}%</td>
                <td>
                  <div className="allocation-bar">
                    <div
                      className="allocation-fill"
                      style={{ width: `${result.weights[idx] * 100}%` }}
                    />
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default PortfolioResults;

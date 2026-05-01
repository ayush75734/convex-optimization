import React from 'react';
import Plot from 'react-plotly.js';

interface EfficientFrontierProps {
  data: {
    efficient_frontier: Array<{
      return: number;
      volatility: number;
      sharpe_ratio: number;
    }>;
  };
}

function EfficientFrontier({ data }: EfficientFrontierProps) {
  if (!data || !data.efficient_frontier || data.efficient_frontier.length === 0) {
    return <div>No frontier data available</div>;
  }

  const frontierData = data.efficient_frontier;
  
  const plotData = [
    {
      x: frontierData.map(p => p.volatility * 100),
      y: frontierData.map(p => p.return * 100),
      mode: 'lines+markers',
      type: 'scatter',
      name: 'Efficient Frontier',
      line: {
        color: 'rgb(31, 119, 180)',
        width: 3,
      },
      marker: {
        size: 6,
        color: frontierData.map(p => p.sharpe_ratio),
        colorscale: 'Viridis',
        showscale: true,
        colorbar: {
          title: 'Sharpe Ratio',
        },
      },
    },
  ];

  const layout = {
    title: 'Efficient Frontier',
    xaxis: {
      title: 'Volatility (Risk) %',
    },
    yaxis: {
      title: 'Expected Return %',
    },
    hovermode: 'closest',
  };

  return (
    <div className="frontier-panel">
      <Plot
        data={plotData}
        layout={layout}
        style={{ width: '100%', height: '500px' }}
      />
    </div>
  );
}

export default EfficientFrontier;

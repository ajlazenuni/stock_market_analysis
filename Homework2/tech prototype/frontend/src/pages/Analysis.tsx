// src/pages/Analysis.tsx
import React, { useEffect, useState } from 'react';
import { Sidebar } from '../components/Sidebar';
import { StockChart } from '../components/StockChart';
import { api, StockData, TechnicalAnalysisData } from '../utilts/api';

interface Indicator {
  key: string;
  name: string;
}

interface AvailableIndicators {
  oscillators: Indicator[];
  moving_averages: Indicator[];
  time_periods: Indicator[];
}

export default function Analysis() {
  const [symbols, setSymbols] = useState<string[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState<string>('');
  const [selectedPeriod, setSelectedPeriod] = useState('daily');
  const [stockData, setStockData] = useState<StockData[]>([]);
  const [technicalData, setTechnicalData] = useState<TechnicalAnalysisData | null>(null);
  const [availableIndicators, setAvailableIndicators] = useState<AvailableIndicators | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const fetchInitialData = async () => {
      const [symbolsData, indicators] = await Promise.all([
        api.getSymbols(),
        api.getAvailableIndicators()
      ]);
      setSymbols(symbolsData);
      setAvailableIndicators(indicators);
    };
    fetchInitialData();
  }, []);

  const handleGenerate = async () => {
    if (!selectedSymbol) return;
    
    setLoading(true);
    try {
      const [history, analysis] = await Promise.all([
        api.getStockHistory(selectedSymbol),
        api.getTechnicalAnalysis(selectedSymbol, selectedPeriod)
      ]);
      
      setStockData(history);
      setTechnicalData(analysis);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen">
      <Sidebar />
      
      <div className="flex-1 p-8 overflow-auto">
        <h1 className="text-2xl font-bold mb-8">Technical Analysis</h1>
        
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Symbol
            </label>
            <select
              className="w-full border rounded-md p-2"
              value={selectedSymbol}
              onChange={(e) => setSelectedSymbol(e.target.value)}
            >
              <option value="">Select Symbol</option>
              {symbols.map(symbol => (
                <option key={symbol} value={symbol}>{symbol}</option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Time Period
            </label>
            <select
              className="w-full border rounded-md p-2"
              value={selectedPeriod}
              onChange={(e) => setSelectedPeriod(e.target.value)}
            >
              {availableIndicators?.time_periods.map(period => (
                <option key={period.key} value={period.key}>
                  {period.name}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={handleGenerate}
              disabled={!selectedSymbol || loading}
              className="w-full bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:bg-blue-400"
            >
              {loading ? 'Loading...' : 'Generate Analysis'}
            </button>
          </div>
        </div>

        {technicalData && (
          <div className="grid grid-cols-2 gap-6 mb-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4">Current Signal</h2>
              <div className={`text-2xl font-bold ${
                technicalData.current_signal === 'Buy' ? 'text-green-500' : 
                technicalData.current_signal === 'Sell' ? 'text-red-500' : 
                'text-yellow-500'
              }`}>
                {technicalData.current_signal}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h2 className="text-lg font-semibold mb-4">Key Indicators</h2>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-sm text-gray-500">RSI</div>
                  <div className="text-lg font-semibold">
                    {technicalData.indicators.RSI.toFixed(2)}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">MACD</div>
                  <div className="text-lg font-semibold">
                    {technicalData.indicators.MACD.toFixed(2)}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">SMA 50</div>
                  <div className="text-lg font-semibold">
                    {technicalData.indicators.SMA_50.toFixed(2)}
                  </div>
                </div>
                <div>
                  <div className="text-sm text-gray-500">SMA 200</div>
                  <div className="text-lg font-semibold">
                    {technicalData.indicators.SMA_200.toFixed(2)}
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {stockData.length > 0 && (
          <>
            <div className="mb-6">
              <StockChart 
                data={stockData} 
                dataKey="last_trade_price"
                height={400}
              />
            </div>
            
            {technicalData && (
              <div className="mb-6">
                <h2 className="text-lg font-semibold mb-4">Technical Indicators</h2>
                <div className="grid grid-cols-2 gap-6">
                  <StockChart 
                    data={Object.entries(technicalData.historical_data).map(([date, data]) => ({
                      date,
                      RSI: data.RSI
                    }))}
                    dataKey="RSI"
                    height={200}
                  />
                  <StockChart 
                    data={Object.entries(technicalData.historical_data).map(([date, data]) => ({
                      date,
                      Close: data.Close
                    }))}
                    dataKey="Close"
                    height={200}
                  />
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
}
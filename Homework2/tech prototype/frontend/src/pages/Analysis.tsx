
import React, { useEffect, useState } from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';
import { api, StockData } from '../utilts/api';

export default function Analysis() {
  const [symbols, setSymbols] = useState<string[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState<string>('');
  const [stockData, setStockData] = useState<StockData[]>([]);

  useEffect(() => {
    api.getSymbols().then(setSymbols);
  }, []);

  useEffect(() => {
    if (selectedSymbol) {
      api.getStockHistory(selectedSymbol).then(setStockData);
    }
  }, [selectedSymbol]);

  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 text-white p-6">
        <div className="mb-8">
          <h1 className="text-xl font-bold">MSE Analysis</h1>
        </div>
        <nav className="space-y-4">
          <a href="/" className="block py-2 px-4 hover:bg-gray-700 rounded">Dashboard</a>
          <a href="/analysis" className="block py-2 px-4 bg-blue-600 rounded">Analysis</a>
          <a href="/reports" className="block py-2 px-4 hover:bg-gray-700 rounded">Reports</a>
        </nav>
      </div>

      <div className="flex-1 p-6">
        <select 
          className="mb-6 border rounded p-2 w-48"
          value={selectedSymbol}
          onChange={(e) => setSelectedSymbol(e.target.value)}
        >
          <option value="">Select Symbol</option>
          {symbols.map(symbol => (
            <option key={symbol} value={symbol}>{symbol}</option>
          ))}
        </select>

        {selectedSymbol && (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold mb-4">{selectedSymbol} Price History</h2>
            <div className="h-96">
              <ResponsiveContainer width="100%" height="100%">
                <LineChart data={stockData}>
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line type="monotone" dataKey="last_trade_price" stroke="#4F46E5" />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
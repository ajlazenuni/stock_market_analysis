import React, { useEffect, useState } from 'react';
import { StockData, api } from '../utilts/api';

export default function Reports() {
  const [symbols, setSymbols] = useState<string[]>([]);
  const [selectedSymbol, setSelectedSymbol] = useState<string>('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [stockData, setStockData] = useState<StockData[]>([]);
  const [loading, setLoading] = useState(false);

  // Helper function to get formatted date for last N days
  const getDateNDaysAgo = (days: number) => {
    const date = new Date();
    date.setDate(date.getDate() - days);
    return date.toISOString().split('T')[0];
  };

  // Load initial data
  useEffect(() => {
    const fetchInitialData = async () => {
      try {
        setLoading(true);
        // Set initial dates
        const endDate = new Date().toISOString().split('T')[0];
        const startDate = getDateNDaysAgo(2);
        setStartDate(startDate);
        setEndDate(endDate);

        // Get symbols and data
        const symbols = await api.getSymbols();
        setSymbols(symbols);
        
        // Fetch data for all symbols
        const allData = await api.getStockHistory('', startDate, endDate);
        setStockData(allData);
      } catch (error) {
        console.error('Error fetching initial data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchInitialData();
  }, []);

  const handleFilter = async () => {
    try {
      setLoading(true);
      const data = await api.getStockHistory(selectedSymbol, startDate, endDate);
      setStockData(data);
    } catch (error) {
      console.error('Error applying filters:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex h-screen">
      {/* Sidebar remains the same */}
      <div className="w-64 bg-gray-800 text-white p-6">
        <div className="mb-8">
          <h1 className="text-xl font-bold">MSE Analysis</h1>
        </div>
        <nav className="space-y-4">
          <a href="/" className="block py-2 px-4 hover:bg-gray-700 rounded">Dashboard</a>
          <a href="/analysis" className="block py-2 px-4 hover:bg-gray-700 rounded">Analysis</a>
          <a href="/reports" className="block py-2 px-4 bg-blue-600 rounded">Reports</a>
        </nav>
      </div>

      <div className="flex-1">
        <div className="p-6">
          <div className="bg-white rounded-lg shadow p-4 mb-6">
            <div className="flex items-center gap-4">
              <select
                className="border rounded p-2 w-48"
                value={selectedSymbol}
                onChange={(e) => setSelectedSymbol(e.target.value)}
              >
                <option value="">All Symbols</option>
                {symbols.map(symbol => (
                  <option key={symbol} value={symbol}>{symbol}</option>
                ))}
              </select>
              <input
                type="date"
                className="border rounded p-2"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
              <input
                type="date"
                className="border rounded p-2"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
              <button
                onClick={handleFilter}
                className="px-4 py-2 bg-blue-600 text-white rounded disabled:bg-blue-400"
                disabled={loading}
              >
                {loading ? 'Loading...' : 'Apply Filters'}
              </button>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow overflow-hidden">
            {loading ? (
              <div className="p-4 text-center">Loading...</div>
            ) : stockData.length === 0 ? (
              <div className="p-4 text-center">No data found for the selected criteria</div>
            ) : (
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Date</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Symbol</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Price</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">High</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Low</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Change %</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Volume</th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {stockData.map((row, i) => (
                    <tr key={i}>
                      <td className="px-6 py-4">{row.date}</td>
                      <td className="px-6 py-4">{row.symbol}</td>
                      <td className="px-6 py-4">{row.last_trade_price.toFixed(2)}</td>
                      <td className="px-6 py-4">{row.max_price.toFixed(2)}</td>
                      <td className="px-6 py-4">{row.min_price.toFixed(2)}</td>
                      <td className={`px-6 py-4 ${
                        row.change_percentage > 0 ? 'text-green-500' : 'text-red-500'
                      }`}>
                        {row.change_percentage.toFixed(2)}%
                      </td>
                      <td className="px-6 py-4">{row.volume.toLocaleString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
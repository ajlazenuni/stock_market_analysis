import React, { useEffect, useState } from "react";
import { api, MarketSummary, StockData } from "../utilts/api";

export default function Dashboard() {
  const [latestPrices, setLatestPrices] = useState<StockData[]>([]);
  const [marketSummary, setMarketSummary] = useState<MarketSummary>({
    total_stocks: 0,
    total_volume: 0,
    avg_change: 0
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        const [prices, summary] = await Promise.all([
          api.getLatestPrices(),
          api.getMarketSummary(),
        ]);
        setLatestPrices(prices);
        setMarketSummary(summary);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
        console.error("Error fetching dashboard data:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  if (loading) {
    return <div className="flex h-screen items-center justify-center">Loading...</div>;
  }

  if (error) {
    return <div className="flex h-screen items-center justify-center text-red-500">{error}</div>;
  }
  return (
    <div className="flex h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-gray-800 text-white p-6">
        <div className="mb-8">
          <h1 className="text-xl font-bold">MSE Analysis</h1>
        </div>
        <nav className="space-y-4">
          <a href="/" className="block py-2 px-4 bg-blue-600 rounded">
            Dashboard
          </a>
          <a
            href="/analysis"
            className="block py-2 px-4 hover:bg-gray-700 rounded"
          >
            Analysis
          </a>
          <a
            href="/reports"
            className="block py-2 px-4 hover:bg-gray-700 rounded"
          >
            Reports
          </a>
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1 overflow-auto">
        <header className="bg-white shadow p-4">
          <div className="flex justify-between items-center">
            <h2 className="text-xl font-semibold">Market Overview</h2>
          </div>
        </header>

        <main className="p-6">
          {/* Stats Grid */}
          <div className="grid grid-cols-4 gap-6 mb-6">
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="text-gray-500 text-sm">Total Stocks</h3>
              <p className="text-2xl font-bold mt-2">
                {marketSummary?.total_stocks || 0}
              </p>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="text-gray-500 text-sm">Total Volume</h3>
              <p className="text-2xl font-bold mt-2">
                {marketSummary?.total_volume.toLocaleString() || 0}
              </p>
            </div>
            <div className="bg-white rounded-lg shadow p-4">
              <h3 className="text-gray-500 text-sm">Average Change</h3>
              <p
                className={`text-2xl font-bold mt-2 ${
                  (marketSummary?.avg_change || 0) > 0
                    ? "text-green-500"
                    : "text-red-500"
                }`}
              >
                {(marketSummary?.avg_change || 0).toFixed(2)}%
              </p>
            </div>
          </div>

          {/* Stock Grid */}
          <div className="grid grid-cols-3 gap-6">
            {latestPrices.map((stock) => (
              <div
                key={stock.symbol}
                className="bg-white rounded-lg shadow p-4"
              >
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="font-bold text-lg">{stock.symbol}</h3>
                    <p className="text-2xl">
                      {stock.last_trade_price.toFixed(2)}
                    </p>
                  </div>
                  <span
                    className={`${
                      stock.change_percentage > 0
                        ? "text-green-500"
                        : "text-red-500"
                    }`}
                  >
                    {stock.change_percentage > 0 ? "+" : ""}
                    {stock.change_percentage.toFixed(2)}%
                  </span>
                </div>
                <div className="mt-2">
                  <div className="grid grid-cols-2 gap-2 text-sm text-gray-500">
                    <div>High: {stock.max_price}</div>
                    <div>Low: {stock.min_price}</div>
                    <div>Volume: {stock.volume.toLocaleString()}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}

// src/utils/api.ts

export interface StockData {
    date: string;
    symbol: string;
    last_trade_price: number;
    max_price: number;
    min_price: number;
    avg_price: number;
    change_percentage: number;
    volume: number;
  }
  
  export interface MarketSummary {
    total_stocks: number;
    total_volume: number;
    avg_change: number;
  }
  
  const BASE_URL = 'http://localhost:3000';
  
  export const api = {
    // Add getSymbols function
    getSymbols: async (): Promise<string[]> => {
      try {
        const res = await fetch(`${BASE_URL}/stocks/symbols`);
        if (!res.ok) throw new Error('Failed to fetch symbols');
        const data = await res.json();
        return data.map((item: any) => item.symbol);
      } catch (error) {
        console.error('Error fetching symbols:', error);
        return [];
      }
    },
  
    // Add getStockHistory function
    getStockHistory: async (symbol: string, startDate?: string, endDate?: string): Promise<StockData[]> => {
      try {
        let url = `${BASE_URL}/stocks/${symbol}`;
        if (startDate && endDate) {
          url += `?startDate=${startDate}&endDate=${endDate}`;
        }
        const res = await fetch(url);
        if (!res.ok) throw new Error('Failed to fetch stock history');
        const data = await res.json();
        return data.map((item: any) => ({
          ...item,
          last_trade_price: Number(item.last_trade_price),
          max_price: Number(item.max_price),
          min_price: Number(item.min_price),
          avg_price: Number(item.avg_price),
          change_percentage: Number(item.change_percentage),
          volume: Number(item.volume)
        }));
      } catch (error) {
        console.error('Error fetching stock history:', error);
        return [];
      }
    },
  
    getLatestPrices: async (): Promise<StockData[]> => {
      try {
        const res = await fetch(`${BASE_URL}/stocks/latest`);
        if (!res.ok) throw new Error('Failed to fetch latest prices');
        const data = await res.json();
        return data.map((item: any) => ({
          ...item,
          last_trade_price: Number(item.last_trade_price),
          max_price: Number(item.max_price),
          min_price: Number(item.min_price),
          avg_price: Number(item.avg_price),
          change_percentage: Number(item.change_percentage),
          volume: Number(item.volume)
        }));
      } catch (error) {
        console.error('Error fetching latest prices:', error);
        return [];
      }
    },
  
    getMarketSummary: async (): Promise<MarketSummary> => {
      try {
        const res = await fetch(`${BASE_URL}/stocks/market/summary`);
        if (!res.ok) throw new Error('Failed to fetch market summary');
        const data = await res.json();
        return {
          total_stocks: Number(data.total_stocks),
          total_volume: Number(data.total_volume),
          avg_change: Number(data.avg_change)
        };
      } catch (error) {
        console.error('Error fetching market summary:', error);
        return {
          total_stocks: 0,
          total_volume: 0,
          avg_change: 0
        };
      }
    }
  };
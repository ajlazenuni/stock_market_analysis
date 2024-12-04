// src/components/StockTable.tsx
import React from 'react';
import { StockData } from '../utilts/api';

interface Props {
  data: StockData[];
}

export const StockTable = ({ data }: Props) => {
  return (
    <div className="bg-white rounded-lg shadow overflow-hidden">
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
          {data.map((row, i) => (
            <tr key={i}>
              <td className="px-6 py-4">{row.date}</td>
              <td className="px-6 py-4">{row.symbol}</td>
              <td className="px-6 py-4">{row.last_trade_price}</td>
              <td className="px-6 py-4">{row.max_price}</td>
              <td className="px-6 py-4">{row.min_price}</td>
              <td className={`px-6 py-4 ${
                row.change_percentage > 0 ? 'text-green-500' : 'text-red-500'
              }`}>
                {row.change_percentage}%
              </td>
              <td className="px-6 py-4">{row.volume.toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
/* eslint-disable @typescript-eslint/no-explicit-any */
// src/components/StockChart.tsx
import React from 'react';
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts';

interface Props {
  data: any[];
  height?: number | string;
  dataKey?: string;
}

export const StockChart = ({ 
  data, 
  height = 400, 
  dataKey = "last_trade_price" 
}: Props) => {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div style={{ height: height }}>
        <ResponsiveContainer width="100%" height="100%">
          <LineChart data={data}>
            <XAxis dataKey="date" />
            <YAxis />
            <Tooltip />
            <Line 
              type="monotone" 
              dataKey={dataKey} 
              stroke="#4F46E5" 
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};
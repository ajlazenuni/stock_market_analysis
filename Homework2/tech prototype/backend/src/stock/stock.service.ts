import { Injectable } from '@nestjs/common';
import { InjectDataSource } from '@nestjs/typeorm';
import { DataSource } from 'typeorm';

@Injectable()
export class StockService {
  constructor(@InjectDataSource() private dataSource: DataSource) {}

  async getSymbols() {
    return await this.dataSource.query(
      'SELECT DISTINCT symbol FROM stock_data',
    );
  }

  async getLatestPrices() {
    return await this.dataSource.query(`
      SELECT t1.* 
      FROM stock_data t1
      INNER JOIN (
        SELECT symbol, MAX(date) as max_date
        FROM stock_data
        GROUP BY symbol
      ) t2 
      ON t1.symbol = t2.symbol AND t1.date = t2.max_date
    `);
  }

  async getStockHistory(symbol: string, startDate?: string, endDate?: string) {
    let query = 'SELECT * FROM stock_data WHERE 1=1';
    const params: any[] = [];

    if (symbol) {
      query += ' AND symbol = ?';
      params.push(symbol);
    }

    if (startDate && endDate) {
      query += ' AND date BETWEEN ? AND ?';
      params.push(startDate, endDate);
    }

    query += ' ORDER BY date DESC, symbol ASC';

    return await this.dataSource.query(query, params);
  }

  async getMarketSummary() {
    const [result] = await this.dataSource.query(`
      SELECT 
        COUNT(DISTINCT symbol) as total_stocks,
        SUM(volume) as total_volume,
        AVG(change_percentage) as avg_change
      FROM stock_data
      WHERE date = (SELECT MAX(date) FROM stock_data)
    `);
    return result;
  }
}

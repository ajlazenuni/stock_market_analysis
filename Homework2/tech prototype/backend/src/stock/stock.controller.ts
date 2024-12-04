import { Controller, Get, Param, Query } from '@nestjs/common';
import { StockService } from './stock.service';

@Controller('stocks')
export class StockController {
  constructor(private readonly stockService: StockService) {}

  @Get('symbols')
  getSymbols() {
    return this.stockService.getSymbols();
  }

  @Get('latest')
  getLatestPrices() {
    return this.stockService.getLatestPrices();
  }

  @Get(':symbol')
  getStockHistory(
    @Param('symbol') symbol: string,
    @Query('startDate') startDate?: string,
    @Query('endDate') endDate?: string,
  ) {
    return this.stockService.getStockHistory(symbol, startDate, endDate);
  }

  @Get('market/summary')
  getMarketSummary() {
    return this.stockService.getMarketSummary();
  }
}

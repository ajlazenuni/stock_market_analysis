import { Controller, Get, Param, Query } from '@nestjs/common';
import { StockService } from './stock.service';
import { TechnicalAnalysisService } from './technical-analysis.service';

@Controller('stocks')
export class StockController {
  constructor(
    private readonly stockService: StockService,
    private readonly technicalAnalysisService: TechnicalAnalysisService,
  ) {}

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
  @Get(':symbol/analysis')
  getTechnicalAnalysis(
    @Param('symbol') symbol: string,
    @Query('period') period: string,
  ) {
    return this.technicalAnalysisService.getTechnicalAnalysis(symbol, period);
  }

  @Get(':symbol/analysis/all-periods')
  getAllPeriodAnalysis(@Param('symbol') symbol: string) {
    return this.technicalAnalysisService.getAllPeriodAnalysis(symbol);
  }

  @Get('analysis/indicators')
  getAvailableIndicators() {
    return this.technicalAnalysisService.getAvailableIndicators();
  }
}

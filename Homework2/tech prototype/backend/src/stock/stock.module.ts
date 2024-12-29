// src/stock/stock.module.ts
import { Module } from '@nestjs/common';
import { StockController } from './stock.controller';
import { StockService } from './stock.service';
import { TechnicalAnalysisService } from './technical-analysis.service';

@Module({
  controllers: [StockController],
  providers: [StockService, TechnicalAnalysisService],
})
export class StockModule {}
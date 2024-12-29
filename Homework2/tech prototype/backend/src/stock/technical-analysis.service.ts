import { Injectable, HttpException, HttpStatus } from '@nestjs/common';
import axios from 'axios';

@Injectable()
export class TechnicalAnalysisService {
  private readonly baseUrl = 'http://127.0.0.1:5000/api';

  async getTechnicalAnalysis(symbol: string, period: string = 'daily') {
    try {
      const response = await axios.get(
        `${this.baseUrl}/analysis/${symbol}?period=${period}`,
      );
      return response.data;
    } catch (error) {
      console.error('Error:', error);
      throw new HttpException(
        'Failed to fetch technical analysis',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getAllPeriodAnalysis(symbol: string) {
    try {
      const response = await axios.get(
        `${this.baseUrl}/analysis/${symbol}/all-periods`,
      );
      return response.data;
    } catch (error) {
      throw new HttpException(
        'Failed to fetch technical analysis for all periods',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }

  async getAvailableIndicators() {
    try {
      const response = await axios.get(`${this.baseUrl}/indicators`);
      return response.data;
    } catch (error) {
      throw new HttpException(
        'Failed to fetch indicators',
        HttpStatus.INTERNAL_SERVER_ERROR,
      );
    }
  }
}

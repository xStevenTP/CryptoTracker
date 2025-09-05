export interface Forecast {
  id: number;
  coin: string;
  forecast_data: number[];
  suggestion: string;
  created_at: string;
}

export interface Coin {
  id: number;
  name: string;
  symbol: string;
  price: number;
}
"use client";

import { useEffect, useState } from "react";
import axios from "axios";

import { Coin, Forecast } from "../types";
import { api } from "../lib/api";

export default function Watchlist() {
  const [coins, setCoins] = useState<Coin[]>([]);
  const [forecasts, setForecasts] = useState<Record<string, Forecast>>({});
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);

  const fetchData = async () => {
    try {
      const coinRes = await api.get<Coin[]>("/coins/");
      setCoins(coinRes.data);

      const forecastRes = await axios.get<Forecast[]>("http://localhost:8000/api/forecast/");
      const forecastMap: Record<string, Forecast> = {};
      forecastRes.data.forEach((f) => {
        forecastMap[f.coin] = f;
      });

      setForecasts(forecastMap);
    } catch (err) {
      console.error("Error fetching watchlist:", err);
    } finally {
      setLoading(false);
    }
  };

  const refreshForecasts = async () => {
    try {
      setRefreshing(true);
      await axios.post("http://localhost:8000/api/forecast-refresh/", {});
      await fetchData();
    } catch (err) {
      console.error("Error refreshing forecasts:", err);
    } finally {
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  if (loading) return <div className="p-6">Loading watchlist...</div>;

  return (
    <div className="p-6">
      <div className="flex items-center justify-between mb-4">
        <h1 className="text-2xl font-bold">Watchlist</h1>
        <button
          onClick={refreshForecasts}
          disabled={refreshing}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400"
        >
          {refreshing ? "Refreshing..." : "Refresh Forecasts"}
        </button>
      </div>

      {coins.length === 0 && <p>No coins in your watchlist yet.</p>}

      <div className="grid gap-4">
        {coins.map((coin) => {
          const forecast = forecasts[coin.name];
          return (
            <div key={coin.name} className="p-4 border rounded-lg shadow bg-white">
              <h2 className="text-lg font-semibold">
                {coin.name} ({coin.symbol})
              </h2>
              <p>Current Price: {coin.price}</p>
              {forecast ? (
                <div>
                  <p className="text-gray-600">
                    Latest Forecast:{" "}
                    <span className="font-bold">
                      {forecast.forecast_data[0].toFixed(2)}
                    </span>
                  </p>
                  <p className="text-sm text-blue-600 mt-2">{forecast.suggestion}</p>
                  <p className="text-xs text-gray-400 mt-1">
                    Updated: {new Date(forecast.created_at).toLocaleString()}
                  </p>
                </div>
              ) : (
                <p className="text-gray-500">No forecast available yet.</p>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}

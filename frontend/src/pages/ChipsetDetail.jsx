import React, { useState, useEffect, useMemo } from 'react';
import { useParams, Link } from 'react-router-dom';
import { getGpus, getPrices } from '../api';
import GpuCard from '../components/GpuCard';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

const Formatter = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 0 });

const ChipsetDetail = () => {
  const { chipsetName } = useParams();
  const [gpus, setGpus] = useState([]);
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([getGpus(), getPrices()]).then(([gpusData, pricesData]) => {
      // Filter GPUs strictly to this chipset
      const chipsetGpus = gpusData.filter(g => g.chipset === chipsetName);
      
      const latestPrices = {};
      pricesData.forEach(p => {
        if (!latestPrices[p.gpu_id] || new Date(p.date) > new Date(latestPrices[p.gpu_id].date)) {
          latestPrices[p.gpu_id] = p;
        }
      });

      const gpusWithPrices = chipsetGpus.map(g => ({
        ...g,
        price: latestPrices[g._id] ? latestPrices[g._id].price : 0
      })).filter(g => g.price > 0);

      setGpus(gpusWithPrices);
      
      // Get all gpu ideas for this chipset
      const gpuIds = new Set(chipsetGpus.map(g => g._id));
      
      // Get all prices that belong to GPUs in this chipset
      const relevantPrices = pricesData.filter(p => gpuIds.has(p.gpu_id));
      setPrices(relevantPrices);
      
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, [chipsetName]);

  // Transform data for the chart: Group by Date and find the Minimum Price
  const chartData = useMemo(() => {
    if (!prices.length) return [];
    
    // Group prices by Day
    const pricesByDay = {};
    for (const price of prices) {
      if (price.price <= 0) continue;
      // Assuming price.date is ISO format like YYYY-MM-DDTHH:mm...
      const dateOnly = price.date.split('T')[0];
      if (!pricesByDay[dateOnly]) {
        pricesByDay[dateOnly] = [];
      }
      pricesByDay[dateOnly].push(price.price);
    }

    // Map to array suitable for recharts, calculating minimum price per day
    const data = Object.keys(pricesByDay).map(date => {
      const minPrice = Math.min(...pricesByDay[date]);
      return {
        date,
        minPrice
      };
    });

    // Sort chronologically
    data.sort((a, b) => a.date.localeCompare(b.date));
    return data;
  }, [prices]);

  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div style={{ backgroundColor: 'var(--bg-tertiary)', padding: '10px', border: '1px solid var(--border-color)', borderRadius: '8px' }}>
          <p style={{ margin: 0, fontWeight: 'bold' }}>{label}</p>
          <p style={{ margin: 0, color: 'var(--success)' }}>{Formatter.format(payload[0].value)}</p>
        </div>
      );
    }
    return null;
  };

  if (loading) return <p className="text-center mt-2">Cargando datos de {chipsetName}...</p>;

  // Sort GPUs by price ascending for display
  const displayGpus = [...gpus].sort((a, b) => a.price - b.price);

  return (
    <div>
      <Link to="/" style={{ color: 'var(--accent-color)', marginBottom: '1rem', display: 'inline-block' }}>
        &larr; Volver a Chipsets
      </Link>
      
      <h1 className="mb-2">{chipsetName}</h1>
      <p className="card-subtitle mb-3">Las gráficas más económicas encontradas para este chipset a lo largo del tiempo.</p>

      {chartData.length > 0 ? (
        <div className="chart-container">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={chartData} margin={{ top: 5, right: 20, bottom: 5, left: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" vertical={false} />
              <XAxis dataKey="date" stroke="var(--text-secondary)" tick={{ fill: 'var(--text-secondary)' }} tickMargin={10} minTickGap={20} />
              <YAxis 
                stroke="var(--text-secondary)" 
                tick={{ fill: 'var(--text-secondary)' }} 
                tickFormatter={(val) => Formatter.format(val)} 
                domain={['auto', 'auto']}
              />
              <Tooltip content={<CustomTooltip />} />
              <Line type="monotone" dataKey="minPrice" stroke="var(--accent-color)" strokeWidth={3} dot={{ r: 4, fill: 'var(--bg-primary)', strokeWidth: 2 }} activeDot={{ r: 6 }} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      ) : (
        <p className="mb-3 text-center" style={{color: 'var(--text-secondary)'}}>No hay historial de precios suficiente para graficar.</p>
      )}

      <h2 className="mb-2">Publicaciones Actuales ({displayGpus.length})</h2>
      <div className="grid">
        {displayGpus.map(gpu => (
          <GpuCard key={gpu._id} gpu={gpu} />
        ))}
      </div>
    </div>
  );
};

export default ChipsetDetail;

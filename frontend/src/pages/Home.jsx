import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getGpus, getPrices } from '../api';

const Home = () => {
  const [gpus, setGpus] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');

  useEffect(() => {
    Promise.all([getGpus(), getPrices()]).then(([gpusData, pricesData]) => {
      const latestPrices = {};
      pricesData.forEach(p => {
        if (!latestPrices[p.gpu_id] || new Date(p.date) > new Date(latestPrices[p.gpu_id].date)) {
          latestPrices[p.gpu_id] = p;
        }
      });

      const gpusWithPrices = gpusData.map(g => ({
        ...g,
        price: latestPrices[g._id] ? latestPrices[g._id].price : 0
      })).filter(g => g.price > 0);

      setGpus(gpusWithPrices);
      setLoading(false);
    }).catch(err => {
      console.error(err);
      setLoading(false);
    });
  }, []);

  // Extract unique chipsets and counts
  const chipsetStats = gpus.reduce((acc, gpu) => {
    if (!gpu.chipset) return acc;
    if (!acc[gpu.chipset]) {
      acc[gpu.chipset] = { name: gpu.chipset, count: 0, minPrice: gpu.price };
    }
    acc[gpu.chipset].count += 1;
    if (gpu.price < acc[gpu.chipset].minPrice) {
      acc[gpu.chipset].minPrice = gpu.price;
    }
    return acc;
  }, {});

  let chipsets = Object.values(chipsetStats).sort((a, b) => a.name.localeCompare(b.name));

  if (search.trim()) {
    chipsets = chipsets.filter(c => c.name.toLowerCase().includes(search.toLowerCase()));
  }

  const Formatter = new Intl.NumberFormat('es-AR', { style: 'currency', currency: 'ARS', maximumFractionDigits: 0 });

  return (
    <div>
      <div className="search-container">
        <input 
          type="text" 
          className="search-input" 
          placeholder="Buscar chipset (ej. RX 7600, RTX 4060)..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
      </div>

      {loading ? (
        <p className="text-center mt-2">Cargando chipsets...</p>
      ) : (
        <div className="grid">
          {chipsets.map(chipset => (
            <Link key={chipset.name} to={`/chipset/${encodeURIComponent(chipset.name)}`} className="card" style={{textDecoration: 'none'}}>
              <h2 className="card-title">{chipset.name}</h2>
              <p className="card-subtitle mb-2">{chipset.count} modelos disponibles</p>
              <div style={{ marginTop: 'auto' }}>
                <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)'}}>Desde</span>
                <p style={{ color: 'var(--success)', fontWeight: 'bold', fontSize: '1.25rem'}}>{Formatter.format(chipset.minPrice)}</p>
              </div>
            </Link>
          ))}
          {chipsets.length === 0 && <p style={{gridColumn: '1 / -1', textAlign: 'center'}}>No se encontraron chipsets.</p>}
        </div>
      )}
    </div>
  );
};

export default Home;

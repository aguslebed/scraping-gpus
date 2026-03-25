import React from 'react';

const Formatter = new Intl.NumberFormat('es-AR', {
  style: 'currency',
  currency: 'ARS',
  maximumFractionDigits: 0
});

const GpuCard = ({ gpu }) => {
  return (
    <a href={gpu.url} target="_blank" rel="noopener noreferrer" className="card" style={{ textDecoration: 'none' }}>
      <img src={gpu.image_url || gpu.img_url} alt={gpu.name} className="gpu-image" loading="lazy" />
      
      <div className="flex flex-col gap-2" style={{ flexGrow: 1 }}>
        <h3 className="card-title text-sm">{gpu.name}</h3>
        <p className="card-subtitle">{gpu.store} • {gpu.chipset}</p>
        
        <div style={{ marginTop: '0.5rem' }}>
            {gpu.is_outlet && <span className="badge badge-outlet">Outlet</span>}
            {gpu.outlet && <span className="badge badge-outlet">Outlet</span>}
        </div>
      </div>
      
      <div className="price-tag">
        {Formatter.format(gpu.price)}
      </div>
    </a>
  );
};

export default GpuCard;

import React from 'react';

const Formatter = new Intl.NumberFormat('es-AR', {
  style: 'currency',
  currency: 'ARS',
  maximumFractionDigits: 0
});

const GpuCard = ({ gpu }) => {
  const isOutOfStock = gpu.in_stock === false;

  return (
    <a 
      href={gpu.url} 
      target="_blank" 
      rel="noopener noreferrer" 
      className="card" 
      style={{ 
        textDecoration: 'none', 
        opacity: isOutOfStock ? 0.6 : 1,
        filter: isOutOfStock ? 'grayscale(0.8)' : 'none'
      }}
    >
      <div style={{ position: 'relative' }}>
        <img src={gpu.image_url || gpu.img_url} alt={gpu.name} className="gpu-image" loading="lazy" />
        {isOutOfStock && (
          <div style={{
            position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)',
            backgroundColor: 'rgba(0,0,0,0.8)', color: 'var(--error, #ff4c4c)', padding: '0.5rem 1rem',
            borderRadius: '4px', fontWeight: 'bold', border: '2px solid var(--error, #ff4c4c)',
            backdropFilter: 'blur(2px)', zIndex: 10
          }}>
            SIN STOCK
          </div>
        )}
      </div>
      
      <div className="flex flex-col gap-2" style={{ flexGrow: 1 }}>
        <h3 className="card-title text-sm">{gpu.name}</h3>
        <p className="card-subtitle">{gpu.store} • {gpu.chipset}</p>
        
        <div style={{ marginTop: '0.5rem' }}>
            {gpu.is_outlet && <span className="badge badge-outlet">Outlet</span>}
            {gpu.outlet && <span className="badge badge-outlet">Outlet</span>}
        </div>
      </div>
      
      <div className="price-tag" style={{ textDecoration: isOutOfStock ? 'line-through' : 'none', color: isOutOfStock ? 'var(--text-secondary)' : 'inherit' }}>
        {Formatter.format(gpu.price)}
      </div>
    </a>
  );
};

export default GpuCard;

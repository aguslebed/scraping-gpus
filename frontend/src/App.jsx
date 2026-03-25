import React from 'react';
import { Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import ChipsetDetail from './pages/ChipsetDetail';

function App() {
  return (
    <div className="app">
      <nav className="navbar">
        <Link to="/" className="logo">GPU Tracker</Link>
      </nav>
      <main className="container">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/chipset/:chipsetName" element={<ChipsetDetail />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;

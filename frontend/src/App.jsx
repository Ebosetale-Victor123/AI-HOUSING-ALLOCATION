import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';

// We use ./ instead of @ to be 100% safe for now
import Navbar from './components/landing/Navbar';
import HeroSection from './components/landing/HeroSection';
import HowItWorks from './components/landing/HowItWorks';
import LiveOccupancy from './components/landing/LiveOccupancy';
import Testimonials from './components/landing/Testimonials';
import Footer from './components/landing/Footer';

function App() {
  return (
    <Router>
      <div className="min-h-screen relative bg-white">
        <Navbar />
        <Routes>
          <Route path="/" element={
            <>
              <HeroSection />
              <HowItWorks />
              <LiveOccupancy />
              <Testimonials />
              <Footer />
            </>
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
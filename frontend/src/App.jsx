import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Navbar from './components/landing/Navbar';
import HeroSection from './components/landing/HeroSection';
import HowItWorks from './components/landing/HowItWorks';
import LiveOccupancy from './components/landing/LiveOccupancy';
import Testimonials from './components/landing/Testimonials';
import Footer from './components/landing/Footer';
import StudentDashboard from './pages/StudentDashboard';
import AdminDashboard from './pages/AdminDashboard';
import Auth from './pages/Auth'; // Import the Auth page

function App() {
  return (
    <Router>
      <div className="min-h-screen relative">
        <Routes>
          {/* Main Landing Page */}
          <Route path="/" element={
            <>
              <Navbar />
              <HeroSection />
              <HowItWorks />
              <LiveOccupancy />
              <Testimonials />
              <Footer />
            </>
          } />

          {/* Authentication Page */}
          <Route path="/auth" element={<Auth />} />
          <Route path="/student-dashboard" element={<StudentDashboard />} />
          <Route path="/admin-dashboard" element={<AdminDashboard />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
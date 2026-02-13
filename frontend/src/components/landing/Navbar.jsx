import React from 'react';
import { Building2 } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function Navbar() {
  return (
    <nav className="absolute top-0 w-full z-50 px-8 py-6 flex justify-between items-center">
      <div className="flex items-center gap-2">
        <Building2 className="w-8 h-8 text-indigo-600" />
        <span className="text-xl font-bold text-slate-900 tracking-tight">UniHousing AI</span>
      </div>
      
      <Link to="/auth">
        <button className="px-6 py-2.5 bg-slate-900 text-white font-bold rounded-xl transition-all 
          hover:bg-indigo-600 hover:shadow-[0_0_20px_rgba(79,70,229,0.6)] active:scale-95">
          Login
        </button>
      </Link>
    </nav>
  );
}
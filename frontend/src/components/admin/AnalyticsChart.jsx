import React from 'react';
import { motion } from 'framer-motion';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
import { TrendingUp } from 'lucide-react';

const mockData = [
  { month: 'Jan', demand: 320, supply: 280 }, { month: 'Feb', demand: 380, supply: 290 },
  { month: 'Mar', demand: 420, supply: 300 }, { month: 'Apr', demand: 480, supply: 310 },
  { month: 'May', demand: 520, supply: 320 }, { month: 'Jun', demand: 350, supply: 330 },
  { month: 'Jul', demand: 280, supply: 340 }, { month: 'Aug', demand: 650, supply: 350 },
  { month: 'Sep', demand: 780, supply: 360 }, { month: 'Oct', demand: 420, supply: 370 },
  { month: 'Nov', demand: 380, supply: 380 }, { month: 'Dec', demand: 300, supply: 390 },
];

export default function AnalyticsChart() {
  return (
    <div className="bg-white rounded-[32px] border border-slate-100 p-10 shadow-sm">
      <div className="flex justify-between items-start mb-10">
        <div>
          <h3 className="text-xl font-bold text-slate-900">Housing Demand vs Supply</h3>
          <p className="text-sm text-slate-400 font-medium mt-1">Monthly comparison for 2026</p>
        </div>
        <div className="flex items-center gap-2 px-3 py-1.5 bg-emerald-50 text-emerald-600 rounded-lg text-xs font-bold">
          <TrendingUp className="w-4 h-4" /> +23% YoY
        </div>
      </div>

      <div className="h-80 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={mockData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
            <XAxis dataKey="month" axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12, fontWeight: 'bold'}} />
            <YAxis axisLine={false} tickLine={false} tick={{fill: '#94a3b8', fontSize: 12, fontWeight: 'bold'}} />
            <Tooltip cursor={{fill: '#f8fafc'}} contentStyle={{borderRadius: '16px', border: 'none', boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)'}} />
            <Legend iconType="rect" wrapperStyle={{ paddingTop: '40px' }} />
            <Bar dataKey="demand" name="Demand" fill="#6366f1" radius={[4, 4, 0, 0]} barSize={20} />
            <Bar dataKey="supply" name="Supply" fill="#06b6d4" radius={[4, 4, 0, 0]} barSize={20} />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Summary Stats Row */}
      <div className="grid grid-cols-3 gap-8 mt-12 pt-10 border-t border-slate-50">
        <div className="text-center">
          <p className="text-3xl font-black text-indigo-600">5,280</p>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mt-1">Total Demand</p>
        </div>
        <div className="text-center">
          <p className="text-3xl font-black text-cyan-500">4,020</p>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mt-1">Total Supply</p>
        </div>
        <div className="text-center">
          <p className="text-3xl font-black text-amber-500">1,260</p>
          <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mt-1">Gap</p>
        </div>
      </div>
    </div>
  );
}
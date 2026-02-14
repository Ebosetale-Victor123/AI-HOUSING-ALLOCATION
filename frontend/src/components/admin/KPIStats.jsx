import React from 'react';
import { Users, Building2, Percent, Brain } from 'lucide-react';

export default function KPIStats() {
  const stats = [
    { label: "Total Applicants", val: "847", change: "+12%", trend: "up", icon: Users, color: "text-indigo-600", bg: "bg-indigo-100" },
    { label: "Available Rooms", val: "99", change: "-23", trend: "down", icon: Building2, color: "text-cyan-600", bg: "bg-cyan-100" },
    { label: "Capacity %", val: "92.4%", change: "+2.1%", trend: "up", icon: Percent, color: "text-emerald-600", bg: "bg-emerald-100" },
    { label: "AI Success Rate", val: "95.8%", change: "+0.5%", trend: "up", icon: Brain, color: "text-amber-600", bg: "bg-amber-100" },
  ];

  return (
    <div className="grid grid-cols-4 gap-6">
      {stats.map((s, i) => (
        <div key={i} className="bg-white p-6 rounded-2xl border border-slate-100 flex items-center justify-between shadow-sm">
          <div className="flex items-center gap-4">
            <div className={`w-12 h-12 ${s.bg} ${s.color} rounded-xl flex items-center justify-center`}>
              <s.icon className="w-6 h-6" />
            </div>
            <div>
              <div className="text-2xl font-bold text-slate-900">{s.val}</div>
              <div className="text-xs text-slate-400 font-medium">{s.label}</div>
            </div>
          </div>
          <div className={`text-[10px] font-bold px-2 py-1 rounded-full ${s.trend === 'up' ? 'bg-emerald-50 text-emerald-500' : 'bg-red-50 text-red-400'}`}>
            {s.change}
          </div>
        </div>
      ))}
    </div>
  );
}
import React from 'react';
import { LayoutDashboard, Users, Brain, BarChart3, Settings, LogOut, Building2, User } from 'lucide-react';

const adminNav = [
  { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { id: 'applications', label: 'Applications', icon: Users },
  { id: 'allocation', label: 'AI Allocation', icon: Brain },
  { id: 'analytics', label: 'Analytics', icon: BarChart3 },
  
];

export default function Sidebar({ activeTab, setActiveTab, user }) {
  return (
    <aside className="fixed top-0 left-0 h-full w-64 bg-[#0f172a] text-slate-400 flex flex-col z-50">
      {/* Logo */}
      <div className="p-6 flex items-center gap-3">
        <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center">
          <Building2 className="w-6 h-6 text-white" />
        </div>
        <div>
          <span className="block text-white font-bold text-lg leading-tight">UniHousing</span>
          <span className="block text-xs text-slate-500">Admin Panel</span>
        </div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 mt-4">
        <ul className="space-y-1">
          {adminNav.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all font-medium ${
                  activeTab === item.id 
                  ? 'bg-indigo-600 text-white shadow-lg' 
                  : 'hover:bg-slate-800/50 hover:text-white'
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span className="text-sm">{item.label}</span>
              </button>
            </li>
          ))}
        </ul>
      </nav>

      {/* User Card */}
      <div className="p-4 bg-slate-800/30 m-4 rounded-2xl border border-slate-700/50">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-full bg-indigo-500 flex items-center justify-center">
            <User className="w-5 h-5 text-white" />
          </div>
          <div className="overflow-hidden">
            <p className="text-sm font-bold text-white truncate">Henry Swazch</p>
            <p className="text-[10px] text-slate-500 truncate">henryswazch@gmail.com</p>
          </div>
        </div>
        <button className="w-full py-2 border border-slate-700 rounded-lg text-xs font-bold hover:bg-slate-800 transition-all flex items-center justify-center gap-2">
          <LogOut className="w-3 h-3" /> Sign Out
        </button>
      </div>
    </aside>
  );
}
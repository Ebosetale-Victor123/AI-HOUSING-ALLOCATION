import React from 'react';
import { LayoutDashboard, FileText, Building2, HelpCircle, LogOut, X, User, ChevronRight, Building } from 'lucide-react';

const navItems = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'application', label: 'My Application', icon: FileText },
  { id: 'hostels', label: 'Hostel Gallery', icon: Building2 },
  { id: 'support', label: 'Support', icon: HelpCircle },
];

export default function Sidebar({ activeTab, setActiveTab, setSidebarOpen, sidebarOpen, user }) {
  return (
    <aside className={`
      fixed top-0 left-0 h-full w-72 bg-white border-r border-slate-100 z-50
      transform transition-transform duration-300 lg:translate-x-0
      ${sidebarOpen ? 'translate-x-0' : '-translate-x-full'}
    `}>
      {/* Sidebar Logo */}
      <div className="p-8">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-200">
            <Building className="w-6 h-6 text-white" />
          </div>
          <span className="text-xl font-black text-slate-900 tracking-tighter uppercase">UniHousing</span>
        </div>
      </div>

      {/* Navigation Links */}
      <nav className="px-4 mt-4">
        <ul className="space-y-2">
          {navItems.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => {
                  setActiveTab(item.id);
                  setSidebarOpen(false);
                }}
                className={`
                  w-full flex items-center gap-3 px-4 py-3.5 rounded-2xl font-bold transition-all
                  ${activeTab === item.id
                    ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-100'
                    : 'text-slate-400 hover:bg-slate-50 hover:text-slate-600'
                  }
                `}
              >
                <item.icon className="w-5 h-5" />
                <span className="text-sm">{item.label}</span>
                {activeTab === item.id && <ChevronRight className="w-4 h-4 ml-auto" />}
              </button>
            </li>
          ))}
        </ul>
      </nav>

      {/* User Profile Card at Bottom */}
      <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-slate-50 bg-slate-50/30">
        <div className="flex items-center gap-3 p-3 bg-white rounded-2xl border border-slate-100 shadow-sm mb-4">
          <div className="w-10 h-10 rounded-xl bg-cyan-100 flex items-center justify-center">
            <User className="w-5 h-5 text-cyan-600" />
          </div>
          <div className="flex-1 min-w-0">
            <p className="text-sm font-bold text-slate-900 truncate">{user?.name || 'Henry Swazch'}</p>
            <p className="text-[10px] font-bold text-slate-400 uppercase truncate">{user?.email || 'henry@uni.edu'}</p>
          </div>
        </div>
        <button className="w-full flex items-center justify-center gap-2 py-3 rounded-xl border border-slate-200 text-slate-500 font-bold text-xs hover:bg-red-50 hover:text-red-500 hover:border-red-100 transition-all">
          <LogOut className="w-4 h-4" /> Sign Out
        </button>
      </div>
    </aside>
  );
}
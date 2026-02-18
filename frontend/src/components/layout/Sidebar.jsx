import React from 'react';
import { LayoutDashboard, Building2, RefreshCw, HelpCircle, LogOut, ChevronRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom'; // 1. Import useNavigate

const navItems = [
  { id: 'overview', label: 'Overview', icon: LayoutDashboard },
  { id: 'room-change', label: 'Room Change', icon: RefreshCw },
  { id: 'hostels', label: 'Hostel Gallery', icon: Building2 },
  { id: 'support', label: 'Support', icon: HelpCircle },
];

export default function Sidebar({ activeTab, setActiveTab, user }) {
  const navigate = useNavigate(); // 2. Initialize navigate

  const handleSignOut = () => {
    // In a real app, you would clear the user session here
    navigate('/auth'); // 3. Redirect to Auth page
  };

  return (
    <aside className="fixed top-0 left-0 h-full w-72 bg-[#0f172a] text-slate-400 flex flex-col z-50">
      {/* Caleb University Logo Section */}
      <div className="p-8 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="w-12 h-12 rounded-2xl bg-green-600 flex items-center justify-center shadow-lg shadow-green-900/20">
            <Building2 className="w-6 h-6 text-white" />
          </div>
          <div>
            <span className="block text-white font-black text-lg tracking-tight leading-tight">Caleb University</span>
            <span className="block text-[10px] font-bold text-green-500 uppercase tracking-widest">Student Portal</span>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-4 mt-6">
        <ul className="space-y-2">
          {navItems.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-3 px-4 py-3.5 rounded-2xl font-bold transition-all ${
                  activeTab === item.id
                    ? 'bg-green-600 text-white shadow-xl shadow-green-900/40'
                    : 'hover:bg-slate-800/50 hover:text-slate-200'
                }`}
              >
                <item.icon className="w-5 h-5" />
                <span className="text-sm">{item.label}</span>
                {activeTab === item.id && <ChevronRight className="w-4 h-4 ml-auto" />}
              </button>
            </li>
          ))}
        </ul>
      </nav>

      {/* Profile Section */}
      <div className="p-4 bg-slate-800/30 m-4 rounded-[24px] border border-slate-700/50">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 rounded-full bg-green-500 flex items-center justify-center text-white font-bold">
            {user?.name?.charAt(0) || 'H'}
          </div>
          <div className="overflow-hidden">
            <p className="text-sm font-bold text-white truncate">{user?.name || 'Henry Swazch'}</p>
            <p className="text-[10px] font-medium text-slate-500 truncate">{user?.email}</p>
          </div>
        </div>
        
        {/* UPDATED SIGN OUT BUTTON */}
        <button 
          onClick={handleSignOut}
          className="w-full py-2.5 rounded-xl bg-slate-800 text-xs font-bold text-slate-300 hover:bg-red-500 hover:text-white transition-all flex items-center justify-center gap-2"
        >
          <LogOut className="w-3 h-3" /> Sign Out
        </button>
      </div>
    </aside>
  );
}
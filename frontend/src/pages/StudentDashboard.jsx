import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Menu, Bell, ChevronRight, Sparkles } from 'lucide-react';
import Sidebar from '../components/layout/Sidebar';

export default function StudentDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  // MOCK USER DATA (Later this comes from Backend)
  const user = { name: "Henry Swazch", email: "henryswazch@gmail.com" };
  const hasApplication = false; // Toggle this to true to see the status view

  return (
    <div className="min-h-screen bg-[#fcfcfd]">
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        sidebarOpen={sidebarOpen} 
        setSidebarOpen={setSidebarOpen}
        user={user}
      />

      <main className="lg:ml-72 min-h-screen">
        {/* Top Header */}
        <header className="sticky top-0 z-30 bg-white/80 backdrop-blur-md border-b border-slate-100 px-8 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <button onClick={() => setSidebarOpen(true)} className="lg:hidden p-2 hover:bg-slate-100 rounded-lg">
                <Menu className="w-6 h-6 text-slate-600" />
              </button>
              <div>
                <h1 className="text-xl font-black text-slate-900 capitalize">{activeTab}</h1>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Welcome back, {user.name.split(' ')[0]}</p>
              </div>
            </div>
            
            <button className="relative p-2.5 bg-slate-50 rounded-xl hover:bg-slate-100 transition-colors">
              <Bell className="w-5 h-5 text-slate-500" />
              <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-indigo-600 rounded-full border-2 border-white" />
            </button>
          </div>
        </header>

        {/* Dashboard Content */}
        <div className="p-8">
          {activeTab === 'overview' && (
            <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="space-y-8">
              
              {/* The Blue Hero Card */}
              {!hasApplication && (
                <div className="relative overflow-hidden bg-gradient-to-r from-indigo-600 via-blue-600 to-cyan-500 rounded-[32px] p-10 text-white shadow-xl shadow-indigo-100">
                  <div className="absolute top-0 right-0 p-8 opacity-10">
                     <Sparkles className="w-40 h-40" />
                  </div>
                  <div className="relative z-10 max-w-lg">
                    <h2 className="text-4xl font-black mb-4">Start Your Application</h2>
                    <p className="text-indigo-100 font-medium mb-8 leading-relaxed text-lg">
                      Your journey to the perfect campus home begins here. Complete your profile and let our AI match you.
                    </p>
                    <button 
                      onClick={() => setActiveTab('application')}
                      className="px-8 py-4 bg-white text-indigo-600 font-black rounded-2xl shadow-lg hover:scale-105 transition-transform flex items-center gap-2"
                    >
                      Apply Now <ChevronRight className="w-5 h-5" />
                    </button>
                  </div>
                </div>
              )}

              {/* Placeholder for other cards */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="p-8 bg-white rounded-3xl border border-slate-100 shadow-sm">
                  <h3 className="font-bold text-slate-900 mb-2">Hostel Guidelines</h3>
                  <p className="text-sm text-slate-500">Read the rules and regulations for the 2026 academic session.</p>
                </div>
                <div className="p-8 bg-white rounded-3xl border border-slate-100 shadow-sm">
                  <h3 className="font-bold text-slate-900 mb-2">Important Dates</h3>
                  <p className="text-sm text-slate-500">Allocation results will be released on October 24th.</p>
                </div>
              </div>

            </motion.div>
          )}

          {activeTab !== 'overview' && (
            <div className="flex flex-col items-center justify-center py-20 text-center">
               <div className="w-20 h-20 bg-slate-100 rounded-full mb-4 flex items-center justify-center">
                  <Sparkles className="text-slate-300 w-10 h-10" />
               </div>
               <h2 className="text-xl font-bold text-slate-400">Section Under Construction</h2>
               <p className="text-slate-400">We are currently revamping the {activeTab} view.</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
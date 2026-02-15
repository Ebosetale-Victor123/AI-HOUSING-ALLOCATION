import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Bell, ChevronRight } from 'lucide-react';

// Component Imports
import Sidebar from '../components/layout/Sidebar';
import KPIStats from '../components/admin/KPIStats';
import AIAllocationEngine from '../components/admin/AIAllocationEngine';
import ApplicationsTable from '../components/admin/ApplicationsTable';
import AnalyticsChart from '../components/admin/AnalyticsChart';


export default function AdminDashboard() {
  const [activeTab, setActiveTab] = useState('dashboard');

  return (
    <div className="min-h-screen bg-[#fcfcfd]">
      {/* Sidebar - Dark Theme */}
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

      <main className="ml-64 p-8">
        {/* Header Section */}
        <header className="flex justify-between items-center mb-10">
          <div>
            <h1 className="text-2xl font-black text-slate-900 capitalize tracking-tight">
              {activeTab === 'dashboard' ? 'Dashboard' : activeTab.replace('-', ' ')}
            </h1>
            <p className="text-sm text-slate-400 font-bold uppercase tracking-widest text-[10px]">
              Housing Management System
            </p>
          </div>
          <button className="p-3 bg-white border border-slate-100 rounded-2xl relative shadow-sm hover:bg-slate-50 transition-all">
            <Bell className="w-5 h-5 text-slate-400" />
            <span className="absolute top-3 right-3 w-2 h-2 bg-red-500 rounded-full border-2 border-white"></span>
          </button>
        </header>

        {/* Content Area with Smooth Transitions */}
        <div className="space-y-10">
          <AnimatePresence mode="wait">
            
            {/* 1. DASHBOARD OVERVIEW */}
            {activeTab === 'dashboard' && (
              <motion.div 
                key="dashboard"
                initial={{ opacity: 0, y: 20 }} 
                animate={{ opacity: 1, y: 0 }} 
                exit={{ opacity: 0, y: -20 }}
                className="space-y-10"
              >
                <KPIStats />
                
                <div className="grid grid-cols-5 gap-8">
                  <div className="col-span-2">
                    <AIAllocationEngine />
                  </div>
                  <div className="col-span-3">
                    <AnalyticsChart />
                  </div>
                </div>

                <ApplicationsTable title="Recent Applications" />
              </motion.div>
            )}

            {/* 2. APPLICATIONS VIEW (Full Screen) */}
            {activeTab === 'applications' && (
              <motion.div 
                key="applications"
                initial={{ opacity: 0, x: 20 }} 
                animate={{ opacity: 1, x: 0 }} 
                exit={{ opacity: 0, x: -20 }}
              >
                <ApplicationsTable />
              </motion.div>
            )}


            {activeTab === 'analytics' && (
  <motion.div 
    key="analytics"
    initial={{ opacity: 0, y: 20 }} 
    animate={{ opacity: 1, y: 0 }}
    className="space-y-8"
  >
    {/* Top Full-Width Chart */}
    <AnalyticsChart />

    {/* Bottom Two Cards Grid */}
    <AnalyticsBottomGrid />
  </motion.div>
)}


            {/* 3. AI ALLOCATION VIEW (Centered Layout) */}
            {activeTab === 'allocation' && (
              <motion.div 
                key="allocation"
                initial={{ opacity: 0, scale: 0.98 }} 
                animate={{ opacity: 1, scale: 1 }} 
                exit={{ opacity: 0, scale: 0.98 }}
                className="max-w-4xl mx-auto space-y-8"
              >
                {/* Main AI Engine Card */}
                <AIAllocationEngine />

                {/* Allocation History Card */}
                <div className="bg-white rounded-[32px] border border-slate-100 shadow-sm overflow-hidden">
                  <div className="p-8 border-b border-slate-50 flex justify-between items-center">
                    <h3 className="font-black text-slate-900 uppercase tracking-tighter text-lg">Allocation History</h3>
                    <div className="px-3 py-1 bg-slate-50 rounded-lg text-[10px] font-bold text-slate-400 uppercase tracking-widest">Logs Archive</div>
                  </div>
                  
                  <div className="p-4 space-y-3">
                    {[
                      { date: '2026-02-10', processed: 234, allocated: 198, success: 84.6 },
                      { date: '2026-01-15', processed: 456, allocated: 412, success: 90.4 },
                      { date: '2025-12-20', processed: 189, allocated: 167, success: 88.4 },
                    ].map((run, i) => (
                      <motion.div 
                        key={i} 
                        whileHover={{ x: 5 }}
                        className="flex items-center justify-between p-6 bg-[#f8fafc] rounded-2xl border border-transparent hover:border-slate-200 transition-all cursor-default"
                      >
                        <div>
                          <p className="font-black text-slate-900 text-lg tracking-tight">{run.date}</p>
                          <p className="text-xs text-slate-400 font-bold uppercase tracking-widest">{run.processed} applications processed</p>
                        </div>
                        <div className="text-right">
                          <p className="font-black text-emerald-500 text-lg">{run.allocated} allocated</p>
                          <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">{run.success}% success rate</p>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>
              </motion.div>
            )}

            {/* 4. ANALYTICS & SETTINGS (Placeholders) */}
            {(activeTab === 'analytics' || activeTab === 'settings') && (
              <motion.div 
                key="other"
                initial={{ opacity: 0 }} 
                animate={{ opacity: 1 }}
                className="py-40 text-center"
              >
                <div className="w-20 h-20 bg-slate-100 rounded-full flex items-center justify-center mx-auto mb-6">
                   <div className="w-10 h-10 bg-slate-200 rounded-lg animate-pulse" />
                </div>
                <h2 className="text-2xl font-black text-slate-300 uppercase tracking-[15px]">
                  {activeTab} VIEW
                </h2>
                <p className="text-slate-400 font-bold mt-4 uppercase text-xs tracking-widest">System configuration in progress</p>
              </motion.div>
            )}

          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
const AnalyticsBottomGrid = () => (
  <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mt-8">
    {/* Left: Applications by Department */}
    <div className="bg-white rounded-[32px] border border-slate-100 p-10 shadow-sm">
      <h3 className="text-sm font-bold text-slate-900 uppercase tracking-tight mb-8">Applications by Department</h3>
      <div className="space-y-6">
        {[
          { name: 'Engineering', count: 234, color: 'bg-cyan-500', width: '55%' },
          { name: 'Business', count: 189, color: 'bg-cyan-500', width: '45%' },
          { name: 'Medicine', count: 156, color: 'bg-cyan-500', width: '38%' },
          { name: 'Arts', count: 145, color: 'bg-cyan-500', width: '35%' },
          { name: 'Science', count: 123, color: 'bg-cyan-500', width: '30%' },
        ].map((item) => (
          <div key={item.name} className="flex items-center gap-4">
            <span className="w-24 text-xs font-bold text-slate-500">{item.name}</span>
            <div className="flex-1 h-2 bg-slate-50 rounded-full overflow-hidden">
              <motion.div initial={{ width: 0 }} animate={{ width: item.width }} className={`h-full ${item.color}`} />
            </div>
            <span className="text-xs font-bold text-slate-900">{item.count}</span>
          </div>
        ))}
      </div>
    </div>

    {/* Right: AI Score Distribution */}
    <div className="bg-white rounded-[32px] border border-slate-100 p-10 shadow-sm">
      <h3 className="text-sm font-bold text-slate-900 uppercase tracking-tight mb-8">AI Score Distribution</h3>
      <div className="space-y-4">
        {[
          { range: '90-100', count: 89, color: 'bg-emerald-500', width: '40%' },
          { range: '80-89', count: 156, color: 'bg-cyan-500', width: '65%' },
          { range: '70-79', count: 234, color: 'bg-indigo-500', width: '90%' },
          { range: '60-69', count: 198, color: 'bg-amber-500', width: '80%' },
          { range: 'Below 60', count: 170, color: 'bg-red-500', width: '70%' },
        ].map((item) => (
          <div key={item.range} className="flex items-center gap-4">
            <span className="w-16 text-[10px] font-bold text-slate-400">{item.range}</span>
            <div className="flex-1 h-8 bg-slate-50 rounded-lg overflow-hidden relative">
              <motion.div initial={{ width: 0 }} animate={{ width: item.width }} className={`h-full ${item.color} flex items-center justify-end pr-4`}>
                <span className="text-[10px] font-black text-white">{item.count}</span>
              </motion.div>
            </div>
          </div>
        ))}
      </div>
    </div>
  </div>
);
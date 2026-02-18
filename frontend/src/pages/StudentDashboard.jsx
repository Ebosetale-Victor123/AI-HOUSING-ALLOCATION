import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, Bell, ChevronRight, Sparkles } from 'lucide-react';

// Component Imports
import Sidebar from '../components/layout/Sidebar';
import OverviewTab from '../components/student/OverviewTab';
import RoomChangeRequest from '../components/student/RoomChangeRequest';
import HostelGallery from '../components/student/HostelGallery';
import Support from '../components/student/Support';

export default function StudentDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  // MOCK USER DATA
  const user = { name: "Henry Swazch", email: "henryswazch@gmail.com" };

  return (
    <div className="min-h-screen bg-[#fcfcfd]">
      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Sidebar with Caleb Branding */}
      <Sidebar 
        activeTab={activeTab} 
        setActiveTab={setActiveTab} 
        sidebarOpen={sidebarOpen} 
        setSidebarOpen={setSidebarOpen}
        user={user}
      />

      <main className="lg:ml-72 min-h-screen">
        {/* Top Header */}
        <header className="sticky top-0 z-30 bg-white/80 backdrop-blur-md border-b border-slate-100 px-8 py-6">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-4">
              <button onClick={() => setSidebarOpen(true)} className="lg:hidden p-2 hover:bg-slate-100 rounded-lg transition-colors">
                <Menu className="w-6 h-6 text-slate-600" />
              </button>
              <div>
                <h1 className="text-xl font-black text-slate-900 capitalize tracking-tight">
                  {activeTab.replace('-', ' ')}
                </h1>
                <p className="text-[10px] font-black text-slate-400 uppercase tracking-[3px]">
                  Welcome back, {user.name.split(' ')[0]}
                </p>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <button className="relative p-3 bg-white border border-slate-100 rounded-2xl shadow-sm text-slate-400 hover:text-indigo-600 transition-all group">
                <Bell className="w-5 h-5 group-hover:animate-bounce" />
                <span className="absolute top-3 right-3 w-2 h-2 bg-red-500 rounded-full border-2 border-white" />
              </button>
            </div>
          </div>
        </header>

        {/* Main Content Area */}
        <div className="p-8 max-w-7xl mx-auto">
          <AnimatePresence mode="wait">
            
            {/* 1. OVERVIEW TAB (Banner -> Form -> Summary Flow) */}
            {activeTab === 'overview' && (
              <motion.div 
                key="overview"
                initial={{ opacity: 0, y: 20 }} 
                animate={{ opacity: 1, y: 0 }} 
                exit={{ opacity: 0, y: -20 }}
              >
                <OverviewTab user={user} />
              </motion.div>
            )}

            {/* 2. ROOM CHANGE TAB */}
            {activeTab === 'room-change' && (
              <motion.div 
                key="room-change"
                initial={{ opacity: 0, x: 20 }} 
                animate={{ opacity: 1, x: 0 }} 
                exit={{ opacity: 0, x: -20 }}
              >
                <RoomChangeRequest user={user} />
              </motion.div>
            )}

            {/* 3. HOSTEL GALLERY TAB */}
            {activeTab === 'hostels' && (
              <motion.div 
                key="hostels"
                initial={{ opacity: 0, scale: 0.98 }} 
                animate={{ opacity: 1, scale: 1 }} 
                exit={{ opacity: 0, scale: 0.98 }}
              >
                <div className="mb-10">
                   <h2 className="text-3xl font-black text-slate-900">Explore Accommodations</h2>
                   <p className="text-slate-500 font-medium">Browse smart residences at Caleb University.</p>
                </div>
                <HostelGallery />
              </motion.div>
            )}

            {/* 4. SUPPORT TAB */}
            {activeTab === 'support' && (
              <motion.div 
                key="support"
                initial={{ opacity: 0, y: 20 }} 
                animate={{ opacity: 1, y: 0 }} 
                exit={{ opacity: 0, y: -20 }}
              >
                <Support />
              </motion.div>
            )}

          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}
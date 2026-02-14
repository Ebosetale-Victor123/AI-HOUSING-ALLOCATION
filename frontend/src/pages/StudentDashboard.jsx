import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Menu, Bell, ChevronRight, Sparkles } from 'lucide-react';

// CORRECT PATHS FOR THE DASHBOARD
import Sidebar from '../components/layout/Sidebar';
import ApplicationWizard from '../components/student/ApplicationWizard';
import HostelGallery from '../components/student/HostelGallery';
import Support from '../components/student/Support';

export default function StudentDashboard() {
  const [activeTab, setActiveTab] = useState('overview');
  const [sidebarOpen, setSidebarOpen] = useState(false);
  
  // MOCK USER DATA (In the future, this will be fetched from the Django API)
  const user = { name: "Henry Swazch", email: "henryswazch@gmail.com" };
  
  // MOCK APPLICATION STATE
  // Toggle this to 'true' to simulate a student who has already applied
  const [hasApplication, setHasApplication] = useState(false);

  const handleFormSubmit = (data) => {
    console.log("Form Data Captured:", data);
    setHasApplication(true);
    setActiveTab('overview');
  };

  return (
    <div className="min-h-screen bg-[#fcfcfd]">
      {/* Mobile Sidebar Overlay */}
      {sidebarOpen && (
        <div 
          className="fixed inset-0 bg-slate-900/20 backdrop-blur-sm z-40 lg:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

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
              <button onClick={() => setSidebarOpen(true)} className="lg:hidden p-2 hover:bg-slate-100 rounded-lg transition-colors">
                <Menu className="w-6 h-6 text-slate-600" />
              </button>
              <div>
                <h1 className="text-xl font-black text-slate-900 capitalize tracking-tight">{activeTab.replace('-', ' ')}</h1>
                <p className="text-xs font-bold text-slate-400 uppercase tracking-widest">Welcome back, {user.name.split(' ')[0]}</p>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <button className="relative p-2.5 bg-slate-50 rounded-xl hover:bg-slate-100 transition-all group">
                <Bell className="w-5 h-5 text-slate-500 group-hover:text-indigo-600" />
                <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-indigo-600 rounded-full border-2 border-white" />
              </button>
            </div>
          </div>
        </header>

        {/* Dashboard Content Area */}
        <div className="p-8 max-w-7xl mx-auto">
          <AnimatePresence mode="wait">
            
            {/* OVERVIEW TAB */}
            {activeTab === 'overview' && (
              <motion.div 
                key="overview"
                initial={{ opacity: 0, y: 20 }} 
                animate={{ opacity: 1, y: 0 }} 
                exit={{ opacity: 0, y: -20 }}
                className="space-y-8"
              >
                {!hasApplication ? (
                  /* Hero CTA for New Students */
                  <div className="relative overflow-hidden bg-gradient-to-r from-indigo-600 via-blue-600 to-cyan-500 rounded-[40px] p-12 text-white shadow-2xl shadow-indigo-200">
                    <div className="absolute top-0 right-0 p-8 opacity-10 pointer-events-none">
                       <Sparkles className="w-64 h-64" />
                    </div>
                    <div className="relative z-10 max-w-lg">
                      <h2 className="text-4xl font-black mb-4 leading-tight">Secure Your Campus Home with AI</h2>
                      <p className="text-indigo-50 font-medium mb-10 leading-relaxed text-lg opacity-90">
                        Our intelligent allocation system is open. Apply now to be ranked based on your academic merit and logistics needs.
                      </p>
                      <button 
                        onClick={() => setActiveTab('application')}
                        className="px-10 py-4 bg-white text-indigo-600 font-black rounded-2xl shadow-xl hover:scale-105 active:scale-95 transition-all flex items-center gap-2 group"
                      >
                        Start Application <ChevronRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
                      </button>
                    </div>
                  </div>
                ) : (
                  /* Summary for Students who have applied */
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                    <div className="p-8 bg-white rounded-[32px] border border-slate-100 shadow-sm">
                       <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">Application Status</p>
                       <div className="flex items-center gap-2">
                          <div className="w-2 h-2 rounded-full bg-amber-500 animate-pulse" />
                          <span className="text-xl font-black text-slate-900">Processing...</span>
                       </div>
                    </div>
                    <div className="p-8 bg-white rounded-[32px] border border-slate-100 shadow-sm">
                       <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">Estimated AI Score</p>
                       <span className="text-xl font-black text-indigo-600 font-mono tracking-tighter italic">Calculating</span>
                    </div>
                    <div className="p-8 bg-white rounded-[32px] border border-slate-100 shadow-sm">
                       <p className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-2">Hostel Preference</p>
                       <span className="text-xl font-black text-slate-900">Any Available</span>
                    </div>
                  </div>
                )}

                {/* Info Cards Section */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                  <div className="p-10 bg-white rounded-[32px] border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
                    <h3 className="text-xl font-black text-slate-900 mb-3">Hostel Guidelines 2026</h3>
                    <p className="text-slate-500 leading-relaxed mb-6">Review the updated codes of conduct and facility usage policies before moving in.</p>
                    <button className="text-indigo-600 font-bold text-sm flex items-center gap-1 hover:gap-2 transition-all">
                      Read Policy <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                  <div className="p-10 bg-white rounded-[32px] border border-slate-100 shadow-sm hover:shadow-md transition-shadow">
                    <h3 className="text-xl font-black text-slate-900 mb-3">Important Deadlines</h3>
                    <p className="text-slate-500 leading-relaxed mb-6">Final AI rankings and room assignments will be published on the portal on October 24th.</p>
                    <button className="text-indigo-600 font-bold text-sm flex items-center gap-1 hover:gap-2 transition-all">
                      View Calendar <ChevronRight className="w-4 h-4" />
                    </button>
                  </div>
                </div>
              </motion.div>
            )}

            {/* MY APPLICATION TAB */}
            {activeTab === 'application' && (
              <motion.div 
                key="application"
                initial={{ opacity: 0, x: 20 }} 
                animate={{ opacity: 1, x: 0 }} 
                exit={{ opacity: 0, x: -20 }}
              >
                {hasApplication ? (
                  <div className="text-center py-20 bg-white rounded-[40px] border border-slate-100">
                    <div className="w-20 h-20 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-6">
                      <Sparkles className="w-10 h-10" />
                    </div>
                    <h2 className="text-2xl font-black text-slate-900 mb-2">Your application is in the cloud!</h2>
                    <p className="text-slate-500 mb-8">You have already submitted your data. The AI is now processing your rank.</p>
                    <button 
                      onClick={() => setHasApplication(false)} 
                      className="text-xs font-bold text-indigo-600 uppercase tracking-widest hover:underline"
                    >
                      Reset Application (Debug Mode)
                    </button>
                  </div>
                ) : (
                  <ApplicationWizard onSubmit={handleFormSubmit} />
                )}
              </motion.div>
            )}

            {/* HOSTEL GALLERY TAB */}
            {activeTab === 'hostels' && (
              <motion.div 
                key="hostels"
                initial={{ opacity: 0, scale: 0.98 }} 
                animate={{ opacity: 1, scale: 1 }} 
                exit={{ opacity: 0, scale: 0.98 }}
              >
                <div className="mb-10 text-center md:text-left">
                   <h2 className="text-3xl font-black text-slate-900">Explore Accommodations</h2>
                   <p className="text-slate-500 font-medium">Browse our smart residences and filter by your preference.</p>
                </div>
                <HostelGallery />
              </motion.div>
            )}

            {/* SUPPORT TAB */}
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
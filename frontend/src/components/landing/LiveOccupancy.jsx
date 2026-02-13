import React from 'react';
import { motion } from 'framer-motion';
import { Activity, Users, LayoutDashboard, Radio } from 'lucide-react';

export default function LiveOccupancy() {
  return (
    <section className="py-24 bg-[#0f172a] text-white overflow-hidden relative">
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-full h-full bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-indigo-500/10 via-transparent to-transparent" />
      
      <div className="max-w-7xl mx-auto px-6 relative z-10">
        <div className="text-center mb-16">
          <span className="px-4 py-1 rounded-full bg-emerald-500/10 text-emerald-400 text-xs font-bold border border-emerald-500/20 uppercase tracking-widest">
            ● Live Occupancy Data
          </span>
          <h2 className="text-4xl font-bold mt-6">Real-Time Availability</h2>
          <p className="text-slate-400 mt-4">Monitor housing availability across all campus residences in real-time.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Card 1 */}
          <div className="p-8 bg-slate-800/40 backdrop-blur-md rounded-3xl border border-slate-700/50 hover:border-indigo-500/50 transition-colors">
            <div className="flex justify-between items-start mb-6">
              <LayoutDashboard className="w-8 h-8 text-indigo-400" />
              <span className="text-[10px] text-slate-500 uppercase font-bold tracking-tighter">Total Capacity</span>
            </div>
            <div className="text-4xl font-bold mb-1">1,300</div>
            <div className="text-slate-400 text-sm italic">Beds across 6 hostels</div>
          </div>

          {/* Card 2 */}
          <div className="p-8 bg-indigo-600 rounded-3xl shadow-xl shadow-indigo-900/20 border border-indigo-500 hover:scale-[1.02] transition-transform">
            <div className="flex justify-between items-start mb-6">
              <Users className="w-8 h-8 text-indigo-100" />
              <span className="text-[10px] text-indigo-200 uppercase font-bold tracking-tighter">Available Now</span>
            </div>
            <div className="text-4xl font-bold mb-1">99</div>
            <div className="text-indigo-100 text-sm italic">Spots ready for allocation</div>
          </div>

          {/* Card 3 */}
          <div className="p-8 bg-slate-800/40 backdrop-blur-md rounded-3xl border border-slate-700/50 hover:border-cyan-500/50 transition-colors">
            <div className="flex justify-between items-start mb-6">
              <Activity className="w-8 h-8 text-cyan-400" />
              <span className="text-[10px] text-slate-500 uppercase font-bold tracking-tighter">Occupancy Rate</span>
            </div>
            <div className="text-4xl font-bold mb-4">92.4%</div>
            <div className="w-full bg-slate-700 h-2 rounded-full overflow-hidden">
              <motion.div 
                initial={{ width: 0 }}
                whileInView={{ width: '92.4%' }}
                className="h-full bg-gradient-to-r from-indigo-500 to-cyan-400" 
              />
            </div>
          </div>
        </div>

        {/* Live Hostel Status (Luna House) - Placed below the grid */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          className="mt-16 max-w-4xl mx-auto p-[1px] bg-gradient-to-r from-transparent via-indigo-500/50 to-transparent rounded-3xl"
        >
          <div className="bg-[#1e293b]/50 backdrop-blur-xl rounded-[23px] p-8 border border-white/5">
            <div className="flex items-center justify-between mb-8 border-b border-white/10 pb-4">
              <div className="flex items-center gap-2 text-emerald-400">
                <Radio className="w-4 h-4 animate-pulse" />
                <span className="text-[10px] font-bold uppercase tracking-widest">Live Hostel Status</span>
              </div>
              <div className="flex gap-1">
                {[1, 2, 3, 4].map(i => <div key={i} className={`w-1.5 h-1.5 rounded-full ${i === 4 ? 'bg-emerald-500' : 'bg-slate-700'}`} />)}
              </div>
            </div>
            
            <div className="flex flex-col md:flex-row justify-between items-center gap-6">
              <div className="text-center md:text-left">
                <h3 className="text-3xl font-bold text-white">Luna House</h3>
                <p className="text-slate-400 text-sm">Female Residence • West Wing Premium</p>
              </div>
              
              <div className="flex items-baseline gap-3">
                <span className="text-7xl font-black text-emerald-500 drop-shadow-[0_0_15px_rgba(16,185,129,0.3)]">8</span>
                <div className="text-slate-500 text-xs font-bold leading-tight uppercase tracking-tighter">
                  beds available <br /> of 150
                </div>
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </section>
  );
}
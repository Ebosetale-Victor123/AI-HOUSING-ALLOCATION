import React, { useState } from 'react';
import { Brain, Settings, Zap, Loader2, CheckCircle2 } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

export default function AIAllocationEngine() {
  const [status, setStatus] = useState('idle'); // idle, running, complete
  const [progress, setProgress] = useState(0);

  const startAI = async () => {
    setStatus('running');
    for (let i = 0; i <= 100; i += 10) {
      await new Promise(r => setTimeout(r, 200));
      setProgress(i);
    }
    setStatus('complete');
  };

  return (
    <div className="bg-white rounded-[32px] border border-slate-100 shadow-sm overflow-hidden">
      {/* Card Header */}
      <div className="p-8 flex justify-between items-center border-b border-slate-50">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center">
            <Brain className="w-6 h-6" />
          </div>
          <div>
            <h3 className="font-bold text-slate-900">AI Allocation Engine</h3>
            <p className="text-xs text-slate-400 font-medium tracking-tight">Automated housing assignment system</p>
          </div>
        </div>
        <button className="flex items-center gap-2 px-4 py-2 border border-slate-100 rounded-xl text-xs font-bold text-slate-500 hover:bg-slate-50">
          <Settings className="w-4 h-4" /> Configure
        </button>
      </div>

      {/* Main Action Area */}
      <div className="p-16 text-center">
        <AnimatePresence mode="wait">
          {status === 'idle' && (
            <motion.div key="idle" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <div className="relative inline-block group">
                {/* Neon Glow */}
                <div className="absolute inset-0 bg-indigo-600 rounded-2xl blur-2xl opacity-40 group-hover:opacity-60 transition-opacity animate-pulse" />
                <button 
                  onClick={startAI}
                  className="relative px-12 py-6 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-black rounded-2xl flex items-center gap-3 shadow-2xl hover:scale-105 active:scale-95 transition-all uppercase tracking-tight"
                >
                  <Zap className="w-6 h-6" /> Initialize AI Allocation Algorithm
                </button>
              </div>
              <p className="mt-8 text-sm text-slate-400 max-w-sm mx-auto leading-relaxed">
                This will process all pending applications and assign housing based on merit, need, and availability.
              </p>
            </motion.div>
          )}

          {status === 'running' && (
            <motion.div key="running" initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-8">
               <div className="relative w-24 h-24 mx-auto">
                 <Loader2 className="w-full h-full text-indigo-600 animate-spin" />
                 <Brain className="w-8 h-8 absolute top-8 left-8 text-indigo-600 animate-pulse" />
               </div>
               <div className="max-w-xs mx-auto">
                  <div className="flex justify-between text-xs font-black text-indigo-600 uppercase mb-2">
                    <span>Processing Neural Weights</span>
                    <span>{progress}%</span>
                  </div>
                  <div className="h-3 bg-slate-100 rounded-full overflow-hidden">
                    <motion.div 
                      className="h-full bg-indigo-600"
                      initial={{ width: 0 }}
                      animate={{ width: `${progress}%` }}
                    />
                  </div>
               </div>
            </motion.div>
          )}

          {status === 'complete' && (
            <motion.div key="complete" initial={{ scale: 0.9 }} animate={{ scale: 1 }} className="py-4">
              <div className="w-20 h-20 bg-emerald-50 text-emerald-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <CheckCircle2 className="w-10 h-10" />
              </div>
              <h4 className="text-2xl font-black text-slate-900 mb-2">Success!</h4>
              <p className="text-slate-500 mb-8">Allocation cycle complete. Notifications sent.</p>
              <button onClick={() => setStatus('idle')} className="text-indigo-600 font-bold hover:underline">Restart Engine</button>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Bottom Summary Stats */}
      <div className="grid grid-cols-3 gap-6 p-8 bg-slate-50/50 border-t border-slate-50">
        <div className="bg-white p-6 rounded-3xl text-center border border-slate-100 shadow-sm">
          <div className="text-3xl font-black text-indigo-600">234</div>
          <div className="text-[10px] text-slate-400 font-black uppercase tracking-widest mt-1">Pending</div>
        </div>
        <div className="bg-white p-6 rounded-3xl text-center border border-slate-100 shadow-sm">
          <div className="text-3xl font-black text-cyan-500">99</div>
          <div className="text-[10px] text-slate-400 font-black uppercase tracking-widest mt-1">Available</div>
        </div>
        <div className="bg-white p-6 rounded-3xl text-center border border-slate-100 shadow-sm">
          <div className="text-3xl font-black text-emerald-500">~2min</div>
          <div className="text-[10px] text-slate-400 font-black uppercase tracking-widest mt-1">Est. Time</div>
        </div>
      </div>
    </div>
  );
}
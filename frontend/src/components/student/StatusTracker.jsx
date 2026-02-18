import React from 'react';
import { motion } from 'framer-motion';
import { Brain, Clock, CheckCircle2 } from 'lucide-react';

export default function StatusTracker({ status }) {
  return (
    <div className="space-y-4">
      <div className="bg-blue-600 rounded-[28px] p-8 text-white shadow-xl relative overflow-hidden">
        <div className="flex items-center gap-4 mb-6">
          <div className="p-3 bg-white/20 rounded-2xl backdrop-blur-md"><Brain className="w-6 h-6 text-white" /></div>
          <div>
            <h4 className="font-black text-lg tracking-tight uppercase">AI ANALYSING</h4>
            <p className="text-blue-100 text-[10px] font-bold uppercase tracking-widest">Processing Data...</p>
          </div>
        </div>
        <div className="h-1.5 w-full bg-blue-400/50 rounded-full overflow-hidden mb-4">
          <motion.div 
            initial={{ width: 0 }} animate={{ width: '100%' }} 
            transition={{ duration: 3, repeat: Infinity }}
            className="h-full bg-white shadow-[0_0_10px_white]" 
          />
        </div>
        <p className="text-[10px] text-blue-100 font-medium leading-relaxed opacity-80 uppercase tracking-tighter">Verified by Caleb University AI Node</p>
      </div>

      <div className="bg-[#fffbeb] rounded-[28px] p-8 border border-amber-100">
        <div className="flex items-center gap-4 mb-4">
           <Clock className="w-6 h-6 text-amber-600" />
           <h4 className="font-black text-amber-900 uppercase tracking-tighter text-sm">Pending Approval</h4>
        </div>
        <p className="text-amber-700/70 text-[11px] font-bold leading-relaxed uppercase">The Caleb University housing team will verify your documents after the AI ranking cycle.</p>
      </div>
    </div>
  );
}
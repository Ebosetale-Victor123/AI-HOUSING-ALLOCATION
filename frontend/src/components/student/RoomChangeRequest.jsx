import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { RefreshCw, AlertCircle } from 'lucide-react';

export default function RoomChangeRequest({ user }) {
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="max-w-4xl mx-auto">
      <div className="bg-white rounded-[32px] border border-slate-100 overflow-hidden shadow-sm">
        <div className="p-8 bg-green-700 text-white flex items-center gap-4">
          <RefreshCw className="w-8 h-8" />
          <div>
            <h2 className="text-2xl font-black uppercase tracking-tight">Room Change Request</h2>
            <p className="text-green-100 text-xs font-bold uppercase tracking-widest">Formal Reassignment Portal</p>
          </div>
        </div>
        
        <div className="p-12 text-center">
          <div className="w-20 h-20 bg-slate-50 rounded-full flex items-center justify-center mx-auto mb-6">
            <AlertCircle className="w-10 h-10 text-slate-300" />
          </div>
          <h3 className="text-xl font-bold text-slate-900 mb-2">No Active Allocation Found</h3>
          <p className="text-slate-500 max-w-sm mx-auto leading-relaxed">
            You can only request a room change after the AI has assigned you a room. Please complete your initial application first.
          </p>
        </div>
      </div>
    </motion.div>
  );
}
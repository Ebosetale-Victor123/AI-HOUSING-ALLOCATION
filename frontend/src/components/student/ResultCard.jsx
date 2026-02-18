import React from 'react';
import { motion } from 'framer-motion';
import { Trophy, Building2, MapPin, Calendar, Star, Sparkles } from 'lucide-react';

export default function ResultCard({ application }) {
  if (!application || application.status !== 'allocated') return null;

  const scoreColor = application.ai_priority_score >= 80 ? 'emerald' : 
                     application.ai_priority_score >= 60 ? 'cyan' : 'amber';

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
      className="relative overflow-hidden"
    >
      {/* Glassmorphic Card */}
      <div className="relative bg-gradient-to-br from-white/80 to-white/60 backdrop-blur-xl rounded-3xl border border-white/50 shadow-2xl shadow-indigo-500/10 p-8">
        {/* Background Decorations */}
        <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-indigo-500/10 to-cyan-500/10 rounded-full blur-3xl -z-10" />
        <div className="absolute bottom-0 left-0 w-48 h-48 bg-gradient-to-tr from-emerald-500/10 to-cyan-500/10 rounded-full blur-3xl -z-10" />

        {/* Header */}
        <div className="flex items-start justify-between mb-8">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-5 h-5 text-indigo-600" />
              <span className="text-sm font-semibold text-indigo-600 uppercase tracking-wider">
                Housing Allocated
              </span>
            </div>
            <h2 className="text-2xl font-bold text-slate-900">
              Congratulations, {application.student_name?.split(' ')[0]}!
            </h2>
          </div>
          <div className="flex items-center gap-2 px-4 py-2 bg-emerald-100 rounded-full">
            <Trophy className="w-4 h-4 text-emerald-600" />
            <span className="text-sm font-semibold text-emerald-700">Successful</span>
          </div>
        </div>

        {/* AI Score */}
        <div className="bg-gradient-to-r from-slate-900 to-slate-800 rounded-2xl p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-slate-400 text-sm mb-1">Your AI Priority Score</p>
              <div className="flex items-baseline gap-2">
                <span className={`text-5xl font-bold text-${scoreColor}-400`}>
                  {application.ai_priority_score || 85}
                </span>
                <span className="text-slate-500">/100</span>
              </div>
            </div>
            <div className="flex gap-1">
              {[...Array(5)].map((_, i) => (
                <Star
                  key={i}
                  className={`w-6 h-6 ${
                    i < Math.ceil((application.ai_priority_score || 85) / 20)
                      ? 'text-amber-400 fill-amber-400'
                      : 'text-slate-600'
                  }`}
                />
              ))}
            </div>
          </div>
          
          {/* Score Breakdown */}
          <div className="mt-4 pt-4 border-t border-slate-700 grid grid-cols-4 gap-4">
            {[
              { label: 'Merit', value: '25%', color: 'indigo' },
              { label: 'Distance', value: '30%', color: 'cyan' },
              { label: 'Financial', value: '25%', color: 'emerald' },
              { label: 'Medical', value: '20%', color: 'amber' },
            ].map((factor) => (
              <div key={factor.label} className="text-center">
                <p className={`text-${factor.color}-400 font-bold`}>{factor.value}</p>
                <p className="text-slate-500 text-xs">{factor.label}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Room Details */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="flex items-start gap-4 p-4 bg-slate-50 rounded-xl">
            <div className="w-12 h-12 rounded-xl bg-indigo-100 flex items-center justify-center">
              <Building2 className="w-6 h-6 text-indigo-600" />
            </div>
            <div>
              <p className="text-sm text-slate-500 mb-1">Assigned Hostel</p>
              <p className="font-semibold text-slate-900">{application.assigned_hostel || 'Aurora Hall'}</p>
            </div>
          </div>

          <div className="flex items-start gap-4 p-4 bg-slate-50 rounded-xl">
            <div className="w-12 h-12 rounded-xl bg-cyan-100 flex items-center justify-center">
              <MapPin className="w-6 h-6 text-cyan-600" />
            </div>
            <div>
              <p className="text-sm text-slate-500 mb-1">Room Number</p>
              <p className="font-semibold text-slate-900">{application.assigned_room || 'A-312'}</p>
            </div>
          </div>

          <div className="flex items-start gap-4 p-4 bg-slate-50 rounded-xl md:col-span-2">
            <div className="w-12 h-12 rounded-xl bg-emerald-100 flex items-center justify-center">
              <Calendar className="w-6 h-6 text-emerald-600" />
            </div>
            <div>
              <p className="text-sm text-slate-500 mb-1">Move-in Date</p>
              <p className="font-semibold text-slate-900">August 15, 2026 - May 15, 2027</p>
              <p className="text-sm text-slate-500 mt-1">Academic Year 2026-2027</p>
            </div>
          </div>
        </div>

        {/* Action Button */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          className="w-full mt-6 py-4 bg-gradient-to-r from-indigo-600 to-cyan-600 text-white font-semibold rounded-xl shadow-lg shadow-indigo-200 hover:shadow-xl transition-shadow"
        >
          Download Allocation Letter
        </motion.button>
      </div>
    </motion.div>
  );
}
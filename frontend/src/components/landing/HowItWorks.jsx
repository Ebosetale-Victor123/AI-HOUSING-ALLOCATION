import React from 'react';
import { motion } from 'framer-motion';
import { ClipboardList, BrainCircuit, CheckCircle2 } from 'lucide-react';

const steps = [
  {
    id: '01',
    title: 'Data Submission',
    desc: 'Submit your academic records, financial info, and personal details through our secure portal.',
    icon: ClipboardList,
    color: 'bg-indigo-600'
  },
  {
    id: '02',
    title: 'AI Merit & Need Analysis',
    desc: 'Our advanced AI evaluates your application based on merit, financial need, distance, and special requirements.',
    icon: BrainCircuit,
    color: 'bg-cyan-500'
  },
  {
    id: '03',
    title: 'Instant Transparent Allocation',
    desc: 'Receive your housing assignment with full transparency on how your priority score was calculated.',
    icon: CheckCircle2,
    color: 'bg-emerald-500'
  }
];

export default function HowItWorks() {
  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-center mb-20">
          <span className="text-indigo-600 font-bold tracking-widest text-xs uppercase">Simple Process</span>
          <h2 className="text-4xl font-bold text-slate-900 mt-3">How It Works</h2>
          <p className="text-slate-500 mt-4 max-w-xl mx-auto">Three simple steps to secure your campus accommodation through our AI-powered system.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {steps.map((step, index) => (
            <motion.div 
              key={step.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.2 }}
              className="relative group p-8 rounded-3xl border border-slate-100 hover:border-indigo-100 transition-all hover:shadow-2xl hover:shadow-indigo-50"
            >
              <div className="text-6xl font-black text-slate-50 mb-4 group-hover:text-indigo-50 transition-colors">{step.id}</div>
              <div className={`w-12 h-12 ${step.color} text-white rounded-xl flex items-center justify-center mb-6 shadow-lg`}>
                <step.icon className="w-6 h-6" />
              </div>
              <h3 className="text-xl font-bold text-slate-800 mb-3">{step.title}</h3>
              <p className="text-slate-500 leading-relaxed">{step.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
}
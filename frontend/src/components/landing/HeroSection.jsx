import React from 'react';
import { motion } from 'framer-motion';
import { ArrowRight, Sparkles, Building2, Users, Shield } from 'lucide-react';
import { Link } from 'react-router-dom';

export default function HeroSection() {
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: { staggerChildren: 0.2 }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { y: 0, opacity: 1 }
  };

  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden bg-[#f8fafc]">
      {/* Premium Background Blobs */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-indigo-200/30 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-cyan-200/30 rounded-full blur-[120px]" />
      </div>

      <motion.div 
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="relative z-10 max-w-7xl mx-auto px-6 py-20 text-center"
      >
        {/* Animated Badge */}
        <motion.div variants={itemVariants} className="flex justify-center mb-6">
          <span className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-white border border-indigo-100 text-indigo-600 text-sm font-semibold shadow-sm">
            <Sparkles className="w-4 h-4 text-amber-400" />
            Next-Gen Allocation Engine
          </span>
        </motion.div>

        {/* Headline */}
        <motion.h1 
  variants={itemVariants} 
  className="text-6xl md:text-8xl font-extrabold text-slate-900 tracking-tight mb-6"
>
  Revolutionizing<br />
  <span className="bg-gradient-to-r from-indigo-600 to-cyan-500 bg-clip-text text-transparent">
    Student Housing
  </span>
  <br /> {/* This is the break you requested */}
  <span className="text-slate-900"> {/* This is now solid black */}
    with AI.
  </span>
</motion.h1>

        {/* Subtitle */}
        <motion.p variants={itemVariants} className="text-xl text-slate-500 max-w-2xl mx-auto mb-10 leading-relaxed">
          The era of "first-come, first-served" is over. Our algorithm ensures every student gets a fair chance based on academic merit, distance, and genuine need.
        </motion.p>

        {/* Revamped Buttons */}
        <motion.div variants={itemVariants} className="flex flex-col sm:flex-row items-center justify-center gap-5 mb-20">
          <Link to="/auth" className="group relative px-8 py-4 bg-indigo-600 text-white font-bold rounded-2xl transition-all hover:scale-105 hover:bg-indigo-700 shadow-xl shadow-indigo-200">
            <span className="flex items-center gap-2">
              Get Started <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </span>
          </Link>
          <button className="px-8 py-4 bg-white text-slate-700 font-bold rounded-2xl border border-slate-200 hover:bg-slate-50 transition-all shadow-sm">
            Contact Us
          </button>
        </motion.div>

        {/* Stats Grid */}
        <motion.div variants={itemVariants} className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {[
            { icon: Building2, label: "Smart Hostels", value: "24", color: "text-indigo-600" },
            { icon: Users, label: "Happy Students", value: "12.4k", color: "text-cyan-600" },
            { icon: Shield, label: "Trust Score", value: "99.9%", color: "text-emerald-600" },
          ].map((stat) => (
            <div key={stat.label} className="p-8 bg-white/50 backdrop-blur-md rounded-3xl border border-white shadow-sm hover:shadow-md transition-all group">
              <stat.icon className={`w-10 h-10 ${stat.color} mb-4 mx-auto group-hover:scale-110 transition-transform`} />
              <div className="text-4xl font-black text-slate-800 mb-1">{stat.value}</div>
              <div className="text-sm uppercase tracking-widest font-bold text-slate-400">{stat.label}</div>
            </div>
          ))}
        </motion.div>
      </motion.div>
    </section>
  );
}
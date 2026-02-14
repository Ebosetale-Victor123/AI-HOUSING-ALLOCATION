import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Building2, Mail, Lock, User, ArrowRight, GraduationCap, Shield } from 'lucide-react';
import { Link, useNavigate } from 'react-router-dom';

export default function Auth() {
  const [mode, setMode] = useState('login'); // login or signup
  const [role, setRole] = useState('student'); // student or admin
  const navigate = useNavigate();

  // Mock login function for now
  const handleAuth = (e) => {
    e.preventDefault();
    // Later, your partner will provide the real API for this
    if (role === 'student') {
      navigate('/student-dashboard');
    } else {
      navigate('/admin-dashboard');
    }
  };

  return (
    <div className="min-h-screen bg-[#f8fafc] flex items-center justify-center p-6 relative overflow-hidden">
      
      {/* Background Animated Blobs */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-indigo-200/30 rounded-full blur-[120px] animate-pulse" />
        <div className="absolute bottom-[-10%] left-[-10%] w-[500px] h-[500px] bg-cyan-200/30 rounded-full blur-[120px]" />
      </div>

      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        className="relative z-10 w-full max-w-md"
      >
        {/* Logo Section */}
        <Link to="/" className="flex items-center justify-center gap-3 mb-10 group">
          <div className="w-12 h-12 rounded-2xl bg-indigo-600 flex items-center justify-center shadow-lg shadow-indigo-200 group-hover:rotate-12 transition-transform">
            <Building2 className="w-6 h-6 text-white" />
          </div>
          <span className="text-2xl font-black text-slate-900 tracking-tighter uppercase">UniHousing AI</span>
        </Link>

        {/* Main Card */}
        <div className="bg-white/70 backdrop-blur-2xl rounded-[32px] shadow-2xl shadow-indigo-100/50 border border-white overflow-hidden">
          
          {/* Role Toggle Switch */}
          <div className="p-2 bg-slate-100/50 m-4 rounded-2xl relative flex">
             {/* The Animated Background Slider */}
             <motion.div 
               animate={{ x: role === 'student' ? 0 : '100%' }}
               className="absolute top-2 left-2 w-[calc(50%-8px)] h-[calc(100%-16px)] bg-white rounded-xl shadow-sm border border-slate-200"
             />
             
             <button
               onClick={() => setRole('student')}
               className={`relative z-10 w-1/2 flex items-center justify-center gap-2 py-3 text-sm font-bold transition-colors ${role === 'student' ? 'text-indigo-600' : 'text-slate-500'}`}
             >
               <GraduationCap className="w-4 h-4" /> Student
             </button>
             <button
               onClick={() => setRole('admin')}
               className={`relative z-10 w-1/2 flex items-center justify-center gap-2 py-3 text-sm font-bold transition-colors ${role === 'admin' ? 'text-indigo-600' : 'text-slate-500'}`}
             >
               <Shield className="w-4 h-4" /> Staff/Admin
             </button>
          </div>

          <div className="p-8 pt-4">
            <div className="text-center mb-8">
              <h1 className="text-3xl font-black text-slate-900 mb-2">
                {mode === 'login' ? 'Welcome Back' : 'Get Started'}
              </h1>
              <p className="text-slate-500 font-medium">
                {role === 'student' ? 'Student Portal Access' : 'Administrative Control Panel'}
              </p>
            </div>

            <form onSubmit={handleAuth} className="space-y-5">
              <AnimatePresence mode="wait">
                {mode === 'signup' && (
                  <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }} exit={{ opacity: 0, height: 0 }} className="space-y-2">
                    <label className="text-xs font-bold text-slate-400 uppercase tracking-widest ml-1">Full Name</label>
                    <div className="relative group">
                      <User className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-indigo-500 transition-colors" />
                      <input type="text" placeholder="Full Name" className="w-full pl-12 pr-4 h-14 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 transition-all font-medium" />
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-400 uppercase tracking-widest ml-1">Email Address</label>
                <div className="relative group">
                  <Mail className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-indigo-500 transition-colors" />
                  <input type="email" required placeholder="name@university.edu" className="w-full pl-12 pr-4 h-14 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 transition-all font-medium" />
                </div>
              </div>

              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-400 uppercase tracking-widest ml-1">Password</label>
                <div className="relative group">
                  <Lock className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400 group-focus-within:text-indigo-500 transition-colors" />
                  <input type="password" required placeholder="••••••••" className="w-full pl-12 pr-4 h-14 bg-slate-50 border border-slate-200 rounded-2xl focus:outline-none focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 transition-all font-medium" />
                </div>
              </div>

              {mode === 'login' && (
                <div className="flex justify-end">
                  <button type="button" className="text-sm text-indigo-600 hover:text-indigo-700 font-bold transition-colors">
                    Forgot password?
                  </button>
                </div>
              )}

              <button type="submit" className="w-full h-14 bg-slate-900 text-white font-bold rounded-2xl shadow-lg shadow-slate-200 hover:bg-indigo-600 hover:shadow-indigo-200 hover:-translate-y-1 transition-all flex items-center justify-center gap-2 group">
                {mode === 'login' ? 'Sign In' : 'Create Account'}
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </button>
            </form>

            <div className="mt-8 text-center">
              <p className="text-slate-500 font-medium">
                {mode === 'login' ? "New here?" : "Already have an account?"}
                {' '}
                <button
                  onClick={() => setMode(mode === 'login' ? 'signup' : 'login')}
                  className="text-indigo-600 hover:text-indigo-700 font-black"
                >
                  {mode === 'login' ? 'Sign up' : 'Sign in'}
                </button>
              </p>
            </div>
          </div>
        </div>

        <p className="text-center text-xs text-slate-400 mt-8 font-medium">
          Protected by Campus Security & AI Verification.
        </p>
      </motion.div>
    </div>
  );
}
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Sparkles, Brain, Clock, ChevronRight, MapPin, GraduationCap, ShieldCheck, Phone, Mail, FileText } from 'lucide-react';

export default function OverviewTab({ user }) {
  // 1. Manage the View State
  const [view, setView] = useState('banner'); // banner, form, summary
  
  // 2. Manage Dynamic Form Data
  const [formData, setFormData] = useState({
    fullName: user?.name || 'Henry Swazch', // Pulls from logged-in user
    matricNo: '',
    email: user?.email || '',
    phone: '',
    department: 'Computer Science',
    level: '100L',
    gpa: '',
    homeAddress: '',
    distance: '',
    financialStatus: 'No Scholarship',
    hasDisability: 'No',
    disabilityDetail: ''
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({ ...prev, [name]: value }));
  };

  const handleFormSubmit = (e) => {
    e.preventDefault();
    setView('summary'); // This fixes the blank page issue
  };

  const inputClass = "w-full px-5 py-4 bg-slate-50 border border-slate-200 rounded-2xl focus:ring-4 focus:ring-green-500/10 focus:border-green-600 outline-none transition-all font-bold text-slate-700 placeholder:text-slate-300";
  const labelClass = "text-[10px] font-black text-slate-400 uppercase tracking-[2px] ml-2 mb-2 block";

  return (
    <div className="max-w-6xl mx-auto pb-20">
      <AnimatePresence mode="wait">
        
        {/* VIEW 1: PREMIUM HERO BANNER */}
        {view === 'banner' && (
          <motion.div 
            key="banner" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, scale: 0.95 }}
            className="relative overflow-hidden bg-[#064e3b] rounded-[48px] p-16 text-white shadow-2xl"
          >
            <div className="relative z-10 max-w-2xl">
              <div className="inline-flex items-center gap-2 px-4 py-2 bg-white/10 backdrop-blur-md rounded-full mb-6 border border-white/10">
                <Sparkles className="w-4 h-4 text-yellow-400" />
                <span className="text-xs font-bold uppercase tracking-widest">Caleb University Admissions 2026</span>
              </div>
              <h2 className="text-5xl font-black mb-6 leading-tight tracking-tighter italic">Secure Your Campus <br/>Residence with AI</h2>
              <p className="text-green-50 font-medium mb-10 text-xl opacity-80 leading-relaxed">
                Welcome, <span className="text-yellow-400 font-black underline underline-offset-8">{formData.fullName}</span>. <br/>
                Our Neural Engine computes housing priority based on your specific needs.
              </p>
              <button 
                onClick={() => setView('form')}
                className="px-12 py-5 bg-white text-green-900 font-black rounded-2xl shadow-xl hover:bg-yellow-400 hover:scale-105 transition-all flex items-center gap-3 uppercase text-sm tracking-widest"
              >
                Apply for Hostel <ChevronRight className="w-5 h-5" />
              </button>
            </div>
            <Brain className="absolute -bottom-20 -right-20 w-96 h-96 text-white/5 rotate-12" />
          </motion.div>
        )}

        {/* VIEW 2: THE INSTITUTIONAL FORM */}
        {view === 'form' && (
          <motion.div 
            key="form" initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, scale: 0.95 }}
            className="bg-white rounded-[48px] border border-slate-100 p-12 shadow-2xl"
          >
            <div className="max-w-4xl mx-auto">
              <header className="text-center mb-16">
                <h3 className="text-3xl font-black text-slate-900 tracking-tighter uppercase">Student Residency Application</h3>
                <div className="h-1 w-20 bg-green-600 mx-auto mt-4 rounded-full" />
              </header>

              <form onSubmit={handleFormSubmit} className="space-y-10">
                {/* ID SECTION */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 bg-slate-50/50 p-8 rounded-[32px] border border-slate-100">
                   <div className="space-y-1">
                      <label className={labelClass}>Full Name</label>
                      <input type="text" name="fullName" value={formData.fullName} className={inputClass} readOnly />
                   </div>
                   <div className="space-y-1">
                      <label className={labelClass}>Matric Number</label>
                      <input type="text" name="matricNo" placeholder="21/0452" className={inputClass} required onChange={handleInputChange} />
                   </div>
                   <div className="space-y-1">
                      <label className={labelClass}>Phone Number</label>
                      <input type="tel" name="phone" placeholder="0810 000 0000" className={inputClass} required onChange={handleInputChange} />
                   </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
                  {/* ACADEMICS */}
                  <div className="space-y-6">
                    <h4 className="font-black text-slate-900 uppercase tracking-widest text-xs flex items-center gap-2 border-l-4 border-green-600 pl-4">
                      Academic Details
                    </h4>
                    <div className="space-y-4">
                      <select name="department" className={inputClass} onChange={handleInputChange}><option>Computer Science</option><option>Mass Comm</option><option>Law</option></select>
                      <select name="level" className={inputClass} onChange={handleInputChange}><option>100L</option><option>200L</option><option>300L</option><option>400L</option></select>
                      <input name="gpa" type="number" step="0.01" placeholder="Current CGPA (e.g 4.52)" className={inputClass} required onChange={handleInputChange} />
                    </div>
                  </div>

                  {/* LOGISTICS */}
                  <div className="space-y-6">
                    <h4 className="font-black text-slate-900 uppercase tracking-widest text-xs flex items-center gap-2 border-l-4 border-green-600 pl-4">
                      Logistics Need
                    </h4>
                    <div className="space-y-4">
                      <input name="homeAddress" type="text" placeholder="Home Address" className={inputClass} required onChange={handleInputChange} />
                      <input name="distance" type="number" placeholder="Distance (KM)" className={inputClass} required onChange={handleInputChange} />
                      <select name="financialStatus" className={inputClass} onChange={handleInputChange}>
                        <option>No Scholarship</option><option>Indigent Fund</option><option>Full Scholarship</option>
                      </select>
                    </div>
                  </div>
                </div>

                {/* DISABILITY BOX */}
                <div className="space-y-4">
                   <div className="flex items-center justify-between p-8 bg-slate-900 rounded-[32px] text-white">
                      <div>
                        <p className="font-black text-sm uppercase tracking-tighter">Physical Disability / Medical Condition</p>
                        <p className="text-[10px] text-slate-400 font-bold uppercase tracking-widest mt-1">This grants immediate AI priority ranking</p>
                      </div>
                      <select 
                        name="hasDisability"
                        className="bg-white/10 border border-white/20 rounded-xl px-6 py-3 font-black text-sm outline-none"
                        onChange={handleInputChange}
                      >
                        <option className="text-slate-900">No</option>
                        <option className="text-slate-900">Yes</option>
                      </select>
                   </div>

                   <AnimatePresence>
                      {formData.hasDisability === 'Yes' && (
                        <motion.div initial={{ height: 0, opacity: 0 }} animate={{ height: 'auto', opacity: 1 }} exit={{ height: 0, opacity: 0 }}>
                           <textarea 
                              name="disabilityDetail"
                              placeholder="Please describe your condition (e.g. Mobility impairment - needs ground floor)..." 
                              className="w-full p-8 bg-red-50/30 border-2 border-red-100 rounded-[32px] outline-none focus:border-red-400 font-bold text-slate-700 min-h-[120px]"
                              onChange={handleInputChange}
                           />
                        </motion.div>
                      )}
                   </AnimatePresence>
                </div>

                <button type="submit" className="w-full py-6 bg-[#064e3b] text-white font-black rounded-[32px] hover:bg-black transition-all shadow-xl shadow-green-100 uppercase tracking-[4px] flex items-center justify-center gap-4 group">
                  Transmit Data to AI Engine <ChevronRight className="w-6 h-6 group-hover:translate-x-2 transition-transform" />
                </button>
              </form>
            </div>
          </motion.div>
        )}

        {/* VIEW 3: THE HIGH-END SUMMARY (WHAT YOU REQUESTED) */}
        {view === 'summary' && (
          <motion.div 
            key="summary" initial={{ opacity: 0, scale: 0.98 }} animate={{ opacity: 1, scale: 1 }}
            className="grid grid-cols-1 lg:grid-cols-3 gap-10"
          >
            {/* Left: Summary Receipt Card */}
            <div className="lg:col-span-2 bg-white rounded-[48px] border-2 border-green-50 p-12 shadow-sm relative overflow-hidden">
               <div className="absolute top-0 right-0 px-10 py-4 bg-green-600 text-white font-black text-[10px] uppercase tracking-widest rounded-bl-[32px] shadow-lg">Submission Verified</div>
               
               <header className="mb-12">
                 <div className="flex items-center gap-3 text-slate-300 uppercase font-black text-[10px] tracking-[4px] mb-2">
                    <FileText className="w-4 h-4" /> Application Archive
                 </div>
                 <h3 className="text-4xl font-black text-slate-900 tracking-tighter italic">Caleb Housing Record</h3>
               </header>
               
               <div className="grid grid-cols-2 gap-y-12 gap-x-16">
                  {[
                    { label: "Matriculation", val: formData.matricNo || '21/0452', icon: ShieldCheck },
                    { label: "Phone Contact", val: formData.phone || '08103425512', icon: Phone },
                    { label: "Verification Email", val: formData.email, icon: Mail },
                    { label: "Need Index", val: `${formData.distance || '450'} KM from Campus`, icon: MapPin },
                    { label: "Academic Tier", val: `${formData.department} (${formData.gpa || '3.85'} CGPA)`, icon: GraduationCap },
                    { label: "Priority Group", val: formData.hasDisability === 'Yes' ? 'High / Medical' : 'Standard', icon: Clock },
                  ].map((item, i) => (
                    <div key={i} className="space-y-3">
                      <div className="flex items-center gap-2 text-slate-400 uppercase text-[9px] font-black tracking-widest">
                        <item.icon className="w-3.5 h-3.5" /> {item.label}
                      </div>
                      <div className="font-mono text-base font-black text-slate-800 bg-[#f8fafc] p-5 rounded-[20px] border border-slate-100 shadow-inner">
                        {item.val}
                      </div>
                    </div>
                  ))}
               </div>
            </div>

            {/* Right: AI & Status Column */}
            <div className="space-y-6">
               {/* AI Processing Card */}
               <div className="bg-[#0f172a] rounded-[40px] p-10 text-white shadow-2xl relative overflow-hidden">
                  <div className="flex items-center gap-5 mb-10">
                     <div className="p-5 bg-indigo-600 rounded-3xl shadow-xl shadow-indigo-500/40 animate-pulse">
                        <Brain className="w-8 h-8 text-white" />
                     </div>
                     <div>
                       <h4 className="font-black text-xl tracking-tighter uppercase leading-none italic text-indigo-400">Neural Ranker</h4>
                       <p className="text-white/40 text-[9px] font-black uppercase tracking-widest mt-1">Status: Computing Priority...</p>
                     </div>
                  </div>
                  <div className="space-y-6">
                     <div className="flex justify-between text-[11px] font-black uppercase tracking-tighter">
                        <span className="text-indigo-300">Need Verification Index</span>
                        <span className="text-indigo-400">82.4%</span>
                     </div>
                     <div className="h-4 w-full bg-slate-800 rounded-full p-1 border border-slate-700">
                        <motion.div 
                          initial={{ width: 0 }} 
                          animate={{ width: '82%' }} 
                          transition={{ duration: 2.5, repeat: Infinity, repeatType: 'mirror' }} 
                          className="h-full bg-gradient-to-r from-indigo-500 via-cyan-400 to-blue-500 rounded-full shadow-[0_0_15px_rgba(99,102,241,0.6)]" 
                        />
                     </div>
                  </div>
                  <div className="mt-10 p-4 bg-white/5 rounded-2xl border border-white/5">
                     <p className="text-[10px] text-slate-400 font-medium leading-relaxed italic uppercase">Our AI is verifying your proximity to Ikorodu/Imota to prioritize out-of-state students.</p>
                  </div>
               </div>

               {/* Admin Pending Card */}
               <div className="bg-[#fffbeb] rounded-[40px] p-10 border border-amber-100 shadow-sm flex flex-col justify-center">
                  <div className="flex items-center gap-4 mb-6">
                     <div className="w-12 h-12 bg-amber-100 text-amber-600 rounded-full flex items-center justify-center animate-bounce">
                        <Clock className="w-6 h-6" />
                     </div>
                     <h4 className="font-black text-amber-900 uppercase tracking-tighter text-sm">Approval Queue</h4>
                  </div>
                  <p className="text-amber-800/60 text-[11px] font-bold leading-relaxed uppercase tracking-tight">
                    Your application is currently at position <span className="text-amber-900">#42</span> in the manual verification queue. The Caleb University housing team will finalize your assignment within 48 hours.
                  </p>
               </div>
            </div>
          </motion.div>
        )}

      </AnimatePresence>
    </div>
  );
}
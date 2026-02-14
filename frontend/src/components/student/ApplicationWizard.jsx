import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { GraduationCap, MapPin, FileHeart, DollarSign, ChevronRight, ChevronLeft, Check, Upload, Loader2 } from 'lucide-react';

const steps = [
  { id: 1, title: "Academic", icon: GraduationCap },
  { id: 2, title: "Logistics", icon: MapPin },
  { id: 3, title: "Medical", icon: FileHeart },
  { id: 4, title: "Financial", icon: DollarSign },
];

export default function ApplicationWizard({ onSubmit }) {
  const [currentStep, setCurrentStep] = useState(1);
  const [formData, setFormData] = useState({
    gpa: '', year_of_study: '1', department: 'engineering',
    home_address: '', distance_from_campus: '',
    has_medical_condition: false, financial_aid_status: 'none'
  });

  const updateField = (field, value) => setFormData(prev => ({ ...prev, [field]: value }));
  const nextStep = () => setCurrentStep(prev => Math.min(prev + 1, 4));
  const prevStep = () => setCurrentStep(prev => Math.max(prev - 1, 1));

  const inputClass = "w-full px-4 h-12 bg-slate-50 border border-slate-200 rounded-xl focus:ring-4 focus:ring-indigo-500/10 focus:border-indigo-500 outline-none transition-all font-medium";

  return (
    <div className="bg-white rounded-[32px] shadow-sm border border-slate-100 overflow-hidden">
      {/* Progress Header */}
      <div className="p-8 border-b border-slate-50 bg-slate-50/30">
        <div className="flex items-center justify-between max-w-2xl mx-auto">
          {steps.map((step, idx) => (
            <React.Fragment key={step.id}>
              <div className="flex flex-col items-center gap-2">
                <div className={`w-12 h-12 rounded-2xl flex items-center justify-center transition-all duration-500 ${currentStep >= step.id ? 'bg-indigo-600 text-white shadow-lg shadow-indigo-200' : 'bg-white text-slate-300 border border-slate-200'}`}>
                  {currentStep > step.id ? <Check className="w-6 h-6" /> : <step.icon className="w-5 h-5" />}
                </div>
                <span className={`text-[10px] font-black uppercase tracking-widest ${currentStep >= step.id ? 'text-indigo-600' : 'text-slate-400'}`}>{step.title}</span>
              </div>
              {idx < steps.length - 1 && <div className={`flex-1 h-1 mx-4 rounded-full ${currentStep > step.id ? 'bg-indigo-600' : 'bg-slate-200'}`} />}
            </React.Fragment>
          ))}
        </div>
      </div>

      <div className="p-10 min-h-[400px]">
        <AnimatePresence mode="wait">
          {currentStep === 1 && (
            <motion.div key="1" initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: -10 }} className="space-y-6">
              <h3 className="text-2xl font-black text-slate-900">Academic Standing</h3>
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-400 uppercase ml-1">Current GPA (4.0 Scale)</label>
                  <input type="number" step="0.01" placeholder="3.85" className={inputClass} value={formData.gpa} onChange={(e) => updateField('gpa', e.target.value)} />
                </div>
                <div className="space-y-2">
                  <label className="text-xs font-bold text-slate-400 uppercase ml-1">Level</label>
                  <select className={inputClass} value={formData.year_of_study} onChange={(e) => updateField('year_of_study', e.target.value)}>
                    <option value="1">100 Level</option>
                    <option value="2">200 Level</option>
                    <option value="3">300 Level</option>
                    <option value="4">400 Level</option>
                  </select>
                </div>
              </div>
            </motion.div>
          )}

          {currentStep === 2 && (
            <motion.div key="2" initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} className="space-y-6">
              <h3 className="text-2xl font-black text-slate-900">Logistics & Distance</h3>
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-400 uppercase ml-1">Permanent Home Address</label>
                <textarea className="w-full p-4 bg-slate-50 border border-slate-200 rounded-xl outline-none focus:border-indigo-500 min-h-[100px]" value={formData.home_address} onChange={(e) => updateField('home_address', e.target.value)} />
              </div>
              <div className="space-y-2">
                <label className="text-xs font-bold text-slate-400 uppercase ml-1">Distance from Campus (KM)</label>
                <input type="number" placeholder="e.g. 450" className={inputClass} value={formData.distance_from_campus} onChange={(e) => updateField('distance_from_campus', e.target.value)} />
              </div>
            </motion.div>
          )}

          {currentStep === 3 && (
            <motion.div key="3" initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} className="space-y-6 text-center py-10">
              <div className="w-20 h-20 bg-red-50 text-red-500 rounded-full flex items-center justify-center mx-auto mb-6">
                <FileHeart className="w-10 h-10" />
              </div>
              <h3 className="text-2xl font-black text-slate-900">Medical Requirements</h3>
              <p className="text-slate-500 mb-8">Do you have a documented medical condition that requires priority housing?</p>
              <div className="flex justify-center gap-4">
                <button onClick={() => updateField('has_medical_condition', true)} className={`px-8 py-3 rounded-2xl font-bold transition-all ${formData.has_medical_condition ? 'bg-red-500 text-white shadow-lg shadow-red-100' : 'bg-slate-100 text-slate-600'}`}>Yes, I do</button>
                <button onClick={() => updateField('has_medical_condition', false)} className={`px-8 py-3 rounded-2xl font-bold transition-all ${!formData.has_medical_condition ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-600'}`}>No, I don't</button>
              </div>
            </motion.div>
          )}

          {currentStep === 4 && (
            <motion.div key="4" initial={{ opacity: 0, x: 10 }} animate={{ opacity: 1, x: 0 }} className="space-y-6">
              <h3 className="text-2xl font-black text-slate-900">Financial Status</h3>
              <div className="grid gap-4">
                {['none', 'partial', 'full'].map((status) => (
                  <button key={status} onClick={() => updateField('financial_aid_status', status)} className={`w-full p-6 text-left rounded-2xl border-2 transition-all flex items-center justify-between ${formData.financial_aid_status === status ? 'border-indigo-600 bg-indigo-50/50' : 'border-slate-100 bg-white'}`}>
                    <span className="font-bold capitalize text-slate-700">{status} Scholarship / Aid</span>
                    {formData.financial_aid_status === status && <div className="w-6 h-6 bg-indigo-600 rounded-full flex items-center justify-center"><Check className="w-4 h-4 text-white" /></div>}
                  </button>
                ))}
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>

      {/* Footer Navigation */}
      <div className="p-8 border-t border-slate-50 flex justify-between bg-slate-50/30">
        <button onClick={prevStep} disabled={currentStep === 1} className="flex items-center gap-2 px-6 py-3 font-bold text-slate-400 hover:text-slate-600 disabled:opacity-0 transition-all">
          <ChevronLeft className="w-5 h-5" /> Back
        </button>
        {currentStep < 4 ? (
          <button onClick={nextStep} className="flex items-center gap-2 px-10 py-3 bg-indigo-600 text-white font-bold rounded-2xl shadow-lg shadow-indigo-100 hover:bg-indigo-700 transition-all">
            Continue <ChevronRight className="w-5 h-5" />
          </button>
        ) : (
          <button onClick={() => onSubmit(formData)} className="px-10 py-3 bg-slate-900 text-white font-bold rounded-2xl hover:bg-indigo-600 shadow-xl transition-all">
            Submit Application
          </button>
        )}
      </div>
    </div>
  );
}
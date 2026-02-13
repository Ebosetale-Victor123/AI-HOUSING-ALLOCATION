import React, { useState } from 'react';
import { ChevronDown, Target, Zap, ShieldCheck } from 'lucide-react';

export default function InfoSections() {
  const [openFaq, setOpenFaq] = useState(null);

  const faqs = [
    { q: "How is my priority score calculated?", a: "The AI considers your CGPA (40%), distance of home from campus (30%), and health/financial status (30%)." },
    { q: "Is the system 100% fair?", a: "Yes. By removing human intervention, the system eliminates favoritism and 'man-know-man' biases." }
  ];

  return (
    <section className="py-24 bg-slate-50">
      <div className="max-w-5xl mx-auto px-6">
        
        {/* Proposal Section */}
        <div className="mb-32">
          <h2 className="text-3xl font-bold text-slate-900 mb-8 text-center">Project Proposal</h2>
          <div className="grid md:grid-cols-3 gap-8">
            <div className="p-6 bg-white rounded-2xl shadow-sm border border-slate-100">
              <Target className="w-8 h-8 text-indigo-600 mb-4" />
              <h4 className="font-bold mb-2">The Objective</h4>
              <p className="text-sm text-slate-500">To automate housing allocation using predictive modeling to ensure transparency.</p>
            </div>
            <div className="p-6 bg-white rounded-2xl shadow-sm border border-slate-100">
              <Zap className="w-8 h-8 text-indigo-600 mb-4" />
              <h4 className="font-bold mb-2">The Solution</h4>
              <p className="text-sm text-slate-500">A real-time AI engine that ranks students based on merit and vulnerability factors.</p>
            </div>
            <div className="p-6 bg-white rounded-2xl shadow-sm border border-slate-100">
              <ShieldCheck className="w-8 h-8 text-indigo-600 mb-4" />
              <h4 className="font-bold mb-2">The Impact</h4>
              <p className="text-sm text-slate-500">Reducing administrative corruption and optimizing hostel occupancy rates by 25%.</p>
            </div>
          </div>
        </div>

        {/* FAQ Section */}
        <div>
          <h2 className="text-3xl font-bold text-slate-900 mb-12 text-center">Common Questions</h2>
          <div className="space-y-4">
            {faqs.map((faq, i) => (
              <div key={i} className="bg-white rounded-2xl border border-slate-200 overflow-hidden">
                <button 
                  onClick={() => setOpenFaq(openFaq === i ? null : i)}
                  className="w-full p-6 text-left flex justify-between items-center font-bold text-slate-800"
                >
                  {faq.q} <ChevronDown className={`transition-transform ${openFaq === i ? 'rotate-180' : ''}`} />
                </button>
                {openFaq === i && <div className="p-6 pt-0 text-slate-500 border-t border-slate-100 bg-slate-50/50">{faq.a}</div>}
              </div>
            ))}
          </div>
        </div>

      </div>
    </section>
  );
}
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Quote, ChevronDown, Star } from 'lucide-react';

const testimonials = [
  { name: "Sarah John", role: "300L Engineering", text: "Finally a system that doesn't require knowing anyone in the admin block. My allocation was instant!" },
  { name: "David Okon", role: "100L Law", text: "As a freshman, I was worried about housing. The AI score showed me exactly why I got my room." },
  { name: "Grace Amadi", role: "400L Medicine", text: "The transparent scoring is a game changer. No more favoritism, just pure merit and need-based allocation." }
];

const faqs = [
  { q: "How is the priority score calculated?", a: "Our AI uses a weighted formula: 40% Academic Performance (GPA), 30% Home Distance, and 30% Health/Financial Need." },
  { q: "What happens if I don't get a room?", a: "You will be placed on a transparent waiting list, and the AI will notify you if a spot opens up based on your rank." },
  { q: "Is my data secure?", a: "Absolutely. We use enterprise-grade encryption for all medical and financial documents uploaded." }
];

export default function Testimonials() {
  const [activeFaq, setActiveFaq] = useState(null);

  return (
    <section className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-6">
        
        {/* Testimonials */}
        <div className="text-center mb-16">
          <h2 className="text-4xl font-bold text-slate-900 mb-4">Student Testimonials</h2>
          <div className="flex justify-center gap-1 mb-12">
            {[1,2,3,4,5].map(i => <Star key={i} className="w-5 h-5 fill-amber-400 text-amber-400" />)}
          </div>
          <div className="grid md:grid-cols-3 gap-8">
            {testimonials.map((t, i) => (
              <div key={i} className="p-8 rounded-3xl bg-slate-50 border border-slate-100 hover:scale-105 transition-transform relative">
                <Quote className="w-10 h-10 text-indigo-100 absolute top-6 right-6" />
                <p className="text-slate-600 italic mb-6 relative z-10">"{t.text}"</p>
                <div className="font-bold text-slate-900">{t.name}</div>
                <div className="text-xs text-indigo-600 font-bold uppercase tracking-widest">{t.role}</div>
              </div>
            ))}
          </div>
        </div>

        {/* FAQ Section */}
        <div className="max-w-3xl mx-auto mt-32">
          <h2 className="text-3xl font-bold text-slate-900 mb-12 text-center">Frequently Asked Questions</h2>
          <div className="space-y-4">
            {faqs.map((faq, i) => (
              <div key={i} className="border border-slate-200 rounded-2xl overflow-hidden">
                <button 
                  onClick={() => setActiveFaq(activeFaq === i ? null : i)}
                  className="w-full p-6 text-left flex justify-between items-center bg-white hover:bg-slate-50 transition-colors font-bold text-slate-800"
                >
                  {faq.q}
                  <ChevronDown className={`w-5 h-5 transition-transform ${activeFaq === i ? 'rotate-180' : ''}`} />
                </button>
                <AnimatePresence>
                  {activeFaq === i && (
                    <motion.div 
                      initial={{ height: 0 }} animate={{ height: 'auto' }} exit={{ height: 0 }}
                      className="overflow-hidden bg-slate-50/50"
                    >
                      <div className="p-6 pt-0 text-slate-500 leading-relaxed border-t border-slate-100">
                        {faq.a}
                      </div>
                    </motion.div>
                  )}
                </AnimatePresence>
              </div>
            ))}
          </div>
        </div>

      </div>
    </section>
  );
}
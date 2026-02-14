import React from 'react';
import { motion } from 'framer-motion';

export default function Support() {
  const supportItems = [
    { title: "FAQs", desc: "Find answers to common questions" },
    { title: "Email Support", desc: "housing@university.edu" },
    { title: "Phone Support", desc: "+1 (555) 123-4567" },
    { title: "Office Hours", desc: "Mon-Fri, 9AM-5PM" }
  ];

  return (
    <motion.div 
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-6xl mx-auto"
    >
      <div className="bg-white rounded-[32px] border border-slate-100 p-10 shadow-sm">
        <h2 className="text-2xl font-bold text-slate-900 mb-10">Need Help?</h2>
        <div className="flex flex-col gap-4">
          {supportItems.map((item, i) => (
            <motion.div 
              key={i}
              whileHover={{ x: 4 }}
              className="p-8 bg-[#f8fafc] rounded-2xl border border-transparent hover:border-slate-200 transition-all cursor-pointer group"
            >
              <h4 className="font-bold text-slate-800 text-lg mb-1 group-hover:text-indigo-600 transition-colors">
                {item.title}
              </h4>
              <p className="text-slate-500 font-medium">{item.desc}</p>
            </motion.div>
          ))}
        </div>
      </div>
    </motion.div>
  );
}
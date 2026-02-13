import React from 'react';
import { Building2, Mail, Phone, MapPin, Twitter, Linkedin, Facebook, Github } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="bg-[#020617] text-slate-400 py-20 border-t border-slate-800/50">
      <div className="max-w-7xl mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-16 mb-16">
          
          {/* Brand & About */}
          <div className="md:col-span-2">
            <div className="flex items-center gap-3 mb-6 group cursor-pointer">
              <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-indigo-500/20 group-hover:scale-110 transition-transform">
                <Building2 className="w-6 h-6 text-white" />
              </div>
              <span className="text-2xl font-black text-white tracking-tight">UniHousing <span className="text-indigo-500">AI</span></span>
            </div>
            <p className="text-slate-400 leading-relaxed mb-8 max-w-sm text-lg">
              We're building the future of campus living. Our AI-driven approach ensures every student finds their home away from home, fairly and transparently.
            </p>
            <div className="flex gap-4">
              {[
                { icon: Twitter, href: "#" },
                { icon: Linkedin, href: "#" },
                { icon: Facebook, href: "#" },
                { icon: Github, href: "#" }
              ].map((social, i) => (
                <a
                  key={i}
                  href={social.href}
                  className="w-11 h-11 rounded-xl bg-slate-800/50 border border-slate-700/50 flex items-center justify-center text-slate-400 hover:text-white hover:bg-indigo-600 hover:border-indigo-500 transition-all duration-300"
                >
                  <social.icon className="w-5 h-5" />
                </a>
              ))}
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-white font-bold text-lg mb-6">Explore</h3>
            <ul className="space-y-4">
              {['About Project', 'How It Works', 'Hostel Gallery', 'Staff Portal'].map((link) => (
                <li key={link}>
                  <a href="#" className="group flex items-center gap-2 hover:text-indigo-400 transition-colors">
                    <span className="w-1.5 h-1.5 rounded-full bg-slate-700 group-hover:bg-indigo-400 transition-colors" />
                    {link}
                  </a>
                </li>
              ))}
            </ul>
          </div>

          {/* Contact Details */}
          <div>
            <h3 className="text-white font-bold text-lg mb-6">Get in Touch</h3>
            <ul className="space-y-5">
              <li className="flex items-center gap-4 group">
                <div className="w-10 h-10 rounded-lg bg-slate-800/50 flex items-center justify-center border border-slate-700/50 group-hover:border-indigo-500/50 transition-colors">
                  <Mail className="w-4 h-4 text-indigo-400" />
                </div>
                <span className="text-sm">support@unihousing.ai</span>
              </li>
              <li className="flex items-center gap-4 group">
                <div className="w-10 h-10 rounded-lg bg-slate-800/50 flex items-center justify-center border border-slate-700/50 group-hover:border-indigo-500/50 transition-colors">
                  <Phone className="w-4 h-4 text-indigo-400" />
                </div>
                <span className="text-sm">+234 (0) 800-HOUSING</span>
              </li>
              <li className="flex items-start gap-4 group">
                <div className="w-10 h-10 rounded-lg bg-slate-800/50 flex items-center justify-center border border-slate-700/50 group-hover:border-indigo-500/50 transition-colors">
                  <MapPin className="w-4 h-4 text-indigo-400" />
                </div>
                <span className="text-sm leading-relaxed">Faculty of Engineering,<br />University Campus</span>
              </li>
            </ul>
          </div>
        </div>

        {/* Bottom Bar */}
        <div className="pt-10 border-t border-slate-800/50 flex flex-col md:flex-row items-center justify-between gap-6">
          <p className="text-sm font-medium">
            © 2026 <span className="text-white">UniHousing AI</span>. Built for Excellence.
          </p>
          <div className="flex gap-8 text-xs font-bold uppercase tracking-widest">
            <a href="#" className="hover:text-white transition-colors">Privacy</a>
            <a href="#" className="hover:text-white transition-colors">Terms</a>
            <a href="#" className="hover:text-white transition-colors">Security</a>
          </div>
        </div>
      </div>
    </footer>
  );
}
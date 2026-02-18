import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Users, Wifi, Car, Coffee, Dumbbell, BookOpen, MapPin, Search, Filter } from 'lucide-react';

const mockHostels = [
  { id: 1, name: "Grace Hall", gender: "Female", roomType: "Double", capacity: 200, occupied: 187, fee: 450000, image: "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800&q=80", amenities: ["WiFi", "Parking", "Gym"] },
  { id: 2, name: "Faith Tower", gender: "Female", roomType: "Single", capacity: 150, occupied: 142, fee: 580000, image: "https://images.unsplash.com/photo-1574362848149-11496d93a7c7?w=800&q=80", amenities: ["WiFi", "Cafeteria", "Lounge"] },
  { id: 3, name: "Covenant Block", gender: "Male", roomType: "Triple", capacity: 180, occupied: 165, fee: 380000, image: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&q=80", amenities: ["WiFi", "Sports", "Laundry"] },
  { id: 4, name: "Victory Lodge", gender: "Male", roomType: "Double", capacity: 220, occupied: 198, fee: 420000, image: "https://images.unsplash.com/photo-1502672260266-1c1ef2d93688?w=800&q=80", amenities: ["WiFi", "Gym", "Cafeteria"] },
  { id: 5, name: "Mercy Residence", gender: "Female", roomType: "Quad", capacity: 240, occupied: 220, fee: 320000, image: "https://images.unsplash.com/photo-1556912172-45b7abe8b7e1?w=800&q=80", amenities: ["WiFi", "Kitchen", "Lounge"] },
  { id: 6, name: "Hope House", gender: "Male", roomType: "Single", capacity: 120, occupied: 115, fee: 550000, image: "https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=800&q=80", amenities: ["WiFi", "Gym", "AC"] },
];

const icons = { WiFi: Wifi, Parking: Car, Cafeteria: Coffee, Gym: Dumbbell, Lounge: BookOpen };

export default function HostelGallery() {
  const [filter, setFilter] = useState('All');

  const filteredHostels = filter === 'All' 
    ? mockHostels 
    : mockHostels.filter(h => h.gender === filter);

  return (
    <div className="space-y-10 max-w-7xl mx-auto">
      {/* 1. Header & Filter System */}
      <div className="flex flex-col md:flex-row justify-between items-end gap-6">
        <div>
           <div className="flex items-center gap-2 text-green-600 font-black text-[10px] uppercase tracking-[4px] mb-2">
              <MapPin className="w-3 h-3" /> Imota, Lagos State
           </div>
           <h2 className="text-4xl font-black text-slate-900 tracking-tighter">Campus Residences</h2>
           <p className="text-slate-400 font-bold uppercase text-[9px] tracking-widest mt-1">Institutional Housing Catalog 2026</p>
        </div>

        <div className="flex bg-white p-1.5 rounded-2xl border border-slate-100 shadow-sm">
           {['All', 'Male', 'Female'].map((type) => (
             <button
               key={type}
               onClick={() => setFilter(type)}
               className={`px-6 py-2.5 rounded-xl text-xs font-black uppercase tracking-widest transition-all ${filter === type ? 'bg-[#064e3b] text-white shadow-lg shadow-green-100' : 'text-slate-400 hover:text-slate-600'}`}
             >
               {type}
             </button>
           ))}
        </div>
      </div>

      {/* 2. Hostel Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
        <AnimatePresence mode="popLayout">
          {filteredHostels.map((hostel, i) => (
            <motion.div
              layout
              key={hostel.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, scale: 0.9 }}
              transition={{ delay: i * 0.05 }}
              className="group bg-white rounded-[40px] border border-slate-100 overflow-hidden hover:shadow-2xl hover:shadow-green-100 transition-all duration-500"
            >
              {/* Image Container */}
              <div className="relative h-64 overflow-hidden">
                <img 
                  src={hostel.image} 
                  alt={hostel.name} 
                  className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" 
                />
                <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/20 to-transparent" />
                
                {/* Custom Badges */}
                <div className="absolute top-6 left-6 px-4 py-2 bg-white/90 backdrop-blur-md rounded-2xl shadow-xl">
                  <span className={`text-[10px] font-black uppercase tracking-widest ${hostel.gender === 'Male' ? 'text-blue-600' : 'text-pink-600'}`}>
                    {hostel.gender} WING
                  </span>
                </div>

                <div className="absolute bottom-6 left-6 right-6">
                  <h3 className="text-2xl font-black text-white italic tracking-tighter">{hostel.name}</h3>
                  <div className="flex items-center gap-2 mt-1">
                    <div className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                    <span className="text-[10px] text-white/70 font-black uppercase tracking-widest">Available for Booking</span>
                  </div>
                </div>
              </div>

              {/* Data Content */}
              <div className="p-8">
                <div className="flex justify-between items-start mb-8">
                  <div className="space-y-1">
                    <p className="text-[10px] font-black text-slate-400 uppercase tracking-widest">Starting From</p>
                    <div className="text-3xl font-black text-slate-900 tracking-tighter">
                      ₦{hostel.fee.toLocaleString()}
                      <span className="text-slate-300 text-xs font-bold uppercase tracking-widest ml-1">/yr</span>
                    </div>
                  </div>
                  <div className="bg-slate-50 p-3 rounded-2xl border border-slate-100">
                    <Users className="w-5 h-5 text-slate-400" />
                  </div>
                </div>

                {/* Progress Bar (Occupancy) */}
                <div className="space-y-3 mb-8">
                  <div className="flex justify-between text-[10px] font-black uppercase tracking-widest text-slate-500 px-1">
                    <span>Occupancy Index</span>
                    <span className="text-green-600">{hostel.occupied}/{hostel.capacity}</span>
                  </div>
                  <div className="h-2 w-full bg-slate-100 rounded-full overflow-hidden p-0.5 border border-slate-50">
                    <motion.div 
                      initial={{ width: 0 }}
                      animate={{ width: `${(hostel.occupied / hostel.capacity) * 100}%` }}
                      className="h-full bg-[#064e3b] rounded-full shadow-[0_0_10px_rgba(6,78,59,0.3)]"
                    />
                  </div>
                </div>

                {/* Footer Actions */}
                <div className="flex items-center justify-between gap-4">
                  <div className="flex gap-2">
                    {hostel.amenities.map(a => {
                      const Icon = icons[a] || Wifi;
                      return (
                        <div key={a} className="p-2.5 bg-slate-50 rounded-xl border border-slate-100 text-slate-400 hover:text-green-600 hover:bg-green-50 transition-all cursor-help">
                          <Icon className="w-4 h-4" />
                        </div>
                      )
                    })}
                  </div>
                  <button className="flex-1 py-3.5 bg-slate-900 text-white font-black text-[10px] uppercase tracking-[2px] rounded-2xl hover:bg-[#064e3b] hover:-translate-y-1 transition-all shadow-xl shadow-slate-100">
                    View Specs
                  </button>
                </div>
              </div>
            </motion.div>
          ))}
        </AnimatePresence>
      </div>

      {/* 3. Empty State Notification */}
      {filteredHostels.length === 0 && (
        <div className="py-20 text-center bg-white rounded-[40px] border-2 border-dashed border-slate-100">
           <Search className="w-12 h-12 text-slate-200 mx-auto mb-4" />
           <h3 className="text-xl font-bold text-slate-400 uppercase tracking-widest">No Hostels Found</h3>
        </div>
      )}
    </div>
  );
}
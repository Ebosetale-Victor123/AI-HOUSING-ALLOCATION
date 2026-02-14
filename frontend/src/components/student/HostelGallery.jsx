import React from 'react';
import { motion } from 'framer-motion';
import { Wifi, Car, Coffee, Dumbbell, BookOpen, MapPin } from 'lucide-react';

const mockHostels = [
  { id: 1, name: "Aurora Hall", type: "Female", roomType: "Double", capacity: 200, occupied: 187, fee: 850, image: "https://images.unsplash.com/photo-1555854877-bab0e564b8d5?w=800&q=80", amenities: ["WiFi", "Parking", "Gym"] },
  { id: 2, name: "Orion Tower", type: "Male", roomType: "Single", capacity: 250, occupied: 231, fee: 1100, image: "https://images.unsplash.com/photo-1574362848149-11496d93a7c7?w=800&q=80", amenities: ["WiFi", "Cafeteria", "Lounge"] },
  { id: 3, name: "Nova Residence", type: "Co-ed", roomType: "Triple", capacity: 180, occupied: 165, fee: 650, image: "https://images.unsplash.com/photo-1522708323590-d24dbb6b0267?w=800&q=80", amenities: ["WiFi", "Kitchen", "Laundry"] }
];

const icons = { WiFi: Wifi, Parking: Car, Cafeteria: Coffee, Gym: Dumbbell, Lounge: BookOpen };

export default function HostelGallery() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
      {mockHostels.map((hostel, i) => (
        <motion.div key={hostel.id} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: i * 0.1 }} className="group bg-white rounded-[32px] border border-slate-100 overflow-hidden hover:shadow-2xl hover:shadow-indigo-100/50 transition-all duration-500">
          <div className="relative h-64 overflow-hidden">
            <img src={hostel.image} alt={hostel.name} className="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700" />
            <div className="absolute top-4 left-4 px-4 py-1.5 bg-white/90 backdrop-blur-md rounded-full text-[10px] font-black uppercase tracking-widest text-indigo-600 shadow-sm">{hostel.type}</div>
            <div className="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-slate-900/80 to-transparent text-white">
              <h3 className="text-2xl font-black">{hostel.name}</h3>
              <div className="flex items-center gap-1 text-xs opacity-80 font-bold uppercase tracking-tighter mt-1"><MapPin className="w-3 h-3" /> University East Campus</div>
            </div>
          </div>
          <div className="p-8">
            <div className="flex justify-between items-end mb-6">
              <div>
                <span className="text-3xl font-black text-slate-900">${hostel.fee}</span>
                <span className="text-slate-400 font-bold text-sm ml-1">/session</span>
              </div>
              <div className="text-right">
                <div className="text-xs font-bold text-slate-400 uppercase tracking-widest mb-1">Available</div>
                <div className="text-xl font-black text-indigo-600">{hostel.capacity - hostel.occupied} <span className="text-slate-300 font-medium">Beds</span></div>
              </div>
            </div>
            <div className="h-1.5 w-full bg-slate-100 rounded-full mb-8 overflow-hidden">
               <motion.div initial={{ width: 0 }} animate={{ width: `${(hostel.occupied / hostel.capacity) * 100}%` }} className="h-full bg-indigo-600" />
            </div>
            <div className="flex items-center justify-between">
               <div className="flex gap-3">
                  {hostel.amenities.map(a => {
                    const Icon = icons[a] || Wifi;
                    return <Icon key={a} className="w-5 h-5 text-slate-300 hover:text-indigo-500 transition-colors" />
                  })}
               </div>
               <button className="px-6 py-2.5 bg-slate-900 text-white text-xs font-bold rounded-xl hover:bg-indigo-600 transition-all">View Details</button>
            </div>
          </div>
        </motion.div>
      ))}
    </div>
  );
}
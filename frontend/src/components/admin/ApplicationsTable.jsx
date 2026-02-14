import React from 'react';
import { Search, Filter, MoreHorizontal, ChevronLeft, ChevronRight } from 'lucide-react';

const mock = [
  { name: "Emma Wilson", email: "emma.w@uni.edu", dept: "Engineering", gpa: 3.85, dist: "245 km", score: 87, status: "Allocated", sColor: "bg-emerald-100 text-emerald-600", bar: "bg-emerald-500" },
  { name: "James Chen", email: "j.chen@uni.edu", dept: "Medicine", gpa: 3.92, dist: "120 km", score: 92, status: "Allocated", sColor: "bg-emerald-100 text-emerald-600", bar: "bg-emerald-500" },
  { name: "Sarah Miller", email: "s.miller@uni.edu", dept: "Business", gpa: 3.45, dist: "380 km", score: 72, status: "AI Scoring", sColor: "bg-purple-100 text-purple-600", bar: "bg-cyan-500" },
  { name: "Michael Brown", email: "m.brown@uni.edu", dept: "Arts", gpa: 3.67, dist: "95 km", score: 68, status: "Pending", sColor: "bg-amber-100 text-amber-600", bar: "bg-cyan-500" },
  { name: "Lisa Anderson", email: "l.anderson@uni.edu", dept: "Science", gpa: 3.78, dist: "290 km", score: 89, status: "Allocated", sColor: "bg-emerald-100 text-emerald-600", bar: "bg-emerald-500" },
  { name: "David Kim", email: "d.kim@uni.edu", dept: "Law", gpa: 3.55, dist: "150 km", score: 58, status: "Rejected", sColor: "bg-red-100 text-red-500", bar: "bg-amber-500" },
];

export default function ApplicationsTable() {
  return (
    <div className="bg-white rounded-2xl border border-slate-100 shadow-sm overflow-hidden">
      
      {/* Search and Filter Row */}
      <div className="p-8 flex justify-between gap-4">
        <div className="relative flex-1 max-w-sm">
          <Search className="absolute left-4 top-1/2 -translate-y-1/2 w-4 h-4 text-slate-300" />
          <input 
            type="text" 
            placeholder="Search by name or email..." 
            className="w-full pl-12 pr-4 h-12 bg-white border border-slate-200 rounded-2xl text-sm outline-none focus:border-indigo-500 transition-all" 
          />
        </div>
        <button className="flex items-center gap-2 px-6 h-12 bg-white border border-slate-200 rounded-2xl text-sm text-slate-500 font-medium hover:bg-slate-50">
          <Filter className="w-4 h-4 text-slate-300" /> All Status
        </button>
      </div>

      {/* The Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-left">
          <thead className="text-[11px] text-slate-400 uppercase font-bold bg-slate-50/30 border-y border-slate-50">
            <tr>
              <th className="px-8 py-5">Student</th>
              <th className="px-8 py-5">Department</th>
              <th className="px-8 py-5">GPA</th>
              <th className="px-8 py-5">Distance</th>
              <th className="px-8 py-5">AI Score</th>
              <th className="px-8 py-5">Status</th>
              <th className="px-8 py-5">Actions</th>
            </tr>
          </thead>
          <tbody className="text-sm">
            {mock.map((app, i) => (
              <tr key={i} className="border-b border-slate-50 hover:bg-slate-50/50 transition-colors">
                <td className="px-8 py-6">
                  <div className="font-bold text-slate-900">{app.name}</div>
                  <div className="text-[11px] text-slate-400 font-medium">{app.email}</div>
                </td>
                <td className="px-8 py-6 text-slate-500 font-medium">{app.dept}</td>
                <td className="px-8 py-6 font-bold text-emerald-500">{app.gpa}</td>
                <td className="px-8 py-6 text-slate-500 font-medium">{app.dist}</td>
                <td className="px-8 py-6">
                  <div className="flex items-center gap-3">
                    <div className="w-20 h-2 bg-slate-100 rounded-full overflow-hidden">
                      <div 
                        className={`h-full ${app.bar} rounded-full`} 
                        style={{width: `${app.score}%`}}
                      ></div>
                    </div>
                    <span className="font-bold text-slate-700 w-6">{app.score}</span>
                  </div>
                </td>
                <td className="px-8 py-6">
                  <span className={`px-4 py-1.5 rounded-lg text-[10px] font-bold uppercase tracking-wider ${app.sColor}`}>
                    {app.status}
                  </span>
                </td>
                <td className="px-8 py-6"><MoreHorizontal className="w-5 h-5 text-slate-300 cursor-pointer hover:text-slate-600" /></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination Footer */}
      <div className="p-6 flex justify-between items-center text-xs text-slate-400 font-bold uppercase tracking-widest">
        <span>Showing 1 to 6 of 6 results</span>
        <div className="flex gap-2">
          <button className="p-2 border border-slate-200 rounded-xl hover:bg-slate-50"><ChevronLeft className="w-4 h-4" /></button>
          <button className="p-2 border border-slate-200 rounded-xl hover:bg-slate-50"><ChevronRight className="w-4 h-4" /></button>
        </div>
      </div>
    </div>
  );
}
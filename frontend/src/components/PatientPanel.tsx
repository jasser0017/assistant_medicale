import { LineChart, Line, ResponsiveContainer } from "recharts";
import { HiHeart } from "react-icons/hi";

const data = [
  { d: "Mon", v: 70 },
  { d: "Tue", v: 68 },
  { d: "Wed", v: 80 },
  { d: "Thu", v: 75 },
  { d: "Fri", v: 78 },
  { d: "Sat", v: 72 },
  { d: "Sun", v: 74 },
];

export default function PatientPanel() {
  return (
    <div className="w-96 shrink-0 rounded-4xl bg-white/10 p-6 backdrop-blur-xl border border-white/20 shadow-[0_4px_30px_rgba(0,0,0,0.1)] text-white">
      <div className="mb-4 p-4 bg-white/5 rounded-xl">
        <p className="text-sm mb-2">Anna • 28 ans</p>
        <p className="text-sm">
          <span className="opacity-70">Blood type:</span> A+
        </p>
      </div>

      <div className="bg-white/5 p-4 rounded-xl mb-4">
        <h4 className="text-sm font-medium mb-2">Weekly activity</h4>
        <ResponsiveContainer width="100%" height={80}>
          <LineChart data={data}>
            <Line
              type="monotone"
              dataKey="v"
              stroke="#3B82F6"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>

      <div className="bg-white/5 p-4 rounded-xl">
        <div className="grid grid-cols-3 gap-4 text-sm mb-4">
          <div className="space-y-1">
            <p className="opacity-70">Score</p>
            <p>No</p>
          </div>
          <div className="space-y-1">
            <p className="opacity-70">Model</p>
            <p>This</p>
          </div>
          <div className="space-y-1">
            <p className="opacity-70">Date</p>
            <p>8.452</p>
          </div>
        </div>
        
        <ul className="space-y-3">
          <li className="flex items-center gap-2">
            <HiHeart className="w-4 h-4 text-red-400" />
            75 bpm
          </li>
          <li className="flex items-center gap-2">
            <span>🩸</span>
            120/80 mmHg
          </li>
        </ul>
      </div>
    </div>
  );
}
import { motion } from 'motion/react';
import { Card } from './ui/card';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
import { TrendingUp } from 'lucide-react';

interface DailyData {
  date: string;
  count: number;
}

interface HistoricalChartProps {
  data: DailyData[];
}

export function HistoricalChart({ data }: HistoricalChartProps) {
  const totalFrowns = data.reduce((sum, day) => sum + day.count, 0);
  
  return (
    <Card className="p-5 bg-white/90 backdrop-blur-sm border border-indigo-200 shadow-xl">
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <TrendingUp className="w-4 h-4 text-indigo-600" />
          <h3 className="text-purple-900">Last 7 Days 📊</h3>
        </div>
        <span className="text-xs text-indigo-600 bg-indigo-50 px-2 py-1 rounded-full border border-indigo-200">{totalFrowns} total</span>
      </div>
      
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
      >
        <ResponsiveContainer width="100%" height={180}>
          <AreaChart data={data} margin={{ top: 10, right: 0, left: -20, bottom: 0 }}>
            <defs>
              <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#8b5cf6" stopOpacity={0.4}/>
                <stop offset="95%" stopColor="#6366f1" stopOpacity={0.05}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e7ff" />
            <XAxis 
              dataKey="date" 
              stroke="#6366f1"
              style={{ fontSize: '11px' }}
              tickLine={false}
            />
            <YAxis 
              stroke="#6366f1"
              style={{ fontSize: '11px' }}
              tickLine={false}
              allowDecimals={false}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(255, 255, 255, 0.95)',
                border: '1px solid #c7d2fe',
                borderRadius: '8px',
                fontSize: '12px',
                padding: '8px 12px',
              }}
              labelStyle={{ color: '#4338ca', fontWeight: 600 }}
              itemStyle={{ color: '#6366f1' }}
            />
            <Area
              type="monotone"
              dataKey="count"
              stroke="#6366f1"
              strokeWidth={2}
              fillOpacity={1}
              fill="url(#colorCount)"
              name="Frowns"
            />
          </AreaChart>
        </ResponsiveContainer>
      </motion.div>
    </Card>
  );
}

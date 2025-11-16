import { motion } from 'motion/react';

interface StatsCardProps {
  label: string;
  value: number;
  color: 'blue' | 'indigo' | 'purple' | 'pink';
  delay?: number;
}

const colorClasses = {
  blue: 'bg-gradient-to-br from-blue-50 to-cyan-50 text-blue-700 border-blue-200',
  indigo: 'bg-gradient-to-br from-indigo-50 to-purple-50 text-indigo-700 border-indigo-200',
  purple: 'bg-gradient-to-br from-purple-50 to-pink-50 text-purple-700 border-purple-200',
  pink: 'bg-gradient-to-br from-pink-50 to-rose-50 text-pink-700 border-pink-200',
};

export function StatsCard({ label, value, color, delay = 0 }: StatsCardProps) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay }}
      className={`p-4 rounded-lg border ${colorClasses[color]} transition-all hover:shadow-md hover:scale-105`}
    >
      <div className="flex items-center justify-between">
        <span className="text-xs">{label}</span>
        <motion.span
          key={value}
          initial={{ scale: 1.5, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="text-2xl"
        >
          {value}
        </motion.span>
      </div>
    </motion.div>
  );
}

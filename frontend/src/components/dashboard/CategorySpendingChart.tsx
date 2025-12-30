import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { CategorySpending } from '../../models/DashboardData';

interface CategorySpendingChartProps {
  data: CategorySpending[];
}

const COLORS = ['#FF6B6B', '#4A90E2', '#50C878', '#FFD93D', '#A78BFA', '#F472B6', '#FB923C', '#34D399', '#60A5FA', '#C084FC'];

export const CategorySpendingChart: React.FC<CategorySpendingChartProps> = ({ data }) => {
  const chartData = data.map(item => ({
    category: item.category,
    amount: item.total_amount
  }));

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Category-wise Spending</h3>
      <ResponsiveContainer width="100%" height={350}>
        <BarChart data={chartData} margin={{ top: 20, right: 30, left: 20, bottom: 60 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
          <XAxis 
            dataKey="category" 
            angle={-45} 
            textAnchor="end" 
            height={100}
            tick={{ fontSize: 12 }}
          />
          <YAxis tick={{ fontSize: 12 }} />
          <Tooltip 
            formatter={(value: number) => `₹${value.toFixed(2)}`}
            contentStyle={{ borderRadius: '8px', border: '1px solid #ddd' }}
          />
          <Bar dataKey="amount" radius={[8, 8, 0, 0]}>
            {chartData.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    backgroundColor: '#fff',
    padding: '25px',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    marginBottom: '30px'
  },
  title: {
    fontSize: '18px',
    fontWeight: 'bold',
    marginBottom: '20px',
    color: '#333'
  }
};

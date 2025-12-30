import React from 'react';
import { CategorySpending } from '../../models/DashboardData';

interface TopCategoriesCardProps {
  data: CategorySpending[];
}

export const TopCategoriesCard: React.FC<TopCategoriesCardProps> = ({ data }) => {
  const top5 = data.slice(0, 5);

  return (
    <div style={styles.container}>
      <h3 style={styles.title}>Top 5 Categories</h3>
      <div style={styles.list}>
        {top5.map((item, index) => (
          <div key={item.category} style={styles.item}>
            <div style={styles.rank}>{index + 1}</div>
            <div style={styles.details}>
              <div style={styles.category}>{item.category}</div>
              <div style={styles.count}>{item.transaction_count} transactions</div>
            </div>
            <div style={styles.amount}>₹{item.total_amount.toFixed(2)}</div>
          </div>
        ))}
      </div>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    backgroundColor: '#fff',
    padding: '20px',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    height: '100%'
  },
  title: {
    fontSize: '16px',
    fontWeight: 'bold',
    marginBottom: '15px',
    color: '#333'
  },
  list: {
    display: 'flex',
    flexDirection: 'column',
    gap: '12px'
  },
  item: {
    display: 'flex',
    alignItems: 'center',
    padding: '12px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px',
    transition: 'background-color 0.2s'
  },
  rank: {
    width: '30px',
    height: '30px',
    borderRadius: '50%',
    backgroundColor: '#4A90E2',
    color: '#fff',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    fontWeight: 'bold',
    fontSize: '14px',
    marginRight: '12px'
  },
  details: {
    flex: 1
  },
  category: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#333',
    marginBottom: '2px'
  },
  count: {
    fontSize: '12px',
    color: '#666'
  },
  amount: {
    fontSize: '14px',
    fontWeight: 'bold',
    color: '#4A90E2'
  }
};

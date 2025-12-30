import React from 'react';

interface Props {
  category: string;
}

const CATEGORY_COLORS: Record<string, string> = {
  Food: '#FF6B6B',
  Shopping: '#4ECDC4',
  Travel: '#45B7D1',
  Bills: '#FFA07A',
  Entertainment: '#98D8C8',
  Subscriptions: '#F7DC6F',
  Health: '#BB8FCE',
  Groceries: '#85C1E2',
  Education: '#F8B739',
  Fuel: '#52B788',
  ATM: '#95A5A6',
  Salary: '#27AE60',
  Interest: '#3498DB',
  Refund: '#E74C3C',
  Internal_Transfer: '#9B59B6',
  Person: '#E67E22',
  Other: '#7F8C8D'
};

export const CategoryBadge: React.FC<Props> = ({ category }) => {
  const color = CATEGORY_COLORS[category] || '#7F8C8D';

  return (
    <span style={{
      display: 'inline-block',
      padding: '4px 12px',
      backgroundColor: color,
      color: '#fff',
      borderRadius: '12px',
      fontSize: '12px',
      fontWeight: '500'
    }}>
      {category}
    </span>
  );
};

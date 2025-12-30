import React from 'react';
import { CATEGORIES } from '../../models/CategorizedTransaction';

interface Props {
  selectedCategory: string;
  onCategoryChange: (category: string) => void;
}

export const CategoryFilter: React.FC<Props> = ({ selectedCategory, onCategoryChange }) => {
  return (
    <div style={{ marginBottom: '16px' }}>
      <label style={{ fontSize: '14px', fontWeight: '500', marginRight: '8px' }}>
        Filter by Category:
      </label>
      <select
        value={selectedCategory}
        onChange={(e) => onCategoryChange(e.target.value)}
        style={{
          padding: '8px 12px',
          fontSize: '14px',
          border: '1px solid #ddd',
          borderRadius: '4px',
          backgroundColor: '#fff',
          cursor: 'pointer'
        }}
      >
        <option value="">All Categories</option>
        {CATEGORIES.map((cat) => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </select>
    </div>
  );
};

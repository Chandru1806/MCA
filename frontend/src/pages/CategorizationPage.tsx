import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { categorizationService } from '../services/categorizationService';
import { CategorizedTransaction, CATEGORIES } from '../models/CategorizedTransaction';
import { CategoryBadge } from '../components/categorization/CategoryBadge';
import { ConfidenceIndicator } from '../components/categorization/ConfidenceIndicator';
import { CategoryFilter } from '../components/categorization/CategoryFilter';

export const CategorizationPage: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const statementId = (location.state as any)?.statementId;

  const [transactions, setTransactions] = useState<CategorizedTransaction[]>([]);
  const [filteredTransactions, setFilteredTransactions] = useState<CategorizedTransaction[]>([]);
  const [selectedCategory, setSelectedCategory] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editingId, setEditingId] = useState<string | null>(null);

  useEffect(() => {
    if (!statementId) {
      navigate('/dashboard');
      return;
    }
    loadTransactions();
  }, [statementId]);

  useEffect(() => {
    if (selectedCategory) {
      setFilteredTransactions(transactions.filter(t => t.category === selectedCategory));
    } else {
      setFilteredTransactions(transactions);
    }
  }, [selectedCategory, transactions]);

  const loadTransactions = async () => {
    try {
      setLoading(true);
      const data = await categorizationService.getCategorizedTransactions(statementId);
      setTransactions(data);
      setFilteredTransactions(data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load transactions');
    } finally {
      setLoading(false);
    }
  };

  const handleCategoryUpdate = async (transactionId: string, newCategory: string) => {
    try {
      await categorizationService.updateCategory(transactionId, newCategory);
      setTransactions(prev => prev.map(t => 
        t.transaction_id === transactionId 
          ? { ...t, category: newCategory, method: 'MANUAL', confidence: 1.0 }
          : t
      ));
      setEditingId(null);
    } catch (err: any) {
      alert(err.response?.data?.error || 'Failed to update category');
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '400px' }}>
        <div style={{
          width: '50px',
          height: '50px',
          border: '5px solid #f3f3f3',
          borderTop: '5px solid #50C878',
          borderRadius: '50%',
          animation: 'spin 1s linear infinite'
        }} />
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '40px', textAlign: 'center' }}>
        <p style={{ color: '#d32f2f', fontSize: '16px' }}>{error}</p>
        <button
          onClick={() => navigate('/dashboard')}
          style={{
            marginTop: '16px',
            padding: '10px 20px',
            backgroundColor: '#50C878',
            color: '#fff',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Back to Dashboard
        </button>
      </div>
    );
  }

  return (
    <div style={{ padding: '24px', maxWidth: '1400px', margin: '0 auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
        <h1 style={{ margin: 0, fontSize: '24px', fontWeight: 'bold' }}>Categorized Transactions</h1>
        <button
          onClick={() => navigate('/dashboard')}
          style={{
            padding: '8px 16px',
            backgroundColor: '#fff',
            border: '1px solid #ddd',
            borderRadius: '4px',
            cursor: 'pointer',
            fontSize: '14px'
          }}
        >
          Back to Dashboard
        </button>
      </div>

      <div style={{
        padding: '16px',
        backgroundColor: '#f5f5f5',
        borderRadius: '4px',
        marginBottom: '24px',
        display: 'flex',
        gap: '24px'
      }}>
        <div>
          <span style={{ fontSize: '14px', color: '#666' }}>Total Transactions: </span>
          <span style={{ fontSize: '18px', fontWeight: 'bold' }}>{transactions.length}</span>
        </div>
        <div>
          <span style={{ fontSize: '14px', color: '#666' }}>Showing: </span>
          <span style={{ fontSize: '18px', fontWeight: 'bold' }}>{filteredTransactions.length}</span>
        </div>
      </div>

      <CategoryFilter selectedCategory={selectedCategory} onCategoryChange={setSelectedCategory} />

      <div style={{ overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', backgroundColor: '#fff', boxShadow: '0 1px 3px rgba(0,0,0,0.1)' }}>
          <thead>
            <tr style={{ backgroundColor: '#f5f5f5', borderBottom: '2px solid #ddd' }}>
              <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px', fontWeight: '600' }}>Date</th>
              <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px', fontWeight: '600' }}>Description</th>
              <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px', fontWeight: '600' }}>Merchant</th>
              <th style={{ padding: '12px', textAlign: 'right', fontSize: '14px', fontWeight: '600' }}>Amount</th>
              <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px', fontWeight: '600' }}>Category</th>
              <th style={{ padding: '12px', textAlign: 'left', fontSize: '14px', fontWeight: '600' }}>Confidence</th>
              <th style={{ padding: '12px', textAlign: 'center', fontSize: '14px', fontWeight: '600' }}>Action</th>
            </tr>
          </thead>
          <tbody>
            {filteredTransactions.map((txn) => (
              <tr key={txn.transaction_id} style={{ borderBottom: '1px solid #eee' }}>
                <td style={{ padding: '12px', fontSize: '13px' }}>{txn.date}</td>
                <td style={{ padding: '12px', fontSize: '13px', maxWidth: '250px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                  {txn.description}
                </td>
                <td style={{ padding: '12px', fontSize: '13px' }}>{txn.merchant || '-'}</td>
                <td style={{ padding: '12px', textAlign: 'right', fontSize: '13px', fontWeight: '500' }}>
                  {txn.debit ? (
                    <span style={{ color: '#d32f2f' }}>- Rs {txn.debit.toFixed(2)}</span>
                  ) : txn.credit ? (
                    <span style={{ color: '#388e3c' }}>+ Rs {txn.credit.toFixed(2)}</span>
                  ) : '-'}
                </td>
                <td style={{ padding: '12px' }}>
                  {editingId === txn.transaction_id ? (
                    <select
                      value={txn.category}
                      onChange={(e) => handleCategoryUpdate(txn.transaction_id, e.target.value)}
                      onBlur={() => setEditingId(null)}
                      autoFocus
                      style={{
                        padding: '4px 8px',
                        fontSize: '12px',
                        border: '1px solid #ddd',
                        borderRadius: '4px'
                      }}
                    >
                      {CATEGORIES.map(cat => (
                        <option key={cat} value={cat}>{cat}</option>
                      ))}
                    </select>
                  ) : (
                    <CategoryBadge category={txn.category} />
                  )}
                </td>
                <td style={{ padding: '12px' }}>
                  <ConfidenceIndicator confidence={txn.confidence} />
                </td>
                <td style={{ padding: '12px', textAlign: 'center' }}>
                  <button
                    onClick={() => setEditingId(txn.transaction_id)}
                    style={{
                      padding: '4px 12px',
                      fontSize: '12px',
                      backgroundColor: 'transparent',
                      border: '1px solid #50C878',
                      color: '#50C878',
                      borderRadius: '4px',
                      cursor: 'pointer'
                    }}
                  >
                    Edit
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {filteredTransactions.length === 0 && (
        <div style={{ textAlign: 'center', padding: '40px', color: '#666' }}>
          No transactions found for the selected category.
        </div>
      )}
    </div>
  );
};

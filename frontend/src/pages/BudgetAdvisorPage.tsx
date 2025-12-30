import React, { useEffect, useState } from 'react';
import { SpendingSummary } from '../components/dashboard/SpendingSummary';
import { CategorySpendingChart } from '../components/dashboard/CategorySpendingChart';
import { TopCategoriesCard } from '../components/dashboard/TopCategoriesCard';
import { AnalyticsSection } from '../components/analytics/AnalyticsSection';
import { dashboardService } from '../services/dashboardService';
import { CategorySpending } from '../models/DashboardData';
import { LoadingSpinner } from '../components/common/LoadingSpinner';

export const BudgetAdvisorPage: React.FC = () => {
  const [categories, setCategories] = useState<CategorySpending[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string>('');

  useEffect(() => {
    loadDashboardData();
  }, []);

  const loadDashboardData = async () => {
    try {
      const data = await dashboardService.getCategorySpending();
      setCategories(data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load dashboard data');
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <LoadingSpinner fullScreen />;

  if (error) {
    return (
      <div style={styles.errorContainer}>
        <div style={styles.errorBox}>
          <h3>Error Loading Data</h3>
          <p>{error}</p>
          <button onClick={loadDashboardData} style={styles.retryButton}>
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (categories.length === 0) {
    return (
      <div style={styles.emptyContainer}>
        <div style={styles.emptyBox}>
          <h3>No Transaction Data</h3>
          <p>Please upload and categorize your bank statements first.</p>
        </div>
      </div>
    );
  }

  const totalDebit = categories.reduce((sum, cat) => sum + cat.total_amount, 0);
  const totalCredit = 0;
  const balance = totalCredit - totalDebit;

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Budget Advisor</h1>
      
      <section style={styles.section}>
        <h2 style={styles.sectionTitle}>SPENDING OVERVIEW</h2>
        <SpendingSummary 
          totalDebit={totalDebit}
          totalCredit={totalCredit}
          balance={balance}
        />
        
        <CategorySpendingChart data={categories} />
        
        <div style={styles.gridRow}>
          <TopCategoriesCard data={categories} />
        </div>
      </section>

      <AnalyticsSection categories={categories} />
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '30px 20px'
  },
  title: {
    fontSize: '32px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '30px',
    textAlign: 'center'
  },
  section: {
    marginBottom: '40px'
  },
  sectionTitle: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: '#4A90E2',
    marginBottom: '20px',
    paddingBottom: '10px',
    borderBottom: '2px solid #4A90E2'
  },
  gridRow: {
    display: 'grid',
    gridTemplateColumns: '1fr',
    gap: '20px'
  },
  errorContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '400px'
  },
  errorBox: {
    textAlign: 'center',
    padding: '40px',
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
  },
  retryButton: {
    marginTop: '20px',
    padding: '10px 20px',
    backgroundColor: '#4A90E2',
    color: '#fff',
    border: 'none',
    borderRadius: '6px',
    cursor: 'pointer',
    fontSize: '14px'
  },
  emptyContainer: {
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    minHeight: '400px'
  },
  emptyBox: {
    textAlign: 'center',
    padding: '40px',
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)'
  }
};

import React, { useState } from 'react';
import { CategorySpending } from '../../models/DashboardData';
import { SavingsReport } from '../../models/AnalyticsData';
import { analyticsService } from '../../services/analyticsService';
import { SavingsReportDisplay } from './SavingsReportDisplay';

interface AnalyticsSectionProps {
  categories: CategorySpending[];
}

export const AnalyticsSection: React.FC<AnalyticsSectionProps> = ({ categories }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const [budgetLimit, setBudgetLimit] = useState<string>('');
  const [targetMonth, setTargetMonth] = useState<string>('');
  const [selectedCategories, setSelectedCategories] = useState<string[]>([]);
  const [savingsReport, setSavingsReport] = useState<SavingsReport[] | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string>('');

  const handleCategoryToggle = (category: string) => {
    setSelectedCategories(prev =>
      prev.includes(category)
        ? prev.filter(c => c !== category)
        : [...prev, category]
    );
  };

  const handleGenerateReport = async () => {
    if (!budgetLimit || parseFloat(budgetLimit) <= 0) {
      setError('Please enter a valid budget limit');
      return;
    }
    if (!targetMonth) {
      setError('Please select a target month');
      return;
    }
    if (selectedCategories.length === 0) {
      setError('Please select at least one category');
      return;
    }

    setError('');
    setLoading(true);

    try {
      const response = await analyticsService.generateForecast({
        budget_limit: parseFloat(budgetLimit),
        target_month: targetMonth,
        categories: selectedCategories,
        save_budget: false
      });

      setSavingsReport(response.data);
    } catch (err: any) {
      console.error('Forecast error:', err);
      if (err.response?.status === 401) {
        setError('Unauthorized: Please login again');
      } else if (err.response?.data?.error?.message) {
        setError(err.response.data.error.message);
      } else {
        setError(err.response?.data?.error || 'Failed to generate forecast');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.header} onClick={() => setIsExpanded(!isExpanded)}>
        <span style={styles.headerIcon}>{isExpanded ? '▼' : '▶'}</span>
        <h3 style={styles.headerTitle}>ANALYZE SPENDING & FORECAST</h3>
      </div>

      {isExpanded && (
        <div style={styles.content}>
          <div style={styles.formGrid}>
            <div style={styles.formGroup}>
              <label style={styles.label}>Budget Limit (₹)</label>
              <input
                type="number"
                value={budgetLimit}
                onChange={(e) => setBudgetLimit(e.target.value)}
                placeholder="Enter budget limit"
                style={styles.input}
              />
            </div>

            <div style={styles.formGroup}>
              <label style={styles.label}>Target Date</label>
              <input
                type="date"
                value={targetMonth}
                onChange={(e) => setTargetMonth(e.target.value)}
                style={styles.input}
              />
            </div>
          </div>

          <div style={styles.formGroup}>
            <label style={styles.label}>Select Categories</label>
            <div style={styles.checkboxGrid}>
              {categories.map((cat) => (
                <label key={cat.category} style={styles.checkboxLabel}>
                  <input
                    type="checkbox"
                    checked={selectedCategories.includes(cat.category)}
                    onChange={() => handleCategoryToggle(cat.category)}
                    style={styles.checkbox}
                  />
                  <span style={styles.checkboxText}>
                    {cat.category} (₹{cat.total_amount.toFixed(2)})
                  </span>
                </label>
              ))}
            </div>
          </div>

          {error && <div style={styles.error}>{error}</div>}

          <button
            onClick={handleGenerateReport}
            disabled={loading}
            style={styles.button}
          >
            {loading ? 'Generating...' : 'Generate Savings Report'}
          </button>

          {savingsReport && (
            <SavingsReportDisplay data={savingsReport} targetMonth={targetMonth} />
          )}
        </div>
      )}
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    backgroundColor: '#fff',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    marginTop: '30px',
    overflow: 'hidden'
  },
  header: {
    padding: '20px',
    backgroundColor: '#f8f9fa',
    cursor: 'pointer',
    display: 'flex',
    alignItems: 'center',
    transition: 'background-color 0.2s'
  },
  headerIcon: {
    fontSize: '16px',
    marginRight: '12px',
    color: '#4A90E2'
  },
  headerTitle: {
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#333',
    margin: 0
  },
  content: {
    padding: '25px'
  },
  formGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(2, 1fr)',
    gap: '20px',
    marginBottom: '20px'
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column'
  },
  label: {
    fontSize: '14px',
    fontWeight: '600',
    color: '#333',
    marginBottom: '8px'
  },
  input: {
    padding: '10px',
    fontSize: '14px',
    border: '1px solid #ddd',
    borderRadius: '6px',
    outline: 'none',
    transition: 'border-color 0.2s'
  },
  checkboxGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '12px',
    marginTop: '8px'
  },
  checkboxLabel: {
    display: 'flex',
    alignItems: 'center',
    cursor: 'pointer',
    padding: '8px',
    borderRadius: '6px',
    transition: 'background-color 0.2s'
  },
  checkbox: {
    marginRight: '8px',
    cursor: 'pointer'
  },
  checkboxText: {
    fontSize: '13px',
    color: '#333'
  },
  error: {
    padding: '12px',
    backgroundColor: '#fee',
    color: '#c33',
    borderRadius: '6px',
    marginBottom: '15px',
    fontSize: '14px'
  },
  button: {
    width: '100%',
    padding: '14px',
    backgroundColor: '#4A90E2',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '16px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'background-color 0.2s'
  }
};

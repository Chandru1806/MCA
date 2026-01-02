import React from 'react';
import { SavingsReport } from '../../models/AnalyticsData';
import jsPDF from 'jspdf';
import { useAuthStore } from '../../store/authStore';

interface SavingsReportDisplayProps {
  data: SavingsReport[];
  targetMonth: string;
}

export const SavingsReportDisplay: React.FC<SavingsReportDisplayProps> = ({ data, targetMonth }) => {
  const { user } = useAuthStore();
  const totalSavings = data.reduce((sum, item) => sum + item.savings, 0);
  const totalCurrentSpending = data.reduce((sum, item) => sum + item.current_spending, 0);
  const totalBudgetLimit = data.reduce((sum, item) => sum + item.budget_limit, 0);
  const savingsPercentage = totalCurrentSpending > 0 ? ((totalSavings / totalCurrentSpending) * 100).toFixed(1) : 0;

  const calculateRiskLevel = (savings: number, currentSpending: number) => {
    const savingsRate = (savings / currentSpending) * 100;
    if (savingsRate > 40) return { level: 'High Risk', color: '#E74C3C', icon: '⚠️' };
    if (savingsRate > 20) return { level: 'Medium Risk', color: '#F39C12', icon: '✓' };
    return { level: 'Achievable', color: '#50C878', icon: '✓' };
  };

  const calculateMonthsToGoal = (savings: number) => {
    if (savings <= 0) return 0;
    // Assuming user wants to save ₹100,000 or 12 months as benchmark
    return Math.ceil(100000 / savings);
  };

  const handleDownloadPDF = () => {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    
    doc.addImage('/Logo/ExpenseIQ_Logo.png', 'PNG', 15, 10, 30, 30);
    
    const fullName = user ? `${user.first_name} ${user.last_name}` : 'User';
    doc.setFontSize(12);
    doc.text(fullName, pageWidth - 15, 20, { align: 'right' });
    doc.setFontSize(16);
    doc.text('Detailed Savings Report', pageWidth - 15, 30, { align: 'right' });
    
    doc.setFontSize(10);
    doc.text(`Report Generated: ${new Date().toLocaleDateString()}`, 15, 50);
    doc.text(`Projection Period: ${targetMonth}`, 15, 57);
    
    doc.setFontSize(14);
    doc.text('SUMMARY OVERVIEW', 15, 70);
    doc.setLineWidth(0.5);
    doc.line(15, 72, pageWidth - 15, 72);
    
    let yPos = 80;
    doc.setFontSize(10);
    doc.text(`Total Monthly Savings: Rs ${totalSavings.toFixed(2)} (${savingsPercentage}% of current spending)`, 15, yPos);
    yPos += 6;
    doc.text(`Current Spending: Rs ${totalCurrentSpending.toFixed(2)} across ${data.length} categories`, 15, yPos);
    yPos += 6;
    doc.text(`New Budget Target: Rs ${totalBudgetLimit.toFixed(2)}`, 15, yPos);
    yPos += 6;
    doc.text(`Annual Savings Potential: Rs ${(totalSavings * 12).toFixed(2)}`, 15, yPos);
    yPos += 6;
    doc.text(`Total Categories: ${data.length}`, 15, yPos);
    yPos += 6;
    doc.text(`Months to Save Rs 100,000: ${calculateMonthsToGoal(totalSavings)} months`, 15, yPos);
    yPos += 6;
    doc.text(`Avg Savings per Category: Rs ${(totalSavings / data.length).toFixed(2)}`, 15, yPos);
    yPos += 12;
    
    doc.setFontSize(14);
    doc.text('CATEGORY-WISE BREAKDOWN', 15, yPos);
    doc.setLineWidth(0.5);
    doc.line(15, yPos + 2, pageWidth - 15, yPos + 2);
    yPos += 10;
    
    data.forEach((item, index) => {
      const risk = calculateRiskLevel(item.savings, item.current_spending);
      const reductionPercent = ((item.savings / item.current_spending) * 100).toFixed(1);
      const budgetUtilization = ((item.budget_limit / item.current_spending) * 100).toFixed(0);
      
      if (yPos > pageHeight - 60) {
        doc.addPage();
        yPos = 20;
      }
      
      doc.setFontSize(12);
      doc.setFont('helvetica', 'bold');
      doc.text(`${index + 1}. ${item.category}`, 15, yPos);
      doc.setFont('helvetica', 'normal');
      doc.setFontSize(9);
      doc.text(`[${risk.level}]`, 15 + doc.getTextWidth(`${index + 1}. ${item.category} `) + 2, yPos);
      yPos += 7;
      
      doc.setFontSize(10);
      doc.text(`   Savings Potential: Rs ${item.savings.toFixed(2)}`, 15, yPos);
      yPos += 6;
      doc.text(`   Current Spending: Rs ${item.current_spending.toFixed(2)}`, 15, yPos);
      yPos += 6;
      doc.text(`   Target Budget: Rs ${item.budget_limit.toFixed(2)}`, 15, yPos);
      yPos += 6;
      doc.text(`   Reduction Required: ${reductionPercent}%`, 15, yPos);
      yPos += 6;
      doc.text(`   Annual Savings: Rs ${(item.savings * 12).toFixed(2)}`, 15, yPos);
      yPos += 6;
      doc.text(`   Budget Utilization: ${budgetUtilization}%`, 15, yPos);
      yPos += 6;
      
      doc.setFontSize(9);
      doc.setFont('helvetica', 'italic');
      const insight = `   Insight: To achieve your ${item.category} budget goal, reduce spending by Rs ${item.savings.toFixed(2)} (${reductionPercent}%).${item.savings > 0 && item.savings > item.budget_limit * 0.5 ? ' This is challenging - consider a phased approach.' : ''}`;
      const splitInsight = doc.splitTextToSize(insight, pageWidth - 30);
      doc.text(splitInsight, 15, yPos);
      yPos += splitInsight.length * 5 + 8;
      doc.setFont('helvetica', 'normal');
    });
    
    if (yPos > pageHeight - 30) {
      doc.addPage();
      yPos = 20;
    }
    
    doc.setFontSize(10);
    doc.setFont('helvetica', 'italic');
    doc.text('Generated by ExpenseIQ - Smart Personal Expense & Budget Advisor', pageWidth / 2, pageHeight - 10, { align: 'center' });
    
    doc.save(`ExpenseIQ_Savings_Report_${new Date().toISOString().split('T')[0]}.pdf`);
  };

  return (
    <div style={styles.container}>
      <h4 style={styles.title}>📊 Detailed Savings Report</h4>
      
      {/* Summary Cards */}
      <div style={styles.summaryGrid}>
        <div style={styles.summaryCard}>
          <div style={styles.summaryLabel}>Total Monthly Savings</div>
          <div style={styles.summaryValue}>₹{totalSavings.toFixed(2)}</div>
          <div style={styles.summarySubtext}>{savingsPercentage}% of current spending</div>
        </div>
        
        <div style={styles.summaryCard}>
          <div style={styles.summaryLabel}>Current Spending</div>
          <div style={styles.summaryValue}>₹{totalCurrentSpending.toFixed(2)}</div>
          <div style={styles.summarySubtext}>Across {data.length} categories</div>
        </div>
        
        <div style={styles.summaryCard}>
          <div style={styles.summaryLabel}>New Budget Target</div>
          <div style={styles.summaryValue}>₹{totalBudgetLimit.toFixed(2)}</div>
          <div style={styles.summarySubtext}>Reduction needed</div>
        </div>
        
        <div style={styles.summaryCard}>
          <div style={styles.summaryLabel}>Annual Savings Potential</div>
          <div style={{...styles.summaryValue, color: '#50C878'}}>₹{(totalSavings * 12).toFixed(2)}</div>
          <div style={styles.summarySubtext}>If sustained for 12 months</div>
        </div>
      </div>

      {/* Detailed Report */}
      <div style={styles.reportList}>
        {data.map((item) => {
          const risk = calculateRiskLevel(item.savings, item.current_spending);
          const savingsPercent = ((item.savings / item.current_spending) * 100).toFixed(1);
          const reductionPercent = ((item.savings / item.current_spending) * 100).toFixed(1);
          
          return (
            <div key={item.category} style={styles.reportItem}>
              <div style={styles.categoryHeader}>
                <div>
                  <span style={styles.categoryName}>{item.category}</span>
                  <span style={{...styles.riskBadge, borderColor: risk.color, color: risk.color}}>
                    {risk.icon} {risk.level}
                  </span>
                </div>
                <span style={{...styles.savingsAmount, color: risk.color}}>
                  ₹{item.savings.toFixed(2)}
                </span>
              </div>
              
              <div style={styles.analyticsGrid}>
                <div style={styles.analyticCard}>
                  <div style={styles.analyticLabel}>Current Spending</div>
                  <div style={styles.analyticValue}>₹{item.current_spending.toFixed(2)}</div>
                </div>
                
                <div style={styles.analyticCard}>
                  <div style={styles.analyticLabel}>Target Budget</div>
                  <div style={styles.analyticValue}>₹{item.budget_limit.toFixed(2)}</div>
                </div>
                
                <div style={styles.analyticCard}>
                  <div style={styles.analyticLabel}>Reduction %</div>
                  <div style={styles.analyticValue}>{reductionPercent}%</div>
                </div>
                
                <div style={styles.analyticCard}>
                  <div style={styles.analyticLabel}>Annual Savings</div>
                  <div style={{...styles.analyticValue, color: '#50C878'}}>₹{(item.savings * 12).toFixed(2)}</div>
                </div>
              </div>
              
              <div style={styles.progressSection}>
                <div style={styles.progressLabel}>
                  <span>Budget Utilization</span>
                  <span>{((item.budget_limit / item.current_spending) * 100).toFixed(0)}%</span>
                </div>
                <div style={styles.progressBar}>
                  <div 
                    style={{
                      ...styles.progressFill,
                      width: `${Math.min((item.budget_limit / item.current_spending) * 100, 100)}%`,
                      backgroundColor: risk.color
                    }}
                  />
                </div>
              </div>
              
              <div style={styles.tipBox}>
                <span style={styles.tipTitle}>💡 Insight:</span>
                <span style={styles.tipText}>
                  To achieve your {item.category} budget goal, reduce spending by ₹{item.savings.toFixed(2)} ({reductionPercent}%).
                  {item.savings > 0 && item.savings > item.budget_limit * 0.5 && 
                    ' This is challenging - consider a phased approach.'}
                </span>
              </div>
            </div>
          );
        })}
      </div>
      
      {/* Summary Footer */}
      <div style={styles.summaryFooter}>
        <div style={styles.footerItem}>
          <span>Total Categories:</span>
          <span style={styles.footerValue}>{data.length}</span>
        </div>
        <div style={styles.footerItem}>
          <span>Months to Save:</span>
          <span style={styles.footerValue}>{calculateMonthsToGoal(totalSavings)} months</span>
        </div>
        <div style={styles.footerItem}>
          <span>Avg Savings per Category:</span>
          <span style={styles.footerValue}>₹{(totalSavings / data.length).toFixed(2)}</span>
        </div>
      </div>
      
      <button onClick={handleDownloadPDF} style={styles.downloadButton}>
        📄 Download Detailed PDF Report
      </button>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    marginTop: '25px',
    padding: '20px',
    backgroundColor: '#f8f9fa',
    borderRadius: '8px'
  },
  title: {
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '20px'
  },
  summaryGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '15px',
    marginBottom: '25px'
  },
  summaryCard: {
    padding: '15px',
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 1px 4px rgba(0,0,0,0.1)',
    borderLeft: '4px solid #4A90E2'
  },
  summaryLabel: {
    fontSize: '12px',
    color: '#666',
    fontWeight: '500',
    marginBottom: '5px'
  },
  summaryValue: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '5px'
  },
  summarySubtext: {
    fontSize: '11px',
    color: '#999'
  },
  reportList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px',
    marginBottom: '20px'
  },
  reportItem: {
    padding: '20px',
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 1px 4px rgba(0,0,0,0.1)',
    borderTop: '3px solid #4A90E2'
  },
  categoryHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: '15px',
    gap: '10px'
  },
  categoryName: {
    fontSize: '16px',
    fontWeight: '700',
    color: '#333',
    marginRight: '10px'
  },
  riskBadge: {
    fontSize: '12px',
    padding: '4px 8px',
    border: '1px solid',
    borderRadius: '4px',
    fontWeight: '600'
  },
  savingsAmount: {
    fontSize: '18px',
    fontWeight: 'bold',
    color: '#50C878'
  },
  analyticsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(120px, 1fr))',
    gap: '10px',
    marginBottom: '15px'
  },
  analyticCard: {
    padding: '10px',
    backgroundColor: '#f5f5f5',
    borderRadius: '6px',
    textAlign: 'center' as const
  },
  analyticLabel: {
    fontSize: '11px',
    color: '#666',
    fontWeight: '500',
    marginBottom: '3px'
  },
  analyticValue: {
    fontSize: '14px',
    fontWeight: 'bold',
    color: '#333'
  },
  progressSection: {
    marginBottom: '15px'
  },
  progressLabel: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '12px',
    color: '#666',
    fontWeight: '600',
    marginBottom: '6px'
  },
  progressBar: {
    height: '10px',
    backgroundColor: '#e0e0e0',
    borderRadius: '5px',
    overflow: 'hidden'
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#4A90E2',
    transition: 'width 0.3s ease'
  },
  tipBox: {
    padding: '12px',
    backgroundColor: '#f0f7ff',
    borderLeft: '3px solid #4A90E2',
    borderRadius: '4px',
    fontSize: '12px'
  },
  tipTitle: {
    fontWeight: '700',
    color: '#4A90E2',
    marginRight: '5px'
  },
  tipText: {
    color: '#666'
  },
  summaryFooter: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
    gap: '15px',
    padding: '15px',
    backgroundColor: '#fff',
    borderRadius: '8px',
    marginBottom: '15px'
  },
  footerItem: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '13px',
    color: '#666'
  },
  footerValue: {
    fontWeight: 'bold',
    color: '#333'
  },
  downloadButton: {
    width: '100%',
    padding: '14px',
    backgroundColor: '#4A90E2',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'background-color 0.2s'
  }
};

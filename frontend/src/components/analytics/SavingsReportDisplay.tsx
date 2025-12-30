import React from 'react';
import { SavingsReport } from '../../models/AnalyticsData';
import jsPDF from 'jspdf';

interface SavingsReportDisplayProps {
  data: SavingsReport[];
  targetMonth: string;
}

export const SavingsReportDisplay: React.FC<SavingsReportDisplayProps> = ({ data, targetMonth }) => {
  const totalSavings = data.reduce((sum, item) => sum + item.savings, 0);

  const handleDownloadPDF = () => {
    const doc = new jsPDF();
    const pageWidth = doc.internal.pageSize.getWidth();
    
    doc.addImage('/Logo/ExpenseIQ_Logo.png', 'PNG', 15, 10, 30, 30);
    
    const userName = localStorage.getItem('user_name') || 'User';
    doc.setFontSize(12);
    doc.text(userName, pageWidth - 15, 20, { align: 'right' });
    doc.setFontSize(16);
    doc.text('Savings Report', pageWidth - 15, 30, { align: 'right' });
    
    doc.setFontSize(10);
    doc.text(`Report Generated: ${new Date().toLocaleDateString()}`, 15, 50);
    doc.text(`Projection Period: ${targetMonth}`, 15, 57);
    
    doc.setFontSize(14);
    doc.text('SAVINGS ANALYSIS', 15, 70);
    doc.setLineWidth(0.5);
    doc.line(15, 72, pageWidth - 15, 72);
    
    let yPos = 85;
    data.forEach((item, index) => {
      doc.setFontSize(12);
      doc.text(`${index + 1}. ${item.category}`, 15, yPos);
      yPos += 7;
      
      doc.setFontSize(10);
      doc.text(`Current Spending: Rs ${item.current_spending.toFixed(2)}`, 20, yPos);
      yPos += 6;
      doc.text(`Budget Limit: Rs ${item.budget_limit.toFixed(2)}`, 20, yPos);
      yPos += 6;
      doc.text(`Savings Potential: Rs ${item.savings.toFixed(2)}`, 20, yPos);
      yPos += 10;
      
      if (yPos > 270) {
        doc.addPage();
        yPos = 20;
      }
    });
    
    doc.setFontSize(12);
    doc.text(`TOTAL SAVINGS POTENTIAL: Rs ${totalSavings.toFixed(2)}`, 15, yPos);
    
    doc.save(`ExpenseIQ_Savings_Report_${new Date().toISOString().split('T')[0]}.pdf`);
  };

  return (
    <div style={styles.container}>
      <h4 style={styles.title}>Savings Report</h4>
      
      <div style={styles.reportList}>
        {data.map((item) => (
          <div key={item.category} style={styles.reportItem}>
            <div style={styles.categoryHeader}>
              <span style={styles.categoryName}>{item.category}</span>
              <span style={styles.savingsAmount}>
                Save ₹{item.savings.toFixed(2)}
              </span>
            </div>
            
            <div style={styles.details}>
              <div style={styles.detailRow}>
                <span>Current Spending:</span>
                <span style={styles.detailValue}>₹{item.current_spending.toFixed(2)}</span>
              </div>
              <div style={styles.detailRow}>
                <span>Budget Limit:</span>
                <span style={styles.detailValue}>₹{item.budget_limit.toFixed(2)}</span>
              </div>
            </div>
            
            <div style={styles.progressBar}>
              <div 
                style={{
                  ...styles.progressFill,
                  width: `${Math.min((item.budget_limit / item.current_spending) * 100, 100)}%`
                }}
              />
            </div>
          </div>
        ))}
      </div>
      
      <div style={styles.totalSection}>
        <span style={styles.totalLabel}>Total Savings Potential:</span>
        <span style={styles.totalValue}>₹{totalSavings.toFixed(2)}</span>
      </div>
      
      <button onClick={handleDownloadPDF} style={styles.downloadButton}>
        Download PDF Report
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
    fontSize: '16px',
    fontWeight: 'bold',
    color: '#333',
    marginBottom: '20px'
  },
  reportList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '15px',
    marginBottom: '20px'
  },
  reportItem: {
    padding: '15px',
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 1px 4px rgba(0,0,0,0.1)'
  },
  categoryHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px'
  },
  categoryName: {
    fontSize: '15px',
    fontWeight: '600',
    color: '#333'
  },
  savingsAmount: {
    fontSize: '16px',
    fontWeight: 'bold',
    color: '#50C878'
  },
  details: {
    display: 'flex',
    flexDirection: 'column',
    gap: '6px',
    marginBottom: '12px'
  },
  detailRow: {
    display: 'flex',
    justifyContent: 'space-between',
    fontSize: '13px',
    color: '#666'
  },
  detailValue: {
    fontWeight: '600',
    color: '#333'
  },
  progressBar: {
    height: '8px',
    backgroundColor: '#e0e0e0',
    borderRadius: '4px',
    overflow: 'hidden'
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#4A90E2',
    transition: 'width 0.3s ease'
  },
  totalSection: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '15px',
    backgroundColor: '#fff',
    borderRadius: '8px',
    marginBottom: '15px'
  },
  totalLabel: {
    fontSize: '16px',
    fontWeight: '600',
    color: '#333'
  },
  totalValue: {
    fontSize: '20px',
    fontWeight: 'bold',
    color: '#50C878'
  },
  downloadButton: {
    width: '100%',
    padding: '12px',
    backgroundColor: '#50C878',
    color: '#fff',
    border: 'none',
    borderRadius: '8px',
    fontSize: '15px',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'background-color 0.2s'
  }
};

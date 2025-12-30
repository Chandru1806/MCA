import React from 'react';

interface SpendingSummaryProps {
  totalDebit: number;
  totalCredit: number;
  balance: number;
}

export const SpendingSummary: React.FC<SpendingSummaryProps> = ({
  totalDebit,
  totalCredit,
  balance
}) => {
  return (
    <div style={styles.container}>
      <div style={{ ...styles.card, ...styles.debitCard }}>
        <div style={styles.cardIcon}>💸</div>
        <div style={styles.cardContent}>
          <div style={styles.cardLabel}>Total Debit</div>
          <div style={styles.cardValue}>₹{totalDebit.toFixed(2)}</div>
        </div>
      </div>

      <div style={{ ...styles.card, ...styles.creditCard }}>
        <div style={styles.cardIcon}>💰</div>
        <div style={styles.cardContent}>
          <div style={styles.cardLabel}>Total Credit</div>
          <div style={styles.cardValue}>₹{totalCredit.toFixed(2)}</div>
        </div>
      </div>

      <div style={{ ...styles.card, ...styles.balanceCard }}>
        <div style={styles.cardIcon}>💳</div>
        <div style={styles.cardContent}>
          <div style={styles.cardLabel}>Balance</div>
          <div style={styles.cardValue}>₹{balance.toFixed(2)}</div>
        </div>
      </div>
    </div>
  );
};

const styles: Record<string, React.CSSProperties> = {
  container: {
    display: 'grid',
    gridTemplateColumns: 'repeat(3, 1fr)',
    gap: '20px',
    marginBottom: '30px'
  },
  card: {
    display: 'flex',
    alignItems: 'center',
    padding: '20px',
    borderRadius: '12px',
    boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
    transition: 'transform 0.2s',
    cursor: 'default'
  },
  debitCard: {
    background: 'linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%)'
  },
  creditCard: {
    background: 'linear-gradient(135deg, #50C878 0%, #6FD89A 100%)'
  },
  balanceCard: {
    background: 'linear-gradient(135deg, #4A90E2 0%, #6BA5E7 100%)'
  },
  cardIcon: {
    fontSize: '40px',
    marginRight: '15px'
  },
  cardContent: {
    flex: 1
  },
  cardLabel: {
    fontSize: '14px',
    color: 'rgba(255,255,255,0.9)',
    marginBottom: '5px',
    fontWeight: '500'
  },
  cardValue: {
    fontSize: '24px',
    fontWeight: 'bold',
    color: '#fff'
  }
};

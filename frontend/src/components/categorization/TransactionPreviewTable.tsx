import React from 'react';
import { TransactionPreview } from '../../models/Transaction';

interface Props {
  transactions: TransactionPreview[];
}

export const TransactionPreviewTable: React.FC<Props> = ({ transactions }) => {
  return (
    <div style={{ maxHeight: '300px', overflowY: 'auto', border: '1px solid #ddd', borderRadius: '4px' }}>
      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '12px' }}>
        <thead style={{ position: 'sticky', top: 0, backgroundColor: '#f5f5f5', zIndex: 1 }}>
          <tr>
            <th style={{ padding: '8px', textAlign: 'left', borderBottom: '2px solid #ddd' }}>#</th>
            <th style={{ padding: '8px', textAlign: 'left', borderBottom: '2px solid #ddd' }}>Date</th>
            <th style={{ padding: '8px', textAlign: 'left', borderBottom: '2px solid #ddd' }}>Description</th>
            <th style={{ padding: '8px', textAlign: 'right', borderBottom: '2px solid #ddd' }}>Debit</th>
            <th style={{ padding: '8px', textAlign: 'right', borderBottom: '2px solid #ddd' }}>Credit</th>
            <th style={{ padding: '8px', textAlign: 'right', borderBottom: '2px solid #ddd' }}>Balance</th>
          </tr>
        </thead>
        <tbody>
          {transactions.map((txn) => (
            <tr key={txn.row_number} style={{ borderBottom: '1px solid #eee' }}>
              <td style={{ padding: '8px' }}>{txn.row_number}</td>
              <td style={{ padding: '8px' }}>{txn.date}</td>
              <td style={{ padding: '8px', maxWidth: '200px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                {txn.description}
              </td>
              <td style={{ padding: '8px', textAlign: 'right', color: '#d32f2f' }}>
                {txn.debit ? `Rs ${txn.debit.toFixed(2)}` : '-'}
              </td>
              <td style={{ padding: '8px', textAlign: 'right', color: '#388e3c' }}>
                {txn.credit ? `Rs ${txn.credit.toFixed(2)}` : '-'}
              </td>
              <td style={{ padding: '8px', textAlign: 'right' }}>
                {txn.balance ? `Rs ${txn.balance.toFixed(2)}` : '-'}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

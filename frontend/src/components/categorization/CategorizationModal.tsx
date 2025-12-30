import React, { useState, useEffect } from 'react';
import { transactionService } from '../../services/transactionService';
import { categorizationService } from '../../services/categorizationService';
import { TransactionPreviewTable } from './TransactionPreviewTable';
import { ValidationSummary } from './ValidationSummary';
import { CategorizationProgress } from './CategorizationProgress';
import { PreviewResponse } from '../../models/Transaction';

interface Props {
  isOpen: boolean;
  onClose: () => void;
  statementId: number;
  onSuccess: () => void;
}

type Step = 'preview' | 'categorizing' | 'success';

export const CategorizationModal: React.FC<Props> = ({ isOpen, onClose, statementId, onSuccess }) => {
  const [step, setStep] = useState<Step>('preview');
  const [previewData, setPreviewData] = useState<PreviewResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [progress, setProgress] = useState({ current: 0, total: 0 });
  const [showRejected, setShowRejected] = useState(false);

  useEffect(() => {
    if (isOpen && statementId) {
      loadPreview();
    }
  }, [isOpen, statementId]);

  const loadPreview = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await transactionService.previewTransactions(statementId);
      setPreviewData(data);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to load preview');
    } finally {
      setLoading(false);
    }
  };

  const handleImportAndCategorize = async () => {
    try {
      setLoading(true);
      setError(null);
      setStep('categorizing');

      const importResult = await transactionService.importTransactions(statementId);
      setProgress({ current: importResult.count, total: importResult.count });

      await new Promise(resolve => setTimeout(resolve, 500));

      const categorizeResult = await categorizationService.categorizeTransactions(statementId);
      
      setStep('success');
      setTimeout(() => {
        onSuccess();
      }, 1500);
    } catch (err: any) {
      setError(err.response?.data?.error || 'Failed to import and categorize');
      setStep('preview');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    if (step !== 'categorizing') {
      setStep('preview');
      setPreviewData(null);
      setError(null);
      setShowRejected(false);
      onClose();
    }
  };

  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0, 0, 0, 0.5)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      zIndex: 1000
    }}>
      <div style={{
        backgroundColor: '#fff',
        borderRadius: '8px',
        width: '80%',
        maxWidth: '900px',
        maxHeight: '85vh',
        display: 'flex',
        flexDirection: 'column',
        boxShadow: '0 4px 20px rgba(0, 0, 0, 0.15)'
      }}>
        <div style={{
          padding: '20px 24px',
          borderBottom: '1px solid #e0e0e0',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center'
        }}>
          <h2 style={{ margin: 0, fontSize: '18px', fontWeight: 'bold' }}>
            Import & Categorize Transactions
          </h2>
          <button
            onClick={handleClose}
            disabled={step === 'categorizing'}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '24px',
              cursor: step === 'categorizing' ? 'not-allowed' : 'pointer',
              color: '#666',
              padding: '0',
              width: '30px',
              height: '30px'
            }}
          >
            &times;
          </button>
        </div>

        <div style={{ flex: 1, overflowY: 'auto', padding: '24px' }}>
          {error && (
            <div style={{
              padding: '12px 16px',
              backgroundColor: '#ffebee',
              color: '#c62828',
              borderRadius: '4px',
              marginBottom: '16px',
              fontSize: '14px'
            }}>
              {error}
            </div>
          )}

          {step === 'preview' && previewData && (
            <>
              <ValidationSummary
                total={previewData.total}
                valid={previewData.valid}
                rejected={previewData.rejected}
                onViewRejected={() => setShowRejected(!showRejected)}
              />

              {showRejected && previewData.rejected_rows.length > 0 ? (
                <>
                  <h3 style={{ fontSize: '14px', marginBottom: '12px', color: '#d32f2f' }}>
                    Rejected Rows (will be skipped):
                  </h3>
                  <div style={{ marginBottom: '16px' }}>
                    {previewData.rejected_rows.map((row) => (
                      <div key={row.row_number} style={{
                        padding: '8px',
                        backgroundColor: '#ffebee',
                        borderRadius: '4px',
                        marginBottom: '8px',
                        fontSize: '12px'
                      }}>
                        <strong>Row {row.row_number}:</strong> {row.errors?.join(', ')}
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <>
                  <h3 style={{ fontSize: '14px', marginBottom: '12px' }}>Preview (First 10 rows):</h3>
                  <TransactionPreviewTable transactions={previewData.preview} />
                </>
              )}
            </>
          )}

          {step === 'categorizing' && (
            <CategorizationProgress
              current={progress.current}
              total={progress.total}
              status="Categorizing transactions..."
            />
          )}

          {step === 'success' && (
            <div style={{ textAlign: 'center', padding: '40px 20px' }}>
              <div style={{
                width: '80px',
                height: '80px',
                borderRadius: '50%',
                backgroundColor: '#d4edda',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 20px',
                fontSize: '40px',
                color: '#27AE60'
              }}>
                &#10003;
              </div>
              <h3 style={{ margin: '0 0 8px', fontSize: '18px', color: '#333' }}>
                Success!
              </h3>
              <p style={{ margin: 0, fontSize: '14px', color: '#666' }}>
                {progress.total} transactions categorized successfully
              </p>
            </div>
          )}

          {loading && step === 'preview' && (
            <div style={{ textAlign: 'center', padding: '40px' }}>
              <div style={{
                width: '40px',
                height: '40px',
                border: '4px solid #f3f3f3',
                borderTop: '4px solid #50C878',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite',
                margin: '0 auto'
              }} />
            </div>
          )}
        </div>

        {step === 'preview' && previewData && !loading && (
          <div style={{
            padding: '16px 24px',
            borderTop: '1px solid #e0e0e0',
            display: 'flex',
            justifyContent: 'flex-end',
            gap: '12px'
          }}>
            <button
              onClick={handleClose}
              style={{
                padding: '10px 20px',
                fontSize: '14px',
                border: '1px solid #ddd',
                backgroundColor: '#fff',
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Cancel
            </button>
            <button
              onClick={handleImportAndCategorize}
              disabled={previewData.valid === 0}
              style={{
                padding: '10px 20px',
                fontSize: '14px',
                border: 'none',
                backgroundColor: previewData.valid === 0 ? '#ccc' : '#50C878',
                color: '#fff',
                borderRadius: '4px',
                cursor: previewData.valid === 0 ? 'not-allowed' : 'pointer',
                fontWeight: '500'
              }}
            >
              Import & Categorize
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

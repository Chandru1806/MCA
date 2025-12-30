import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { CategorizationModal } from '../components/categorization/CategorizationModal';
import './Dashboard.css';

interface DashboardCard {
  id: string;
  title: string;
  description: string;
  icon: string;
  route: string;
  color: string;
}

const dashboardCards: DashboardCard[] = [
  {
    id: 'upload',
    title: 'UPLOAD PDF',
    description: 'Upload your bank statement PDF for processing. Supports multiple banks including SBI, HDFC, ICICI, KOTAK, and more. Secure and fast extraction.',
    icon: '📄',
    route: '/upload',
    color: '#4A90E2'
  },
  {
    id: 'preprocessing',
    title: 'PREPROCESSING',
    description: 'Validate, repair, normalize transactions and export CSV. Automatically detects missing data, repairs balance inconsistencies, and standardizes formats.',
    icon: '⚙️',
    route: '/preprocessing',
    color: '#7B68EE'
  },
  {
    id: 'categorization',
    title: 'CATEGORIZATION',
    description: 'Automatically categorize expenses with confidence scores. Uses hybrid ML and rule-based classification across 17 categories with merchant detection.',
    icon: '📊',
    route: '/categorization',
    color: '#50C878'
  },
  {
    id: 'advisor',
    title: 'BUDGET ADVISOR',
    description: 'Analyze spending patterns and forecast savings. Get personalized insights, set budget limits, and project future expenses with ML-powered predictions.',
    icon: '💡',
    route: '/advisor',
    color: '#FF6B6B'
  }
];

export const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [statementId, setStatementId] = useState<number | null>(null);

  const handleCardClick = (route: string, cardId: string) => {
    if (cardId === 'categorization') {
      // Get statement ID from localStorage (set during preprocessing)
      const savedStatementId = localStorage.getItem('current_statement_id');
      if (savedStatementId) {
        setStatementId(parseInt(savedStatementId));
        setIsModalOpen(true);
      } else {
        alert('Please upload and preprocess a bank statement first');
      }
    } else {
      navigate(route);
    }
  };

  const handleCategorizationSuccess = () => {
    setIsModalOpen(false);
    if (statementId) {
      navigate('/categorize', { state: { statementId } });
    }
  };

  return (
    <div className="dashboard-container">
      <h1 className="dashboard-title">ExpenseIQ Dashboard</h1>
      <div className="dashboard-grid">
        {dashboardCards.map((card) => (
          <div
            key={card.id}
            className="dashboard-card"
            onClick={() => handleCardClick(card.route, card.id)}
            style={{ '--card-color': card.color } as React.CSSProperties}
          >
            <div className="card-icon-wrapper" style={{ backgroundColor: card.color }}>
              <span className="card-icon">{card.icon}</span>
            </div>
            <h2 className="card-title">{card.title}</h2>
            <p className="card-description">{card.description}</p>
          </div>
        ))}
      </div>

      {statementId && (
        <CategorizationModal
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          statementId={statementId}
          onSuccess={handleCategorizationSuccess}
        />
      )}
    </div>
  );
};

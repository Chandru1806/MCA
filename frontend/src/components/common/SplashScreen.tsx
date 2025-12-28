import React from 'react';
import { useNavigate } from 'react-router-dom';
import { LOGO_PATH } from '../../utils/constants';

export const SplashScreen: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div 
      className="fixed inset-0 flex items-center justify-center bg-white cursor-pointer"
      onClick={() => navigate('/login')}
    >
      <img 
        src={LOGO_PATH} 
        alt="ExpenseIQ" 
        className="max-w-md animate-pulse"
      />
    </div>
  );
};

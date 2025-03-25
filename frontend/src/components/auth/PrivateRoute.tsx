import { Navigate } from 'react-router-dom';
import { useAuthStore } from '../../store/auth';
import { useState } from 'react';

interface PrivateRouteProps {
  children: React.ReactNode;
  requiresImport?: boolean;
  requiresMessage?: boolean;
}

export const PrivateRoute = ({ 
  children, 
  requiresImport = false,
  requiresMessage = false 
}: PrivateRouteProps) => {
  const { 
    token, 
    isGuest, 
    needsLogin,
    getRemainingImports,
    getRemainingMessages
  } = useAuthStore();
  const [showLimitWarning, setShowLimitWarning] = useState(false);

  // If not logged in at all, redirect to home page instead of login
  if (!token) {
    return <Navigate to="/" replace />;
  }

  // Check if guest user has reached limits
  if (isGuest() && needsLogin()) {
    return <Navigate to="/" replace />;
  }

  // For guest users with remaining actions, show warning if they're close to limit
  if (isGuest()) {
    // For import-related pages
    if (requiresImport && getRemainingImports() <= 1) {
      setTimeout(() => setShowLimitWarning(true), 500);
    }
    
    // For message-related pages
    if (requiresMessage && getRemainingMessages() <= 2) {
      setTimeout(() => setShowLimitWarning(true), 500);
    }
  }

  return (
    <>
      {children}
      
      {/* Warning modal for guest users approaching limits */}
      {showLimitWarning && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white dark:bg-dark-100 p-6 rounded-lg max-w-md w-full shadow-xl">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white mb-2">
              Guest Usage Limit
            </h3>
            <p className="text-gray-600 dark:text-gray-300 mb-4">
              {requiresImport && 
                `You have ${getRemainingImports()} chat import${getRemainingImports() !== 1 ? 's' : ''} remaining as a guest user.`
              }
              {requiresMessage && 
                `You have ${getRemainingMessages()} message${getRemainingMessages() !== 1 ? 's' : ''} remaining as a guest user.`
              }
            </p>
            <p className="text-gray-600 dark:text-gray-300 mb-6">
              Create an account to get unlimited access to all features.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowLimitWarning(false)}
                className="px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-800"
              >
                Continue as Guest
              </button>
              <button
                onClick={() => window.location.href = '/'}
                className="px-4 py-2 bg-primary-600 border border-transparent rounded-md text-white hover:bg-primary-700"
              >
                Create Account
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

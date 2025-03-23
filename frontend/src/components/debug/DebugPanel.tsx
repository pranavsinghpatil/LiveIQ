import { useState } from 'react';

interface DebugPanelProps {
  apiStatus?: string;
  authStatus?: string;
  errors?: any[];
  networkInfo?: any;
  title?: string;
  data?: any;
}

export const DebugPanel = ({ 
  apiStatus = 'Unknown', 
  authStatus = 'Unknown',
  errors = [],
  networkInfo = {},
  title,
  data
}: DebugPanelProps) => {
  const [isExpanded, setIsExpanded] = useState(false);

  // If data is provided, use it instead of individual props
  const displayData = data || {
    apiStatus,
    authStatus,
    errors,
    networkInfo
  };

  return (
    <div className="fixed bottom-0 right-0 z-50 bg-gray-800 dark:bg-dark-300 text-white p-2 rounded-tl-md shadow-lg">
      <div className="flex items-center justify-between">
        <button 
          onClick={() => setIsExpanded(!isExpanded)}
          className="text-xs font-mono px-2 py-1 bg-gray-700 dark:bg-dark-400 rounded hover:bg-gray-600 dark:hover:bg-dark-500"
        >
          {isExpanded ? `Hide ${title || 'Debug'}` : `Show ${title || 'Debug'}`}
        </button>
        <div className="ml-2 flex items-center">
          <span className="text-xs mr-2">API:</span>
          <span className={`h-2 w-2 rounded-full ${
            displayData.apiStatus === 'OK' ? 'bg-green-500' : 
            displayData.apiStatus === 'Error' ? 'bg-red-500' : 'bg-yellow-500'
          }`}></span>
          <span className="text-xs mx-2">Auth:</span>
          <span className={`h-2 w-2 rounded-full ${
            displayData.authStatus === 'OK' ? 'bg-green-500' : 
            displayData.authStatus === 'Error' ? 'bg-red-500' : 'bg-yellow-500'
          }`}></span>
        </div>
      </div>

      {isExpanded && (
        <div className="mt-2 p-2 bg-gray-900 dark:bg-dark-400 rounded text-xs font-mono overflow-auto max-h-96 max-w-lg">
          <div className="grid grid-cols-2 gap-1">
            <div className="font-bold">API Status:</div>
            <div className={`${
              displayData.apiStatus === 'OK' ? 'text-green-400' : 
              displayData.apiStatus === 'Error' ? 'text-red-400' : 'text-yellow-400'
            }`}>{displayData.apiStatus}</div>
            
            <div className="font-bold">Auth Status:</div>
            <div className={`${
              displayData.authStatus === 'OK' ? 'text-green-400' : 
              displayData.authStatus === 'Error' ? 'text-red-400' : 'text-yellow-400'
            }`}>{displayData.authStatus}</div>
          </div>

          {displayData.errors && displayData.errors.length > 0 && (
            <div className="mt-2">
              <div className="font-bold text-red-400">Errors:</div>
              <ul className="list-disc pl-4 mt-1">
                {displayData.errors.map((error: any, index: number) => (
                  <li key={index} className="text-red-300">
                    <div>{error.type}: {error.message}</div>
                    {error.timestamp && <div className="text-gray-400 text-xs">{error.timestamp}</div>}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {displayData.networkInfo && Object.keys(displayData.networkInfo).length > 0 && (
            <div className="mt-2">
              <div className="font-bold text-blue-400">Network Info:</div>
              <pre className="bg-gray-800 dark:bg-dark-500 p-1 rounded mt-1 overflow-x-auto">
                {JSON.stringify(displayData.networkInfo, null, 2)}
              </pre>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

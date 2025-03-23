import React, { useState } from 'react';
import { useAuthStore } from '../../store/auth';
import { Dialog } from '@headlessui/react';
import { PlusIcon } from '@heroicons/react/24/outline';

interface ImportChatProps {
  onImportComplete: () => void;
}

export const ImportChat: React.FC<ImportChatProps> = ({ onImportComplete }) => {
  const [isOpen, setIsOpen] = useState(false);
  const { isGuest, getRemainingImports, hasReachedImportLimit } = useAuthStore();

  const remainingImports = getRemainingImports();
  const isLimitReached = hasReachedImportLimit();

  const handleImport = async () => {
    // Import logic will be implemented here
    onImportComplete();
    setIsOpen(false);
  };

  return (
    <div>
      <button
        type="button"
        onClick={() => setIsOpen(true)}
        disabled={isLimitReached}
        className={`inline-flex items-center justify-center font-medium rounded-md focus:outline-none transition-colors duration-200 ease-in-out bg-gradient-to-r from-primary-600 to-primary-700 text-white hover:from-primary-700 hover:to-primary-800 shadow-sm text-sm px-4 py-2 ${
          isLimitReached ? 'opacity-50 cursor-not-allowed' : 'bg-gradient-to-r from-primary-500 to-primary-600 hover:from-primary-600 hover:to-primary-700 shadow-md hover:shadow-lg transition-all duration-300'
        }`}
      >
        <span className="mr-2">
          <PlusIcon className="h-5 w-5" aria-hidden="true" />
        </span>
        Import Chat
      </button>

      {isGuest() && (
        <div className="mt-2 text-sm text-gray-600">
          {isLimitReached ? (
            <span className="text-red-500">No imports remaining</span>
          ) : (
            <span>{remainingImports} import{remainingImports !== 1 ? 's' : ''} remaining</span>
          )}
        </div>
      )}

      <Dialog
        open={isOpen}
        onClose={() => setIsOpen(false)}
        className="fixed inset-0 bg-black bg-opacity-50 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto"
      >
        <Dialog.Panel className="w-full max-w-md transform overflow-hidden rounded-2xl bg-white dark:bg-dark-100 p-6 text-left align-middle shadow-xl transition-all">
          <Dialog.Title
            as="h3"
            className="text-lg font-medium leading-6 text-gray-900 dark:text-gray-100"
          >
            Import from URL or File
          </Dialog.Title>
          <div className="mt-4">
            <div className="border-2 border-dashed border-gray-300 dark:border-dark-300 rounded-lg p-8 text-center">
              <p className="text-gray-600 dark:text-gray-400">
                Drop files here or click to select
              </p>
              {/* File input will be added here */}
            </div>
            <div className="mt-4">
              <input
                type="text"
                placeholder="Or paste a URL"
                className="w-full px-4 py-2 border border-gray-300 dark:border-dark-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary-500 dark:bg-dark-200 dark:text-gray-100"
              />
            </div>
          </div>

          <div className="mt-6 flex justify-end space-x-3">
            <button
              type="button"
              className="px-4 py-2 text-sm font-medium text-gray-700 dark:text-gray-200 hover:bg-gray-50 dark:hover:bg-dark-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              onClick={() => setIsOpen(false)}
            >
              Cancel
            </button>
            <button
              type="button"
              className="px-4 py-2 text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 dark:bg-primary-700 dark:hover:bg-primary-800 rounded-md focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              onClick={handleImport}
            >
              Import
            </button>
          </div>
        </Dialog.Panel>
      </Dialog>
    </div>
  );
};

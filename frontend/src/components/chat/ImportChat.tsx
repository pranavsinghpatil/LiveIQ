import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/auth';
import { Dialog } from '@headlessui/react';
import { PlusIcon, LinkIcon, DocumentIcon, VideoCameraIcon } from '@heroicons/react/24/outline';
import { api } from '../../utils/api';
import { Button } from '../ui/Button';
import { Card } from '../ui/Card';

interface ImportChatProps {
  onImportComplete?: () => void;
  standalone?: boolean;
}

type ImportType = 'link' | 'file' | 'video' | 'other';
type Platform = 'chatgpt' | 'mistral' | 'gemini' | 'youtube' | 'spotify' | 'other';

interface ImportResponse {
  id: string;
  success: boolean;
  message?: string;
}

export const ImportChat: React.FC<ImportChatProps> = ({ onImportComplete, standalone = false }) => {
  const navigate = useNavigate();
  const [isOpen, setIsOpen] = useState(standalone);
  const [importType, setImportType] = useState<ImportType>('link');
  const [platform, setPlatform] = useState<Platform>('chatgpt');
  const [customPlatform, setCustomPlatform] = useState('');
  const [url, setUrl] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const { isGuest, getRemainingImports, hasReachedImportLimit } = useAuthStore();

  const remainingImports = getRemainingImports();
  const isLimitReached = hasReachedImportLimit();

  const handleImport = async () => {
    try {
      setError(null);
      setIsLoading(true);

      let formData = new FormData();
      formData.append('platform', platform === 'other' ? customPlatform : platform);
      formData.append('type', importType);

      if (importType === 'link' || importType === 'video') {
        if (!url) {
          throw new Error('Please enter a valid URL');
        }
        formData.append('url', url);
      } else if (importType === 'file') {
        const file = fileInputRef.current?.files?.[0];
        if (!file) {
          throw new Error('Please select a file to upload');
        }
        formData.append('file', file);
      }

      const response = await api.post<ImportResponse>('/chats/import', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.data.success) {
        if (onImportComplete) {
          onImportComplete();
        }
        setIsOpen(false);
        
        if (standalone) {
          navigate(`/chats/${response.data.id}`);
        }
      } else {
        throw new Error(response.data.message || 'Import failed');
      }
    } catch (error) {
      console.error('Import error:', error);
      setError(error instanceof Error ? error.message : 'An unexpected error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  const platforms: { id: Platform; name: string }[] = [
    { id: 'chatgpt', name: 'ChatGPT' },
    { id: 'mistral', name: 'Mistral AI' },
    { id: 'gemini', name: 'Google Gemini' },
    { id: 'youtube', name: 'YouTube' },
    { id: 'spotify', name: 'Spotify' },
    { id: 'other', name: 'Other Platform' },
  ];

  const importTypes = [
    { id: 'link', name: 'Import from URL', Icon: LinkIcon },
    { id: 'file', name: 'Upload File', Icon: DocumentIcon },
    { id: 'video', name: 'Video/Podcast', Icon: VideoCameraIcon },
  ];

  const renderImportButton = () => (
    <Button
      onClick={() => setIsOpen(true)}
      disabled={isLimitReached}
      className="inline-flex items-center bg-accent-100 hover:bg-accent-200 text-secondary-100 dark:text-primary-100"
    >
      <PlusIcon className="-ml-1 mr-2 h-5 w-5" />
      Import Chat
    </Button>
  );

  const renderImportDialog = () => (
    <Dialog
      open={isOpen}
      onClose={() => !standalone && setIsOpen(false)}
      className="fixed inset-0 z-10 overflow-y-auto"
    >
      <div className="flex min-h-screen items-center justify-center p-4">
        <Dialog.Overlay className="fixed inset-0 bg-secondary-100/30" />

        <Card className="relative mx-auto max-w-md w-full bg-primary-100 dark:bg-secondary-100 p-6 shadow-lg rounded-lg">
          <Dialog.Title className="text-xl font-semibold mb-4 text-secondary-100 dark:text-primary-100">Import Chat</Dialog.Title>

          {error && (
            <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-md text-sm">
              {error}
            </div>
          )}

          <div className="space-y-4">
            {/* Import Type Selection */}
            <div>
              <label className="block text-sm font-medium text-secondary-100 dark:text-primary-100 mb-2">
                Import Type
              </label>
              <div className="grid grid-cols-3 gap-2">
                {importTypes.map(({ id, name, Icon }) => (
                  <button
                    key={id}
                    type="button"
                    onClick={() => setImportType(id as ImportType)}
                    className={`flex flex-col items-center p-3 border rounded-lg ${
                      importType === id
                        ? 'border-accent-100 bg-accent-50 dark:border-accent-200 dark:bg-accent-200/20'
                        : 'border-accent-100/30 hover:bg-primary-200 dark:border-accent-300/30 dark:hover:bg-secondary-200'
                    }`}
                  >
                    <Icon className={`h-6 w-6 ${importType === id ? 'text-accent-100 dark:text-accent-100' : 'text-secondary-300 dark:text-primary-300'}`} />
                    <span className={`mt-2 text-sm ${importType === id ? 'text-secondary-100 dark:text-primary-100' : 'text-secondary-300 dark:text-primary-300'}`}>{name}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Platform Selection */}
            <div>
              <label className="block text-sm font-medium text-secondary-100 dark:text-primary-100 mb-2">
                Platform
              </label>
              <div className="grid grid-cols-3 gap-2">
                {platforms.slice(0, 6).map((p) => (
                  <button
                    key={p.id}
                    type="button"
                    onClick={() => setPlatform(p.id)}
                    className={`p-2 border rounded-lg text-sm ${
                      platform === p.id
                        ? 'border-accent-100 bg-accent-50 text-secondary-100 dark:border-accent-200 dark:bg-accent-200/20 dark:text-primary-100'
                        : 'border-accent-100/30 text-secondary-300 hover:bg-primary-200 dark:border-accent-300/30 dark:text-primary-300 dark:hover:bg-secondary-200'
                    }`}
                  >
                    {p.name}
                  </button>
                ))}
              </div>
            </div>

            {/* Custom Platform Input */}
            {platform === 'other' && (
              <div>
                <label htmlFor="custom-platform" className="block text-sm font-medium text-secondary-100 dark:text-primary-100 mb-2">
                  Custom Platform Name
                </label>
                <input
                  type="text"
                  id="custom-platform"
                  value={customPlatform}
                  onChange={(e) => setCustomPlatform(e.target.value)}
                  className="w-full p-2 border border-accent-100/50 dark:border-accent-300/50 rounded-md bg-primary-50 dark:bg-secondary-200 text-secondary-100 dark:text-primary-100"
                  placeholder="Enter platform name"
                />
              </div>
            )}

            {/* URL Input */}
            {(importType === 'link' || importType === 'video') && (
              <div>
                <label htmlFor="url" className="block text-sm font-medium text-secondary-100 dark:text-primary-100 mb-2">
                  {importType === 'link' ? 'Chat URL' : 'Video/Podcast URL'}
                </label>
                <input
                  type="text"
                  id="url"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  className="w-full p-2 border border-accent-100/50 dark:border-accent-300/50 rounded-md bg-primary-50 dark:bg-secondary-200 text-secondary-100 dark:text-primary-100"
                  placeholder={importType === 'link' ? 'https://chat.openai.com/share/...' : 'https://youtube.com/...'}
                />
              </div>
            )}

            {/* File Input */}
            {importType === 'file' && (
              <div>
                <label htmlFor="file" className="block text-sm font-medium text-secondary-100 dark:text-primary-100 mb-2">
                  Chat Export File
                </label>
                <input
                  type="file"
                  id="file"
                  ref={fileInputRef}
                  className="w-full p-2 border border-accent-100/50 dark:border-accent-300/50 rounded-md bg-primary-50 dark:bg-secondary-200 text-secondary-100 dark:text-primary-100"
                  accept=".json,.txt,.html,.md"
                />
              </div>
            )}

            {/* Guest User Warning */}
            {isGuest && (
              <div className="p-3 bg-success-50 text-secondary-100 dark:bg-success-200/20 dark:text-primary-100 rounded-md text-sm">
                <p>
                  <strong>Guest Mode:</strong> {remainingImports} {remainingImports === 1 ? 'import' : 'imports'} remaining.
                </p>
                {isLimitReached && (
                  <p className="mt-1">
                    You've reached the guest import limit. <button className="text-accent-100 hover:underline" onClick={() => navigate('/signup')}>Create an account</button> for unlimited imports.
                  </p>
                )}
              </div>
            )}

            <div className="flex justify-end space-x-3 mt-6">
              {!standalone && (
                <button
                  type="button"
                  onClick={() => setIsOpen(false)}
                  className="px-4 py-2 border border-accent-100/50 dark:border-accent-300/50 rounded-md text-secondary-100 dark:text-primary-100 hover:bg-primary-200 dark:hover:bg-secondary-200"
                  disabled={isLoading}
                >
                  Cancel
                </button>
              )}
              <button
                type="button"
                onClick={handleImport}
                disabled={isLoading || isLimitReached}
                className="px-4 py-2 bg-success-100 hover:bg-success-200 text-secondary-100 dark:text-secondary-100 rounded-md disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isLoading ? 'Importing...' : 'Import Chat'}
              </button>
            </div>
          </div>
        </Card>
      </div>
    </Dialog>
  );

  return (
    <>
      {!standalone && renderImportButton()}
      {(isOpen || standalone) && renderImportDialog()}
    </>
  );
};

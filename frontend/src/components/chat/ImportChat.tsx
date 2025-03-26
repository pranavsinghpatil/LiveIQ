import { useState } from 'react';
import { Dialog } from '@headlessui/react';
import { DocumentIcon, VideoCameraIcon, MicrophoneIcon } from '@heroicons/react/24/outline';
import { api } from '../../utils/api';
import { Button } from '../ui/Button';
import { useAuthStore } from '../../store/auth';

interface ImportChatProps {
  isOpen?: boolean;
  onClose?: () => void;
  standalone?: boolean;
  onImportSuccess?: (data: any) => void;
}

export const ImportChat = ({ 
  isOpen: propIsOpen = false, 
  onClose = () => {}, 
  standalone = false,
  onImportSuccess 
}: ImportChatProps) => {
  const [localIsOpen, setLocalIsOpen] = useState(standalone);
  const [importType, setImportType] = useState<'link' | 'file' | 'video' | 'audio'>('link');
  const [platform, setPlatform] = useState('');
  const [customPlatform, setCustomPlatform] = useState('');
  const [linkUrl, setLinkUrl] = useState('');
  const [file, setFile] = useState<File | null>(null);
  const [transcript, setTranscript] = useState<File | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const { user } = useAuthStore();
  const hasReachedImportLimit = () => user?.role === 'guest' && (user?.remainingImports ?? 0) <= 0;

  const handleImport = async () => {
    if (isLoading) return;
    setError(null);
    setIsLoading(true);

    try {
      const formData = new FormData();

      if (importType !== 'file') {
        if (!platform) {
          throw new Error('Please select a platform');
        }
        formData.append('platform', platform === 'other' ? customPlatform.trim() : platform);
      }

      formData.append('type', importType);

      if (importType === 'link') {
        if (!linkUrl.trim()) {
          throw new Error('Please enter a valid URL');
        }
        formData.append('url', linkUrl.trim());
      } else {
        if (!file) {
          throw new Error('Please select a file');
        }
        formData.append('file', file);
      }

      if ((importType === 'video' || importType === 'audio') && transcript) {
        formData.append('transcript', transcript);
      }

      const response = await api.post('/chats/import', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      if (onImportSuccess) {
        onImportSuccess(response.data);
      }
      handleClose();
    } catch (err: any) {
      console.error('Import error:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to import chat');
    } finally {
      setIsLoading(false);
    }
  };

  const handleClose = () => {
    if (standalone) return;
    setLocalIsOpen(false);
    onClose();
  };

  const isOpen = standalone ? localIsOpen : propIsOpen;

  return (
    <>
      {!standalone && (
        <Button 
          onClick={() => setLocalIsOpen(true)}
          className="bg-gradient-to-r from-primary-600 to-primary-400 hover:from-primary-700 hover:to-primary-500 text-white shadow-lg"
        >
          Import Chat
        </Button>
      )}

      <Dialog 
        open={Boolean(isOpen)} 
        onClose={handleClose}
        className="relative z-50"
      >
        <div className="fixed inset-0 bg-gradient-to-br from-primary-900/60 to-primary-600/30 backdrop-blur-sm" aria-hidden="true" />
        
        <div className="fixed inset-0 flex items-center justify-center p-4">
          <Dialog.Panel className="w-full max-w-md rounded-xl shadow-2xl bg-gradient-to-b from-surface to-surface/95 p-6 border border-primary-200/20">
            <Dialog.Title className="text-2xl font-semibold mb-6 bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
              Import Chat
            </Dialog.Title>

            {error && (
              <div className="mb-6 p-4 rounded-lg bg-gradient-to-r from-red-500/10 to-red-600/5 border border-red-500/20">
                <span className="text-gradient-error">{error}</span>
              </div>
            )}

            <div className="space-y-6">
              <div>
                <label className="block text-sm font-medium mb-2 bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                  Import Type
                </label>
                <div className="grid grid-cols-2 gap-3">
                  {[
                    { id: 'link', name: 'Import URL', icon: DocumentIcon },
                    { id: 'file', name: 'Upload File', icon: DocumentIcon },
                    { id: 'video', name: 'Video', icon: VideoCameraIcon },
                    { id: 'audio', name: 'Audio', icon: MicrophoneIcon },
                  ].map(({ id, name, icon: Icon }) => (
                    <button
                      key={id}
                      type="button"
                      onClick={() => {
                        setImportType(id as any);
                        setError(null);
                      }}
                      className={`flex items-center justify-center p-4 rounded-lg border transition-all ${
                        importType === id
                          ? 'border-primary-400/30 bg-gradient-to-br from-primary-400/20 to-primary-600/10 text-gradient-primary'
                          : 'border-primary-200/20 hover:bg-gradient-to-br hover:from-primary-400/10 hover:to-primary-600/5 text-primary-300'
                      }`}
                    >
                      <Icon className="h-5 w-5 mr-2" />
                      <span>{name}</span>
                    </button>
                  ))}
                </div>
              </div>

              {importType !== 'file' && (
                <div>
                  <label className="block text-sm font-medium mb-2 bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                    Platform
                  </label>
                  <select
                    value={platform}
                    onChange={(e) => setPlatform(e.target.value)}
                    className="w-full p-3 bg-gradient-to-b from-white to-gray-50 border border-primary-200/30 rounded-lg text-primary-600 
                             focus:border-primary-400/50 focus:ring focus:ring-primary-400/20"
                  >
                    <option value="">Select Platform</option>
                    <option value="chatgpt">ChatGPT</option>
                    <option value="claude">Claude</option>
                    <option value="bard">Bard</option>
                    <option value="other">Other</option>
                  </select>
                </div>
              )}

              {platform === 'other' && (
                <div>
                  <label className="block text-sm font-medium mb-2 bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                    Custom Platform
                  </label>
                  <input
                    type="text"
                    value={customPlatform}
                    onChange={(e) => setCustomPlatform(e.target.value)}
                    className="w-full p-3 bg-gradient-to-b from-white to-gray-50 border border-primary-200/30 rounded-lg text-primary-600
                             focus:border-primary-400/50 focus:ring focus:ring-primary-400/20"
                    placeholder="Enter platform name"
                  />
                </div>
              )}

              {importType === 'link' && (
                <div>
                  <label className="block text-sm font-medium mb-2 bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                    URL
                  </label>
                  <input
                    type="url"
                    value={linkUrl}
                    onChange={(e) => setLinkUrl(e.target.value)}
                    className="w-full p-3 bg-gradient-to-b from-white to-gray-50 border border-primary-200/30 rounded-lg text-primary-600
                             focus:border-primary-400/50 focus:ring focus:ring-primary-400/20"
                    placeholder="Enter chat URL"
                  />
                </div>
              )}

              {(importType === 'file' || importType === 'video' || importType === 'audio') && (
                <div>
                  <label className="block text-sm font-medium mb-2 bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                    File
                  </label>
                  <input
                    type="file"
                    onChange={(e) => setFile(e.target.files?.[0] || null)}
                    className="w-full p-3 bg-gradient-to-b from-white to-gray-50 border border-primary-200/30 rounded-lg text-primary-600
                             file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0
                             file:bg-gradient-to-r file:from-primary-500 file:to-primary-600 file:text-white
                             hover:file:from-primary-600 hover:file:to-primary-700
                             focus:border-primary-400/50 focus:ring focus:ring-primary-400/20"
                    accept={importType === 'file' ? '.txt,.json,.md' : '.mp3,.mp4,.wav,.avi,.mov'}
                  />
                </div>
              )}

              {(importType === 'video' || importType === 'audio') && (
                <div>
                  <label className="block text-sm font-medium mb-2 bg-gradient-to-r from-primary-400 to-primary-600 bg-clip-text text-transparent">
                    Transcript (Optional)
                  </label>
                  <input
                    type="file"
                    onChange={(e) => setTranscript(e.target.files?.[0] || null)}
                    className="w-full p-3 bg-gradient-to-b from-white to-gray-50 border border-primary-200/30 rounded-lg text-primary-600
                             file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0
                             file:bg-gradient-to-r file:from-primary-500 file:to-primary-600 file:text-white
                             hover:file:from-primary-600 hover:file:to-primary-700
                             focus:border-primary-400/50 focus:ring focus:ring-primary-400/20"
                    accept=".txt,.srt,.vtt"
                  />
                </div>
              )}

              <div className="flex justify-end space-x-3 pt-6">
                <Button
                  variant="outline"
                  onClick={handleClose}
                  className="border-primary-200/30 bg-gradient-to-br from-surface to-surface/80 text-gradient-primary hover:bg-gradient-to-br hover:from-primary-50 hover:to-primary-100/30"
                >
                  Cancel
                </Button>
                <Button
                  onClick={handleImport}
                  disabled={isLoading}
                  className="bg-gradient-to-r from-primary-500 to-primary-600 text-white shadow-lg
                           hover:from-primary-600 hover:to-primary-700 disabled:opacity-50"
                >
                  {isLoading ? 'Importing...' : 'Import'}
                </Button>
              </div>
            </div>
          </Dialog.Panel>
        </div>
      </Dialog>
    </>
  );
};

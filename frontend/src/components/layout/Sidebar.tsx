import { useState } from 'react';
import { NavLink, useLocation, useNavigate } from 'react-router-dom';
import {
  HomeIcon,
  ChatBubbleLeftRightIcon,
  TagIcon,
  CogIcon,
  PlusIcon,
} from '@heroicons/react/24/outline';
import clsx from 'clsx';
import { ImportChat } from '../chat/ImportChat';

const navigation = [
  { name: 'Dashboard', href: '/', icon: HomeIcon },
  { name: 'Chats', href: '/chats', icon: ChatBubbleLeftRightIcon },
  { name: 'Tags', href: '/tags', icon: TagIcon },
  { name: 'Settings', href: '/settings', icon: CogIcon },
];

const platforms = [
  { id: 'chatgpt', name: 'ChatGPT', color: 'bg-accent-green' },
  { id: 'mistral', name: 'Mistral', color: 'bg-accent-blue' },
  { id: 'gemini', name: 'Gemini', color: 'bg-accent-mauve' },
  { id: 'claude', name: 'Claude', color: 'bg-accent-peach' },
];

export const Sidebar = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const [selectedPlatforms, setSelectedPlatforms] = useState<string[]>([]);

  const togglePlatform = (platformId: string) => {
    setSelectedPlatforms(prev =>
      prev.includes(platformId)
        ? prev.filter(id => id !== platformId)
        : [...prev, platformId]
    );
  };

  const createNewChat = () => {
    // This would typically call an API to create a new chat
    // For now, we'll just navigate to a placeholder URL
    navigate('/chats/new');
  };

  return (
    <div className="hidden md:flex md:flex-shrink-0">
      <div className="flex flex-col w-64">
        <div className="flex flex-col h-0 flex-1 border-r border-gray-200 dark:border-dark-100 bg-white dark:bg-dark-100 transition-colors duration-200">
          <div className="flex items-center justify-center h-16 flex-shrink-0 px-4 bg-primary-600 dark:bg-primary-800">
            <span className="text-xl font-bold text-white">ChatSynth</span>
          </div>
          <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
            <div className="px-4 mb-6">
              <button
                onClick={createNewChat}
                className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 dark:bg-primary-700 dark:hover:bg-primary-800 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors duration-150"
              >
                <PlusIcon className="h-5 w-5 mr-2" />
                New Chat
              </button>
            </div>
            
            <div className="px-4 mb-6">
              <ImportChat />
            </div>
            
            <nav className="mt-2 flex-1 px-2 space-y-1">
              {navigation.map((item) => (
                <NavLink
                  key={item.name}
                  to={item.href}
                  className={({ isActive }) =>
                    clsx(
                      isActive
                        ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400'
                        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-dark-300/50 hover:text-gray-900 dark:hover:text-gray-200',
                      'group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors duration-150'
                    )
                  }
                >
                  <item.icon
                    className={clsx(
                      location.pathname === item.href
                        ? 'text-primary-500 dark:text-primary-400'
                        : 'text-gray-400 dark:text-gray-500 group-hover:text-gray-500 dark:group-hover:text-gray-400',
                      'mr-3 flex-shrink-0 h-5 w-5 transition-colors duration-150'
                    )}
                    aria-hidden="true"
                  />
                  {item.name}
                </NavLink>
              ))}
            </nav>

            <div className="mt-6 px-3">
              <h3 className="px-2 text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider">
                Platforms
              </h3>
              <div className="mt-2 space-y-1">
                {platforms.map((platform) => (
                  <button
                    key={platform.id}
                    onClick={() => togglePlatform(platform.id)}
                    className={clsx(
                      'w-full flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors duration-150',
                      selectedPlatforms.includes(platform.id)
                        ? 'bg-gray-100 dark:bg-dark-300 text-gray-900 dark:text-gray-100'
                        : 'text-gray-600 dark:text-gray-400 hover:bg-gray-50 dark:hover:bg-dark-300/50 hover:text-gray-900 dark:hover:text-gray-200'
                    )}
                  >
                    <span className={`h-3 w-3 ${platform.color} rounded-full mr-2`} />
                    {platform.name}
                  </button>
                ))}
              </div>
            </div>
          </div>
          
          <div className="p-4 border-t border-gray-200 dark:border-dark-100">
            <div className="text-xs text-gray-500 dark:text-gray-400">
              <p>ChatSynth v1.0</p>
              <p className="mt-1"> 2025 ChatSynth</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

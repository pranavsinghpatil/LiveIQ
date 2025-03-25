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
  { id: 'chatgpt', name: 'ChatGPT', color: 'bg-success-100' },
  { id: 'mistral', name: 'Mistral', color: 'bg-accent-100' },
  { id: 'gemini', name: 'Gemini', color: 'bg-secondary-100' },
  { id: 'claude', name: 'Claude', color: 'bg-primary-200' },
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
        <div className="flex flex-col h-0 flex-1 border-r border-accent-100 dark:border-accent-300 bg-primary-100 dark:bg-secondary-100 transition-colors duration-200">
          <div className="flex items-center justify-center h-16 flex-shrink-0 px-4 bg-accent-100 dark:bg-accent-300">
            <span className="text-xl font-bold text-secondary-100 dark:text-primary-100">ChatSynth</span>
          </div>
          <div className="flex-1 flex flex-col pt-5 pb-4 overflow-y-auto">
            <div className="px-4 mb-6">
              <button
                onClick={createNewChat}
                className="w-full flex items-center justify-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-secondary-100 dark:text-primary-100 bg-success-100 hover:bg-success-200 dark:bg-success-200 dark:hover:bg-success-300 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-success-100 transition-colors duration-150"
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
                        ? 'bg-accent-50 dark:bg-accent-300/20 text-secondary-100 dark:text-primary-100'
                        : 'text-secondary-300 dark:text-primary-300 hover:bg-primary-200 dark:hover:bg-secondary-200 hover:text-secondary-100 dark:hover:text-primary-100',
                      'group flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors duration-150'
                    )
                  }
                >
                  <item.icon
                    className={clsx(
                      location.pathname === item.href
                        ? 'text-accent-100 dark:text-accent-100'
                        : 'text-secondary-300 dark:text-primary-300 group-hover:text-secondary-100 dark:group-hover:text-primary-100',
                      'mr-3 flex-shrink-0 h-5 w-5 transition-colors duration-150'
                    )}
                    aria-hidden="true"
                  />
                  {item.name}
                </NavLink>
              ))}
            </nav>

            <div className="mt-6 px-3">
              <h3 className="px-2 text-xs font-semibold text-secondary-300 dark:text-primary-300 uppercase tracking-wider">
                Platforms
              </h3>
              <div className="mt-2 space-y-1">
                {platforms.map((platform) => (
                  <button
                    key={platform.id}
                    onClick={() => togglePlatform(platform.id)}
                    className={clsx(
                      'flex items-center px-2 py-1.5 text-sm font-medium rounded-md w-full transition-colors duration-150',
                      selectedPlatforms.includes(platform.id)
                        ? 'bg-primary-200 dark:bg-secondary-200 text-secondary-100 dark:text-primary-100'
                        : 'text-secondary-300 dark:text-primary-300 hover:bg-primary-200 dark:hover:bg-secondary-200 hover:text-secondary-100 dark:hover:text-primary-100'
                    )}
                  >
                    <span
                      className={clsx(
                        'h-2.5 w-2.5 rounded-full mr-3',
                        platform.color
                      )}
                    ></span>
                    {platform.name}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

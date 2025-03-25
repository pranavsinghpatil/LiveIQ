import { Fragment } from 'react';
import { Menu, Transition } from '@headlessui/react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../../store/auth';
import { UserCircleIcon, MagnifyingGlassIcon } from '@heroicons/react/24/outline';
import { ThemeToggle } from '../ui/ThemeToggle';

export const Header = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <header className="bg-primary-100 dark:bg-secondary-100 shadow-sm transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
        <div className="flex items-center">
          <h1 className="text-2xl font-bold text-secondary-100 dark:text-primary-100">ChatSynth</h1>
        </div>
        
        <div className="flex-1 max-w-xl mx-8">
          <div className="relative rounded-md shadow-sm">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <MagnifyingGlassIcon className="h-5 w-5 text-secondary-300 dark:text-primary-300" aria-hidden="true" />
            </div>
            <input
              type="text"
              className="block w-full pl-10 pr-3 py-2 border border-accent-100 dark:border-accent-300 rounded-md leading-5 bg-primary-50 dark:bg-secondary-200 placeholder-secondary-400 dark:placeholder-primary-300 focus:outline-none focus:ring-2 focus:ring-accent-100 focus:border-accent-100 dark:focus:border-accent-100 text-secondary-100 dark:text-primary-100 transition-colors duration-200"
              placeholder="Search chats..."
            />
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <ThemeToggle />
          
          <Menu as="div" className="relative">
            <Menu.Button className="flex items-center space-x-2 text-secondary-100 dark:text-primary-100 hover:text-secondary-300 dark:hover:text-primary-300">
              <UserCircleIcon className="h-8 w-8" />
              <span>{user?.username}</span>
            </Menu.Button>
            
            <Transition
              as={Fragment}
              enter="transition ease-out duration-100"
              enterFrom="transform opacity-0 scale-95"
              enterTo="transform opacity-100 scale-100"
              leave="transition ease-in duration-75"
              leaveFrom="transform opacity-100 scale-100"
              leaveTo="transform opacity-0 scale-95"
            >
              <Menu.Items className="absolute right-0 mt-2 w-48 origin-top-right bg-primary-100 dark:bg-secondary-100 divide-y divide-accent-100 dark:divide-accent-300 rounded-md shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none">
                <div className="py-1">
                  <Menu.Item>
                    {({ active }) => (
                      <button
                        className={`${
                          active ? 'bg-accent-100 text-secondary-100 dark:bg-accent-300 dark:text-primary-100' : 'text-secondary-100 dark:text-primary-100'
                        } group flex items-center w-full px-4 py-2 text-sm`}
                        onClick={() => navigate('/profile')}
                      >
                        Profile
                      </button>
                    )}
                  </Menu.Item>
                  <Menu.Item>
                    {({ active }) => (
                      <button
                        className={`${
                          active ? 'bg-accent-100 text-secondary-100 dark:bg-accent-300 dark:text-primary-100' : 'text-secondary-100 dark:text-primary-100'
                        } group flex items-center w-full px-4 py-2 text-sm`}
                        onClick={handleLogout}
                      >
                        Logout
                      </button>
                    )}
                  </Menu.Item>
                </div>
              </Menu.Items>
            </Transition>
          </Menu>
        </div>
      </div>
    </header>
  );
};

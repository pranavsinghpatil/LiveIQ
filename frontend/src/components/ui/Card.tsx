import React from 'react';
import clsx from 'clsx';

type CardProps = {
  children: React.ReactNode;
  className?: string;
  hover?: boolean;
  bordered?: boolean;
  padding?: 'sm' | 'md' | 'lg';
  onClick?: () => void;
};

export const Card: React.FC<CardProps> = ({
  children,
  className = '',
  hover = false,
  bordered = false,
  padding = 'md',
  onClick
}) => {
  const paddingClass = {
    sm: 'p-2',
    md: 'p-4',
    lg: 'p-6'
  }[padding];

  return (
    <div
      className={clsx(
        'bg-white rounded-xl shadow-sm overflow-hidden',
        paddingClass,
        {
          'hover:shadow-md transition-all duration-200': hover,
          'border border-gray-200': bordered
        },
        className
      )}
      onClick={onClick}
      role={onClick ? 'button' : undefined}
    >
      {children}
    </div>
  );
};

export const CardHeader: React.FC<{ children: React.ReactNode; className?: string }> = ({ 
  children, 
  className = '' 
}) => {
  return (
    <div className={`mb-4 ${className}`}>
      {children}
    </div>
  );
};

export const CardTitle: React.FC<{ children: React.ReactNode; className?: string }> = ({ 
  children, 
  className = '' 
}) => {
  return (
    <h3 className={`text-lg font-semibold text-gray-900 ${className}`}>
      {children}
    </h3>
  );
};

export const CardDescription: React.FC<{ children: React.ReactNode; className?: string }> = ({ 
  children, 
  className = '' 
}) => {
  return (
    <p className={`text-sm text-gray-500 ${className}`}>
      {children}
    </p>
  );
};

export const CardContent: React.FC<{ children: React.ReactNode; className?: string }> = ({ 
  children, 
  className = '' 
}) => {
  return (
    <div className={className}>
      {children}
    </div>
  );
};

export const CardFooter: React.FC<{ children: React.ReactNode; className?: string }> = ({ 
  children, 
  className = '' 
}) => {
  return (
    <div className={`mt-4 flex items-center ${className}`}>
      {children}
    </div>
  );
};

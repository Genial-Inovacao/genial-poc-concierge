import React from 'react';
import { ExclamationTriangleIcon } from '@heroicons/react/24/outline';

const ErrorMessage = ({ title, message, onRetry }) => {
  return (
    <div className="rounded-md bg-red-50 p-4">
      <div className="flex">
        <div className="flex-shrink-0">
          <ExclamationTriangleIcon className="h-5 w-5 text-red-400" aria-hidden="true" />
        </div>
        <div className="ml-3">
          <h3 className="text-sm font-medium text-red-800">
            {title || 'Erro'}
          </h3>
          <div className="mt-2 text-sm text-red-700">
            <p>{message || 'Ocorreu um erro inesperado.'}</p>
          </div>
          {onRetry && (
            <div className="mt-4">
              <button
                type="button"
                onClick={onRetry}
                className="text-sm font-medium text-red-800 hover:text-red-700"
              >
                Tentar novamente
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ErrorMessage;
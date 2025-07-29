import React, { useState } from 'react';
import { useApp } from '../../store/AppContext';
import { 
  CheckIcon, 
  XMarkIcon, 
  ClockIcon,
  CurrencyDollarIcon,
  HeartIcon,
  BriefcaseIcon,
  HomeIcon,
  UserGroupIcon,
  SparklesIcon
} from '@heroicons/react/24/outline';

const SuggestionCard = ({ suggestion }) => {
  const { handleSuggestionAction } = useApp();
  const [loading, setLoading] = useState(false);
  const [showPostponeModal, setShowPostponeModal] = useState(false);
  const [postponeDate, setPostponeDate] = useState('');

  const categoryIcons = {
    finance: CurrencyDollarIcon,
    health: HeartIcon,
    productivity: BriefcaseIcon,
    lifestyle: HomeIcon,
    relationships: UserGroupIcon,
    default: SparklesIcon,
  };

  const categoryColors = {
    finance: 'text-green-600 bg-green-100',
    health: 'text-red-600 bg-red-100',
    productivity: 'text-blue-600 bg-blue-100',
    lifestyle: 'text-purple-600 bg-purple-100',
    relationships: 'text-pink-600 bg-pink-100',
    default: 'text-gray-600 bg-gray-100',
  };

  const getPriorityLabel = (priority) => {
    if (priority <= 3) return { text: 'Baixa', class: 'bg-gray-100 text-gray-800' };
    if (priority <= 7) return { text: 'Média', class: 'bg-yellow-100 text-yellow-800' };
    return { text: 'Alta', class: 'bg-red-100 text-red-800' };
  };

  const suggestionTypeLabels = {
    anniversary: 'Aniversário',
    purchase: 'Compra',
    routine: 'Rotina',
    seasonal: 'Sazonal',
    savings: 'Economia',
    reminder: 'Lembrete',
    recommendation: 'Recomendação',
  };

  const Icon = categoryIcons[suggestion.category] || categoryIcons.default;
  const colorClass = categoryColors[suggestion.category] || categoryColors.default;
  const priorityLabel = getPriorityLabel(suggestion.priority);

  const handleAction = async (action, data = {}) => {
    setLoading(true);
    try {
      const result = await handleSuggestionAction(suggestion.id, action, data);
      if (!result.success) {
        // Mostrar erro ao usuário
        console.error('Ação falhou:', result.error);
      }
    } finally {
      setLoading(false);
      setShowPostponeModal(false);
    }
  };

  const handlePostpone = () => {
    if (!postponeDate) return;
    handleAction('postpone', { postponeUntil: postponeDate });
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR', {
      day: 'numeric',
      month: 'short',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  return (
    <>
      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6 hover:shadow-md transition-shadow duration-200">
        <div className="flex items-start space-x-4">
          <div className={`flex-shrink-0 p-3 rounded-lg ${colorClass}`}>
            <Icon className="h-6 w-6" />
          </div>
          
          <div className="flex-1 min-w-0">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="text-lg font-semibold text-gray-900">
                  {suggestionTypeLabels[suggestion.type.toLowerCase()] || suggestion.type}
                </h3>
                <p className="mt-1 text-sm text-gray-500">
                  {formatDate(suggestion.scheduled_date)}
                </p>
              </div>
              <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${priorityLabel.class}`}>
                {priorityLabel.text}
              </span>
            </div>
            
            <p className="mt-3 text-gray-600">
              {suggestion.content}
            </p>

            {suggestion.metadata?.estimated_savings && (
              <div className="mt-3 flex items-center text-sm text-green-600">
                <CurrencyDollarIcon className="h-4 w-4 mr-1" />
                Economia estimada: R$ {suggestion.metadata.estimated_savings.toFixed(2)}
              </div>
            )}

            <div className="mt-4 flex space-x-2">
              <button
                onClick={() => handleAction('accept')}
                disabled={loading || suggestion.status !== 'pending'}
                className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <CheckIcon className="h-4 w-4 mr-1" />
                Aceitar
              </button>
              
              <button
                onClick={() => handleAction('reject')}
                disabled={loading || suggestion.status !== 'pending'}
                className="inline-flex items-center px-3 py-1.5 border border-transparent text-xs font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <XMarkIcon className="h-4 w-4 mr-1" />
                Rejeitar
              </button>
              
              <button
                onClick={() => setShowPostponeModal(true)}
                disabled={loading || suggestion.status !== 'pending'}
                className="inline-flex items-center px-3 py-1.5 border border-gray-300 text-xs font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <ClockIcon className="h-4 w-4 mr-1" />
                Adiar
              </button>
            </div>

            {suggestion.status !== 'pending' && (
              <div className="mt-3">
                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                  suggestion.status === 'accepted' ? 'bg-green-100 text-green-800' :
                  suggestion.status === 'rejected' ? 'bg-red-100 text-red-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {suggestion.status === 'accepted' ? 'Aceita' :
                   suggestion.status === 'rejected' ? 'Rejeitada' :
                   'Adiada'}
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Modal de Adiar */}
      {showPostponeModal && (
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <h3 className="text-lg font-medium text-gray-900 mb-4">
              Adiar Sugestão
            </h3>
            <p className="text-sm text-gray-500 mb-4">
              Escolha quando você gostaria de receber esta sugestão novamente.
            </p>
            
            <input
              type="datetime-local"
              value={postponeDate}
              onChange={(e) => setPostponeDate(e.target.value)}
              min={new Date().toISOString().slice(0, 16)}
              className="block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
            />
            
            <div className="mt-6 flex justify-end space-x-3">
              <button
                onClick={() => setShowPostponeModal(false)}
                className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Cancelar
              </button>
              <button
                onClick={handlePostpone}
                disabled={!postponeDate || loading}
                className="px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Confirmar
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};

export default SuggestionCard;
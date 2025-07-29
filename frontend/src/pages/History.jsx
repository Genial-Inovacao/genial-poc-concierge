import React, { useState, useEffect } from 'react';
import analyticsService from '../services/analytics';
import { 
  CalendarIcon, 
  ChartBarIcon,
  CheckCircleIcon,
  XCircleIcon,
  ClockIcon,
  FunnelIcon 
} from '@heroicons/react/24/outline';

const History = () => {
  const [activities, setActivities] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({
    dateRange: 'week',
    type: 'all',
    status: 'all',
  });
  const [activeTab, setActiveTab] = useState('activities');

  useEffect(() => {
    loadData();
  }, [filters, activeTab]);

  const loadData = async () => {
    setLoading(true);
    try {
      if (activeTab === 'activities') {
        const params = {
          date_range: filters.dateRange,
          status: filters.status !== 'all' ? filters.status : undefined,
        };
        const data = await analyticsService.getActivityHistory(params);
        setActivities(data.activities || []);
      } else {
        const params = {
          date_range: filters.dateRange,
          type: filters.type !== 'all' ? filters.type : undefined,
        };
        const data = await analyticsService.getTransactions(params);
        setTransactions(data.transactions || []);
      }
    } catch (err) {
      console.error('Erro ao carregar dados:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({ ...prev, [filterType]: value }));
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR', {
      day: 'numeric',
      month: 'long',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    }).format(date);
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case 'accepted':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />;
      case 'rejected':
        return <XCircleIcon className="h-5 w-5 text-red-500" />;
      case 'postponed':
        return <ClockIcon className="h-5 w-5 text-yellow-500" />;
      default:
        return <ClockIcon className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusLabel = (status) => {
    const labels = {
      accepted: 'Aceita',
      rejected: 'Rejeitada',
      postponed: 'Adiada',
      pending: 'Pendente',
    };
    return labels[status] || status;
  };

  const getCategoryLabel = (category) => {
    const labels = {
      finance: 'Finanças',
      health: 'Saúde',
      productivity: 'Produtividade',
      lifestyle: 'Estilo de Vida',
      relationships: 'Relacionamentos',
    };
    return labels[category] || category;
  };

  return (
    <div className="max-w-7xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="mb-8">
        <h1 className="text-2xl font-bold text-gray-900">Histórico</h1>
        <p className="mt-1 text-sm text-gray-500">
          Acompanhe todas as suas interações e transações
        </p>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <nav className="-mb-px flex space-x-8" aria-label="Tabs">
          <button
            onClick={() => setActiveTab('activities')}
            className={`whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'activities'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Atividades
          </button>
          <button
            onClick={() => setActiveTab('transactions')}
            className={`whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm ${
              activeTab === 'transactions'
                ? 'border-primary-500 text-primary-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            }`}
          >
            Transações
          </button>
        </nav>
      </div>

      {/* Filtros */}
      <div className="bg-white shadow rounded-lg p-4 mb-6">
        <div className="flex flex-wrap gap-4">
          <div className="flex items-center space-x-2">
            <CalendarIcon className="h-5 w-5 text-gray-400" />
            <label className="text-sm font-medium text-gray-700">Período:</label>
            <select
              value={filters.dateRange}
              onChange={(e) => handleFilterChange('dateRange', e.target.value)}
              className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
            >
              <option value="today">Hoje</option>
              <option value="week">Última Semana</option>
              <option value="month">Último Mês</option>
              <option value="year">Último Ano</option>
            </select>
          </div>

          {activeTab === 'activities' ? (
            <div className="flex items-center space-x-2">
              <FunnelIcon className="h-5 w-5 text-gray-400" />
              <label className="text-sm font-medium text-gray-700">Status:</label>
              <select
                value={filters.status}
                onChange={(e) => handleFilterChange('status', e.target.value)}
                className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
              >
                <option value="all">Todos</option>
                <option value="accepted">Aceitas</option>
                <option value="rejected">Rejeitadas</option>
                <option value="postponed">Adiadas</option>
              </select>
            </div>
          ) : (
            <div className="flex items-center space-x-2">
              <FunnelIcon className="h-5 w-5 text-gray-400" />
              <label className="text-sm font-medium text-gray-700">Tipo:</label>
              <select
                value={filters.type}
                onChange={(e) => handleFilterChange('type', e.target.value)}
                className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
              >
                <option value="all">Todos</option>
                <option value="savings">Economia</option>
                <option value="expense">Despesa</option>
                <option value="reminder">Lembrete</option>
              </select>
            </div>
          )}
        </div>
      </div>

      {/* Lista de Atividades/Transações */}
      {loading ? (
        <div className="flex justify-center py-12">
          <div className="text-center">
            <div className="inline-flex items-center justify-center w-16 h-16 mb-4">
              <svg
                className="animate-spin h-8 w-8 text-primary-600"
                xmlns="http://www.w3.org/2000/svg"
                fill="none"
                viewBox="0 0 24 24"
              >
                <circle
                  className="opacity-25"
                  cx="12"
                  cy="12"
                  r="10"
                  stroke="currentColor"
                  strokeWidth="4"
                ></circle>
                <path
                  className="opacity-75"
                  fill="currentColor"
                  d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                ></path>
              </svg>
            </div>
            <p className="text-gray-600">Carregando...</p>
          </div>
        </div>
      ) : activeTab === 'activities' ? (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          {activities.length === 0 ? (
            <div className="text-center py-12">
              <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                Nenhuma atividade encontrada
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Suas atividades aparecerão aqui quando você interagir com sugestões.
              </p>
            </div>
          ) : (
            <ul className="divide-y divide-gray-200">
              {activities.map((activity) => (
                <li key={activity.id}>
                  <div className="px-4 py-4 sm:px-6">
                    <div className="flex items-center justify-between">
                      <div className="flex items-center">
                        {getStatusIcon(activity.status)}
                        <div className="ml-4">
                          <p className="text-sm font-medium text-gray-900">
                            {activity.suggestion?.title}
                          </p>
                          <p className="text-sm text-gray-500">
                            {getCategoryLabel(activity.suggestion?.category)} • {formatDate(activity.created_at)}
                          </p>
                        </div>
                      </div>
                      <div className="flex items-center">
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                          activity.status === 'accepted' ? 'bg-green-100 text-green-800' :
                          activity.status === 'rejected' ? 'bg-red-100 text-red-800' :
                          activity.status === 'postponed' ? 'bg-yellow-100 text-yellow-800' :
                          'bg-gray-100 text-gray-800'
                        }`}>
                          {getStatusLabel(activity.status)}
                        </span>
                        {activity.suggestion?.metadata?.estimated_savings && (
                          <span className="ml-2 text-sm text-green-600">
                            +R$ {activity.suggestion.metadata.estimated_savings.toFixed(2)}
                          </span>
                        )}
                      </div>
                    </div>
                    {activity.suggestion?.description && (
                      <p className="mt-2 text-sm text-gray-600">
                        {activity.suggestion.description}
                      </p>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      ) : (
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          {transactions.length === 0 ? (
            <div className="text-center py-12">
              <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                Nenhuma transação encontrada
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Suas transações aparecerão aqui quando você completar ações.
              </p>
            </div>
          ) : (
            <ul className="divide-y divide-gray-200">
              {transactions.map((transaction) => (
                <li key={transaction.id}>
                  <div className="px-4 py-4 sm:px-6">
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-gray-900">
                          {transaction.description}
                        </p>
                        <p className="text-sm text-gray-500">
                          {formatDate(transaction.created_at)}
                        </p>
                      </div>
                      <div className="text-right">
                        <p className={`text-sm font-medium ${
                          transaction.type === 'savings' ? 'text-green-600' : 
                          transaction.type === 'expense' ? 'text-red-600' : 
                          'text-gray-900'
                        }`}>
                          {transaction.type === 'savings' ? '+' : 
                           transaction.type === 'expense' ? '-' : ''}
                          R$ {transaction.amount?.toFixed(2) || '0,00'}
                        </p>
                        <p className="text-xs text-gray-500">
                          {transaction.type === 'savings' ? 'Economia' :
                           transaction.type === 'expense' ? 'Despesa' :
                           'Lembrete'}
                        </p>
                      </div>
                    </div>
                  </div>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
};

export default History;
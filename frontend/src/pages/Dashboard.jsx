import React, { useEffect } from 'react';
import { useAuth } from '../store/AuthContext';
import { useApp } from '../store/AppContext';
import SuggestionCard from '../components/suggestions/SuggestionCard';
import StatsWidget from '../components/dashboard/StatsWidget';
import { 
  CalendarIcon, 
  ChartBarIcon, 
  CheckCircleIcon,
  ClockIcon,
  FunnelIcon,
  SparklesIcon 
} from '@heroicons/react/24/outline';

const Dashboard = () => {
  const { user } = useAuth();
  const { suggestions, stats, loading, filters, updateFilters, loadSuggestions } = useApp();

  useEffect(() => {
    loadSuggestions();
  }, []);

  const handleFilterChange = (filterType, value) => {
    updateFilters({ [filterType]: value });
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Bom dia';
    if (hour < 18) return 'Boa tarde';
    return 'Boa noite';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="py-4 md:flex md:items-center md:justify-between">
            <div className="flex-1 min-w-0">
              <h1 className="text-2xl font-bold text-gray-900">
                {getGreeting()}, {user?.profile?.name?.split(' ')[0] || user?.username}!
              </h1>
              <p className="mt-1 text-sm text-gray-500">
                Aqui estão suas sugestões personalizadas para hoje
              </p>
            </div>
            <div className="mt-4 flex md:mt-0 md:ml-4">
              <button
                type="button"
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <FunnelIcon className="-ml-1 mr-2 h-5 w-5 text-gray-400" />
                Filtros
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Estatísticas */}
        <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
          <StatsWidget
            title="Dias Ativo"
            value={stats?.days_active || 0}
            icon={CalendarIcon}
            color="bg-primary-500"
          />
          <StatsWidget
            title="Ações Executadas"
            value={stats?.total_actions || 0}
            icon={CheckCircleIcon}
            color="bg-green-500"
          />
          <StatsWidget
            title="Taxa de Aceitação"
            value={`${stats?.acceptance_rate || 0}%`}
            icon={ChartBarIcon}
            color="bg-blue-500"
          />
          <StatsWidget
            title="Economia Gerada"
            value={`R$ ${stats?.total_savings?.toFixed(2) || '0,00'}`}
            icon={SparklesIcon}
            color="bg-purple-500"
          />
        </div>

        {/* Filtros */}
        <div className="bg-white shadow rounded-lg p-4 mb-6">
          <div className="flex flex-wrap gap-4">
            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium text-gray-700">Status:</label>
              <select
                value={filters.status}
                onChange={(e) => handleFilterChange('status', e.target.value)}
                className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
              >
                <option value="pending">Pendentes</option>
                <option value="accepted">Aceitas</option>
                <option value="rejected">Rejeitadas</option>
                <option value="all">Todas</option>
              </select>
            </div>

            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium text-gray-700">Categoria:</label>
              <select
                value={filters.category}
                onChange={(e) => handleFilterChange('category', e.target.value)}
                className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
              >
                <option value="all">Todas</option>
                <option value="finance">Finanças</option>
                <option value="health">Saúde</option>
                <option value="productivity">Produtividade</option>
                <option value="lifestyle">Estilo de Vida</option>
                <option value="relationships">Relacionamentos</option>
              </select>
            </div>

            <div className="flex items-center space-x-2">
              <label className="text-sm font-medium text-gray-700">Período:</label>
              <select
                value={filters.dateRange}
                onChange={(e) => handleFilterChange('dateRange', e.target.value)}
                className="block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md"
              >
                <option value="today">Hoje</option>
                <option value="week">Esta Semana</option>
                <option value="month">Este Mês</option>
                <option value="all">Todas</option>
              </select>
            </div>
          </div>
        </div>

        {/* Lista de Sugestões */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">
            Suas Sugestões
          </h2>

          {loading.suggestions ? (
            <div className="flex justify-center py-12">
              <div className="text-center">
                <ClockIcon className="mx-auto h-12 w-12 text-gray-400 animate-pulse" />
                <p className="mt-2 text-sm text-gray-500">Carregando sugestões...</p>
              </div>
            </div>
          ) : suggestions.length === 0 ? (
            <div className="text-center py-12 bg-white rounded-lg shadow">
              <SparklesIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">
                Nenhuma sugestão encontrada
              </h3>
              <p className="mt-1 text-sm text-gray-500">
                Tente ajustar os filtros ou volte mais tarde para novas sugestões.
              </p>
            </div>
          ) : (
            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
              {suggestions.map((suggestion) => (
                <SuggestionCard key={suggestion.id} suggestion={suggestion} />
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
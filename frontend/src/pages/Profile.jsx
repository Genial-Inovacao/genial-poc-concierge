import React, { useState, useEffect } from 'react';
import { useAuth } from '../store/AuthContext';
import userService from '../services/user';
import { UserIcon, CameraIcon } from '@heroicons/react/24/outline';

const Profile = () => {
  const { user, updateUser } = useAuth();
  const [loading, setLoading] = useState(false);
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    phone: '',
    birth_date: '',
    spouse_name: '',
    spouse_birth_date: '',
    notification_preferences: {
      email: true,
      push: false,
      sms: false,
    },
    categories_of_interest: [],
    preferred_times: {
      morning: false,
      afternoon: false,
      evening: false,
      night: false,
    },
    daily_suggestion_limit: 5,
  });
  const [errors, setErrors] = useState({});
  const [successMessage, setSuccessMessage] = useState('');

  useEffect(() => {
    if (user) {
      setFormData({
        name: user.profile?.name || '',
        email: user.email || '',
        phone: user.profile?.phone || '',
        birth_date: user.profile?.birth_date || '',
        spouse_name: user.profile?.spouse_name || '',
        spouse_birth_date: user.profile?.spouse_birth_date || '',
        notification_preferences: user.profile?.preferences_json?.notifications || {
          email: true,
          push: false,
          sms: false,
        },
        categories_of_interest: user.profile?.preferences_json?.categories_of_interest || [],
        preferred_times: user.profile?.preferences_json?.preferred_times || {
          morning: false,
          afternoon: false,
          evening: false,
          night: false,
        },
        daily_suggestion_limit: user.profile?.preferences_json?.max_daily_suggestions || 5,
      });
    }
  }, [user]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    
    if (name.includes('.')) {
      const [parent, child] = name.split('.');
      setFormData(prev => ({
        ...prev,
        [parent]: {
          ...prev[parent],
          [child]: type === 'checkbox' ? checked : value,
        },
      }));
    } else {
      setFormData(prev => ({
        ...prev,
        [name]: type === 'checkbox' ? checked : value,
      }));
    }
  };

  const handleCategoryChange = (category) => {
    setFormData(prev => ({
      ...prev,
      categories_of_interest: prev.categories_of_interest.includes(category)
        ? prev.categories_of_interest.filter(c => c !== category)
        : [...prev.categories_of_interest, category],
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setErrors({});
    setSuccessMessage('');

    try {
      const profileData = {
        name: formData.name,
        phone: formData.phone,
        birth_date: formData.birth_date,
        spouse_name: formData.spouse_name,
        spouse_birth_date: formData.spouse_birth_date,
      };

      const preferencesData = {
        notifications: formData.notification_preferences,
        categories_of_interest: formData.categories_of_interest,
        preferred_times: formData.preferred_times,
        max_daily_suggestions: formData.daily_suggestion_limit,
      };

      await userService.updateProfile(profileData);
      await userService.updatePreferences(preferencesData);
      
      // Atualizar contexto
      const updatedUser = await userService.getProfile();
      updateUser(updatedUser);
      
      setSuccessMessage('Perfil atualizado com sucesso!');
    } catch (err) {
      setErrors({ general: 'Erro ao atualizar perfil' });
    } finally {
      setLoading(false);
    }
  };

  const handleAvatarChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    try {
      await userService.uploadAvatar(file);
      const updatedUser = await userService.getProfile();
      updateUser(updatedUser);
    } catch (err) {
      console.error('Erro ao fazer upload da foto:', err);
    }
  };

  const categories = [
    { id: 'finance', label: 'Finanças' },
    { id: 'health', label: 'Saúde' },
    { id: 'productivity', label: 'Produtividade' },
    { id: 'lifestyle', label: 'Estilo de Vida' },
    { id: 'relationships', label: 'Relacionamentos' },
  ];

  return (
    <div className="max-w-4xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
      <div className="md:grid md:grid-cols-3 md:gap-6">
        <div className="md:col-span-1">
          <h3 className="text-lg font-medium leading-6 text-gray-900">
            Informações Pessoais
          </h3>
          <p className="mt-1 text-sm text-gray-600">
            Atualize suas informações pessoais e preferências
          </p>
        </div>

        <div className="mt-5 md:mt-0 md:col-span-2">
          <form onSubmit={handleSubmit}>
            <div className="shadow sm:rounded-md sm:overflow-hidden">
              <div className="px-4 py-5 bg-white space-y-6 sm:p-6">
                {errors.general && (
                  <div className="rounded-md bg-red-50 p-4">
                    <p className="text-sm text-red-800">{errors.general}</p>
                  </div>
                )}

                {successMessage && (
                  <div className="rounded-md bg-green-50 p-4">
                    <p className="text-sm text-green-800">{successMessage}</p>
                  </div>
                )}

                {/* Avatar */}
                <div>
                  <label className="block text-sm font-medium text-gray-700">
                    Foto de Perfil
                  </label>
                  <div className="mt-2 flex items-center">
                    <span className="inline-block h-20 w-20 rounded-full overflow-hidden bg-gray-100">
                      {user?.avatar_url ? (
                        <img
                          src={user.avatar_url}
                          alt="Avatar"
                          className="h-full w-full object-cover"
                        />
                      ) : (
                        <UserIcon className="h-full w-full text-gray-300" />
                      )}
                    </span>
                    <label
                      htmlFor="avatar-upload"
                      className="ml-5 bg-white py-2 px-3 border border-gray-300 rounded-md shadow-sm text-sm leading-4 font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 cursor-pointer"
                    >
                      <CameraIcon className="h-5 w-5 inline-block mr-2" />
                      Alterar
                      <input
                        id="avatar-upload"
                        name="avatar"
                        type="file"
                        accept="image/*"
                        className="sr-only"
                        onChange={handleAvatarChange}
                      />
                    </label>
                  </div>
                </div>

                {/* Dados Básicos */}
                <div className="grid grid-cols-6 gap-6">
                  <div className="col-span-6 sm:col-span-3">
                    <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                      Nome Completo
                    </label>
                    <input
                      type="text"
                      name="name"
                      id="name"
                      value={formData.name}
                      onChange={handleChange}
                      className="mt-1 focus:ring-primary-500 focus:border-primary-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    />
                  </div>

                  <div className="col-span-6 sm:col-span-3">
                    <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                      Email
                    </label>
                    <input
                      type="email"
                      name="email"
                      id="email"
                      value={formData.email}
                      disabled
                      className="mt-1 bg-gray-50 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    />
                  </div>

                  <div className="col-span-6 sm:col-span-3">
                    <label htmlFor="phone" className="block text-sm font-medium text-gray-700">
                      Telefone
                    </label>
                    <input
                      type="tel"
                      name="phone"
                      id="phone"
                      value={formData.phone}
                      onChange={handleChange}
                      className="mt-1 focus:ring-primary-500 focus:border-primary-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    />
                  </div>

                  <div className="col-span-6 sm:col-span-3">
                    <label htmlFor="birth_date" className="block text-sm font-medium text-gray-700">
                      Data de Nascimento
                    </label>
                    <input
                      type="date"
                      name="birth_date"
                      id="birth_date"
                      value={formData.birth_date}
                      onChange={handleChange}
                      className="mt-1 focus:ring-primary-500 focus:border-primary-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                    />
                  </div>
                </div>

                {/* Dados do Cônjuge */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900">
                    Informações do Cônjuge (Opcional)
                  </h4>
                  <div className="mt-4 grid grid-cols-6 gap-6">
                    <div className="col-span-6 sm:col-span-3">
                      <label htmlFor="spouse_name" className="block text-sm font-medium text-gray-700">
                        Nome do Cônjuge
                      </label>
                      <input
                        type="text"
                        name="spouse_name"
                        id="spouse_name"
                        value={formData.spouse_name}
                        onChange={handleChange}
                        className="mt-1 focus:ring-primary-500 focus:border-primary-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                      />
                    </div>

                    <div className="col-span-6 sm:col-span-3">
                      <label htmlFor="spouse_birth_date" className="block text-sm font-medium text-gray-700">
                        Data de Nascimento do Cônjuge
                      </label>
                      <input
                        type="date"
                        name="spouse_birth_date"
                        id="spouse_birth_date"
                        value={formData.spouse_birth_date}
                        onChange={handleChange}
                        className="mt-1 focus:ring-primary-500 focus:border-primary-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                      />
                    </div>
                  </div>
                </div>

                {/* Preferências de Notificação */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900">
                    Preferências de Notificação
                  </h4>
                  <div className="mt-4 space-y-4">
                    <div className="flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="notification_email"
                          name="notification_preferences.email"
                          type="checkbox"
                          checked={formData.notification_preferences.email}
                          onChange={handleChange}
                          className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="notification_email" className="font-medium text-gray-700">
                          Email
                        </label>
                        <p className="text-gray-500">Receba sugestões por email</p>
                      </div>
                    </div>

                    <div className="flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="notification_push"
                          name="notification_preferences.push"
                          type="checkbox"
                          checked={formData.notification_preferences.push}
                          onChange={handleChange}
                          className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="notification_push" className="font-medium text-gray-700">
                          Push
                        </label>
                        <p className="text-gray-500">Notificações push no navegador</p>
                      </div>
                    </div>

                    <div className="flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="notification_sms"
                          name="notification_preferences.sms"
                          type="checkbox"
                          checked={formData.notification_preferences.sms}
                          onChange={handleChange}
                          className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="notification_sms" className="font-medium text-gray-700">
                          SMS
                        </label>
                        <p className="text-gray-500">Mensagens de texto</p>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Categorias de Interesse */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900">
                    Categorias de Interesse
                  </h4>
                  <div className="mt-4 space-y-2">
                    {categories.map((category) => (
                      <div key={category.id} className="flex items-start">
                        <div className="flex items-center h-5">
                          <input
                            id={`category_${category.id}`}
                            type="checkbox"
                            checked={formData.categories_of_interest.includes(category.id)}
                            onChange={() => handleCategoryChange(category.id)}
                            className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                          />
                        </div>
                        <div className="ml-3 text-sm">
                          <label htmlFor={`category_${category.id}`} className="font-medium text-gray-700">
                            {category.label}
                          </label>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Horários Preferenciais */}
                <div>
                  <h4 className="text-sm font-medium text-gray-900">
                    Horários Preferenciais para Sugestões
                  </h4>
                  <div className="mt-4 grid grid-cols-2 gap-4">
                    <div className="flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="time_morning"
                          name="preferred_times.morning"
                          type="checkbox"
                          checked={formData.preferred_times.morning}
                          onChange={handleChange}
                          className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="time_morning" className="font-medium text-gray-700">
                          Manhã (6h - 12h)
                        </label>
                      </div>
                    </div>

                    <div className="flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="time_afternoon"
                          name="preferred_times.afternoon"
                          type="checkbox"
                          checked={formData.preferred_times.afternoon}
                          onChange={handleChange}
                          className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="time_afternoon" className="font-medium text-gray-700">
                          Tarde (12h - 18h)
                        </label>
                      </div>
                    </div>

                    <div className="flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="time_evening"
                          name="preferred_times.evening"
                          type="checkbox"
                          checked={formData.preferred_times.evening}
                          onChange={handleChange}
                          className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="time_evening" className="font-medium text-gray-700">
                          Noite (18h - 22h)
                        </label>
                      </div>
                    </div>

                    <div className="flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="time_night"
                          name="preferred_times.night"
                          type="checkbox"
                          checked={formData.preferred_times.night}
                          onChange={handleChange}
                          className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="time_night" className="font-medium text-gray-700">
                          Madrugada (22h - 6h)
                        </label>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Limite de Sugestões */}
                <div>
                  <label htmlFor="daily_suggestion_limit" className="block text-sm font-medium text-gray-700">
                    Limite Diário de Sugestões
                  </label>
                  <input
                    type="number"
                    name="daily_suggestion_limit"
                    id="daily_suggestion_limit"
                    min="1"
                    max="20"
                    value={formData.daily_suggestion_limit}
                    onChange={handleChange}
                    className="mt-1 focus:ring-primary-500 focus:border-primary-500 block w-24 shadow-sm sm:text-sm border-gray-300 rounded-md"
                  />
                  <p className="mt-1 text-sm text-gray-500">
                    Número máximo de sugestões que você deseja receber por dia
                  </p>
                </div>
              </div>

              <div className="px-4 py-3 bg-gray-50 text-right sm:px-6">
                <button
                  type="submit"
                  disabled={loading}
                  className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Salvando...' : 'Salvar Alterações'}
                </button>
              </div>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Profile;
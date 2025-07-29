import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../store/AuthContext';
import { EnvelopeIcon, LockClosedIcon, UserIcon } from '@heroicons/react/24/outline';

const Register = () => {
  const navigate = useNavigate();
  const { register } = useAuth();
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    confirmPassword: '',
    acceptTerms: false,
  });
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
    // Clear error when user types
    if (errors[name]) {
      setErrors(prev => ({ ...prev, [name]: '' }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    // Validação do nome (username)
    if (!formData.name) {
      newErrors.name = 'Nome é obrigatório';
    } else if (formData.name.length < 3 || formData.name.length > 20) {
      newErrors.name = 'Nome deve ter entre 3 e 20 caracteres';
    } else if (!/^[a-zA-Z]/.test(formData.name)) {
      newErrors.name = 'Nome deve começar com uma letra';
    } else if (!/^[a-zA-Z0-9_]+$/.test(formData.name)) {
      newErrors.name = 'Nome pode conter apenas letras, números e underscore';
    }
    
    // Validação do email
    if (!formData.email) {
      newErrors.email = 'Email é obrigatório';
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(formData.email)) {
        newErrors.email = 'Email inválido';
      }
    }
    
    // Validação da senha
    if (!formData.password) {
      newErrors.password = 'Senha é obrigatória';
    } else {
      const passwordErrors = [];
      
      if (formData.password.length < 8) {
        passwordErrors.push('pelo menos 8 caracteres');
      }
      if (!/[A-Z]/.test(formData.password)) {
        passwordErrors.push('uma letra maiúscula');
      }
      if (!/[a-z]/.test(formData.password)) {
        passwordErrors.push('uma letra minúscula');
      }
      if (!/\d/.test(formData.password)) {
        passwordErrors.push('um número');
      }
      if (!/[!@#$%^&*(),.?:{}|<>]/.test(formData.password)) {
        passwordErrors.push('um caractere especial (!@#$%^&*(),.?:{}|<>)');
      }
      
      if (passwordErrors.length > 0) {
        newErrors.password = `Senha deve ter ${passwordErrors.join(', ')}`;
      }
    }
    
    // Validação da confirmação de senha
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Confirmação de senha é obrigatória';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Senhas não coincidem';
    }
    
    // Validação dos termos
    if (!formData.acceptTerms) {
      newErrors.acceptTerms = 'Você deve aceitar os termos de uso';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const getPasswordStrength = (password) => {
    if (!password) return { strength: 0, label: '' };
    
    let strength = 0;
    if (password.length >= 8) strength++;
    if (password.length >= 12) strength++;
    if (/[a-z]/.test(password) && /[A-Z]/.test(password)) strength++;
    if (/\d/.test(password)) strength++;
    if (/[!@#$%^&*(),.?:{}|<>]/.test(password)) strength++;
    
    const labels = ['', 'Fraca', 'Regular', 'Boa', 'Forte', 'Muito Forte'];
    const colors = ['', 'bg-red-500', 'bg-orange-500', 'bg-yellow-500', 'bg-green-500', 'bg-green-600'];
    
    return {
      strength,
      label: labels[strength],
      color: colors[strength],
    };
  };

  const passwordStrength = getPasswordStrength(formData.password);

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    setLoading(true);
    
    try {
      const result = await register({
        name: formData.name,
        email: formData.email,
        password: formData.password,
      });
      
      if (result.success) {
        navigate('/dashboard');
      } else {
        setErrors({ general: result.error || 'Falha no registro' });
      }
    } catch (err) {
      setErrors({ general: 'Erro ao conectar com o servidor' });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md">
        <h2 className="mt-6 text-center text-3xl font-bold text-gray-900">
          Crie sua conta
        </h2>
        <p className="mt-2 text-center text-sm text-gray-600">
          Ou{' '}
          <Link to="/login" className="font-medium text-primary-600 hover:text-primary-500">
            entre com uma conta existente
          </Link>
        </p>
      </div>

      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
        <div className="bg-white py-8 px-4 shadow sm:rounded-lg sm:px-10">
          <form className="space-y-6" onSubmit={handleSubmit}>
            {errors.general && (
              <div className="rounded-md bg-red-50 p-4">
                <p className="text-sm text-red-800">{errors.general}</p>
              </div>
            )}

            <div>
              <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                Nome de usuário
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <UserIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="name"
                  name="name"
                  type="text"
                  autoComplete="username"
                  required
                  value={formData.name}
                  onChange={handleChange}
                  className={`block w-full pl-10 pr-3 py-2 border ${
                    errors.name ? 'border-red-300' : 'border-gray-300'
                  } rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm`}
                  placeholder="joaosilva"
                />
              </div>
              <p className="mt-1 text-xs text-gray-500">
                Deve começar com letra, 3-20 caracteres, apenas letras, números e _
              </p>
              {errors.name && (
                <p className="mt-1 text-sm text-red-600">{errors.name}</p>
              )}
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700">
                Email
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <EnvelopeIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="email"
                  name="email"
                  type="email"
                  autoComplete="email"
                  required
                  value={formData.email}
                  onChange={handleChange}
                  className={`block w-full pl-10 pr-3 py-2 border ${
                    errors.email ? 'border-red-300' : 'border-gray-300'
                  } rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm`}
                  placeholder="seu@email.com"
                />
              </div>
              {errors.email && (
                <p className="mt-1 text-sm text-red-600">{errors.email}</p>
              )}
            </div>

            <div>
              <label htmlFor="password" className="block text-sm font-medium text-gray-700">
                Senha
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <LockClosedIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="password"
                  name="password"
                  type="password"
                  autoComplete="new-password"
                  required
                  value={formData.password}
                  onChange={handleChange}
                  className={`block w-full pl-10 pr-3 py-2 border ${
                    errors.password ? 'border-red-300' : 'border-gray-300'
                  } rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm`}
                  placeholder="••••••••"
                />
              </div>
              {errors.password && (
                <p className="mt-1 text-sm text-red-600">{errors.password}</p>
              )}
              
              {formData.password && (
                <div className="mt-1 space-y-1">
                  <p className={`text-xs ${formData.password.length >= 8 ? 'text-green-600' : 'text-gray-500'}`}>
                    ✓ Mínimo 8 caracteres
                  </p>
                  <p className={`text-xs ${/[A-Z]/.test(formData.password) ? 'text-green-600' : 'text-gray-500'}`}>
                    ✓ Uma letra maiúscula
                  </p>
                  <p className={`text-xs ${/[a-z]/.test(formData.password) ? 'text-green-600' : 'text-gray-500'}`}>
                    ✓ Uma letra minúscula
                  </p>
                  <p className={`text-xs ${/\d/.test(formData.password) ? 'text-green-600' : 'text-gray-500'}`}>
                    ✓ Um número
                  </p>
                  <p className={`text-xs ${/[!@#$%^&*(),.?:{}|<>]/.test(formData.password) ? 'text-green-600' : 'text-gray-500'}`}>
                    ✓ Um caractere especial (!@#$%^&*(),.?:{}|&lt;&gt;)
                  </p>
                </div>
              )}
              {formData.password && (
                <div className="mt-2">
                  <div className="flex items-center">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full transition-all duration-300 ${passwordStrength.color}`}
                        style={{ width: `${passwordStrength.strength * 20}%` }}
                      />
                    </div>
                    <span className="ml-2 text-xs text-gray-600">{passwordStrength.label}</span>
                  </div>
                </div>
              )}
            </div>

            <div>
              <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
                Confirmar senha
              </label>
              <div className="mt-1 relative">
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <LockClosedIcon className="h-5 w-5 text-gray-400" />
                </div>
                <input
                  id="confirmPassword"
                  name="confirmPassword"
                  type="password"
                  autoComplete="new-password"
                  required
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  className={`block w-full pl-10 pr-3 py-2 border ${
                    errors.confirmPassword ? 'border-red-300' : 'border-gray-300'
                  } rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500 sm:text-sm`}
                  placeholder="••••••••"
                />
              </div>
              {errors.confirmPassword && (
                <p className="mt-1 text-sm text-red-600">{errors.confirmPassword}</p>
              )}
            </div>

            <div>
              <div className="flex items-start">
                <input
                  id="acceptTerms"
                  name="acceptTerms"
                  type="checkbox"
                  checked={formData.acceptTerms}
                  onChange={handleChange}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="acceptTerms" className="ml-2 block text-sm text-gray-900">
                  Eu aceito os{' '}
                  <a href="#" className="font-medium text-primary-600 hover:text-primary-500">
                    termos de uso
                  </a>{' '}
                  e a{' '}
                  <a href="#" className="font-medium text-primary-600 hover:text-primary-500">
                    política de privacidade
                  </a>
                </label>
              </div>
              {errors.acceptTerms && (
                <p className="mt-1 text-sm text-red-600">{errors.acceptTerms}</p>
              )}
            </div>

            <div>
              <button
                type="submit"
                disabled={loading}
                className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {loading ? 'Criando conta...' : 'Criar conta'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Register;
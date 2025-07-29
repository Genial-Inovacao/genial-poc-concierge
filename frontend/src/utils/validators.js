export const validators = {
  email: (value) => {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(value);
  },

  password: (value) => {
    return value && value.length >= 8;
  },

  phone: (value) => {
    const phoneRegex = /^\+?[\d\s()-]+$/;
    return !value || phoneRegex.test(value);
  },

  required: (value) => {
    return value !== null && value !== undefined && value !== '';
  },

  minLength: (min) => (value) => {
    return !value || value.length >= min;
  },

  maxLength: (max) => (value) => {
    return !value || value.length <= max;
  },

  matchField: (fieldValue) => (value) => {
    return value === fieldValue;
  },
};

export const validateForm = (formData, rules) => {
  const errors = {};

  Object.keys(rules).forEach((field) => {
    const fieldRules = rules[field];
    const value = formData[field];

    for (const rule of fieldRules) {
      if (!rule.validator(value)) {
        errors[field] = rule.message;
        break;
      }
    }
  });

  return errors;
};
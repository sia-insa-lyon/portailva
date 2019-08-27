module.exports = {
  'env': {
    'browser': true,
    'es6': true,
  },
  'extends': [
    'google'
  ],
  'globals': {
    'Atomics': 'readonly',
    'SharedArrayBuffer': 'readonly',
  },
  'parserOptions': {
    'ecmaVersion': 2018,
  },
  'rules': {
      'comma-dangle': 'off',
      'indent':['error', 4],
      'implicit-arrow-linebreak': 'off',
      'max-len': ['error', { 'code': 180 }],
      'no-trailing-spaces': 'off',
      'semi': ['error','always'],
      'require-jsdoc': 'off',
  },
};

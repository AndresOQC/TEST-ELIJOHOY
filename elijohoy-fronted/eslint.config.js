import js from '@eslint/js'
import pluginVue from 'eslint-plugin-vue'
import globals from 'globals'

export default [
  {
    name: 'app/files-to-lint',
    files: ['**/*.{js,cjs,mjs,vue}'],
  },
  {
    name: 'app/files-to-ignore',
    ignores: ['**/dist/**', '**/node_modules/**', '.quasar/**', '/src-capacitor', '/src-cordova', '/src-ssr', '/src-pwa'],
  },
  js.configs.recommended,
  ...pluginVue.configs['flat/essential'],
  {
    name: 'app/globals',
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
        process: 'readonly',
        ga: 'readonly', // Google Analytics
        cordova: 'readonly',
        __statics: 'readonly',
        __QUASAR_SSR__: 'readonly',
        __QUASAR_SSR_SERVER__: 'readonly',
        __QUASAR_SSR_CLIENT__: 'readonly',
        __QUASAR_SSR_PWA__: 'readonly',
      },
    },
  },
  {
    name: 'app/vue-rules',
    files: ['**/*.vue'],
    rules: {
      'vue/multi-word-component-names': 'off',
    },
  },
]
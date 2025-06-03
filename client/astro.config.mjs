// @ts-check
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';
import svelte from '@astrojs/svelte';

import node from '@astrojs/node';

// https://astro.build/config
export default defineConfig({
  output: 'server',
  integrations: [
    svelte(),
  ],
  vite: {
    plugins: [tailwindcss(), svelte()],
    server: {
      proxy: {
        '/api': {
          target: 'http://127.0.0.1:5100',
          changeOrigin: true,
          secure: false
        }
      }
    }
  },

  adapter: node({
    mode: 'standalone'
  }),
});
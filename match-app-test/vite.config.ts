import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  define: {
    'import.meta.env.REACT_APP_GOOGLE_SHEETS_API_KEY': JSON.stringify(process.env.REACT_APP_GOOGLE_SHEETS_API_KEY),
    'import.meta.env.REACT_APP_GOOGLE_SHEETS_DOC_ID': JSON.stringify(process.env.REACT_APP_GOOGLE_SHEETS_DOC_ID),
  },
});
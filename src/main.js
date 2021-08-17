import { createApp } from 'vue';
import App from './App.vue';
import Oruga from '@oruga-ui/oruga-next';
import '@oruga-ui/oruga-next/dist/oruga-full.css';
import '@mdi/font/css/materialdesignicons.css';

const app = createApp(App)
app.use(Oruga);
app.mount('#app');


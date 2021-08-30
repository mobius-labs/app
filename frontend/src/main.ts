import { createApp } from 'vue';
import App from './App.vue';
import Oruga from '@oruga-ui/oruga-next';
import '@oruga-ui/oruga-next/dist/oruga-full.css';
import { bulmaConfig } from 'my-vue-app/src/plugins/oruga';
import router from './router'

import 'my-vue-app/src/assets/scss/plugin.scss'

import '@fortawesome/fontawesome-free/scss/fontawesome.scss'
import '@fortawesome/fontawesome-free/scss/regular.scss'
import '@fortawesome/fontawesome-free/scss/solid.scss'

const app = createApp(App).use(router)
app.use(Oruga, {
    iconPack: 'fas',
    ...bulmaConfig
});
app.mount('#app');


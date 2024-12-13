import { createApp } from 'vue'
import router from './router'
import './style.css'
import App from './App.vue';
import 'primeicons/primeicons.css'
import { initKeycloak } from './keycloak'; // Cambia esto a lo que realmente exportas
import { keycloak } from './keycloak'; // También importa keycloak si lo necesitas



const app = createApp(App);

// Inicializar Keycloak
initKeycloak()
  .then(() => {
    app.use(router); // Usa el enrutador después de inicializar Keycloak
    app.mount('#app'); // Monta la aplicación
  })
  .catch((error) => {
    console.error("Failed to initialize Keycloak", error);
  });
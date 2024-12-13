import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  url: 'http://localhost:8080',  // URL del servidor Keycloak
  realm: 'odeonic-app',          // Nombre del Realm
  clientId: 'frontend',        // Client ID configurado en Keycloak
});

let isKeycloakInitialized = false; // Variable para rastrear el estado de inicialización

const initKeycloak = () => {
  // Retorna una promesa que se resuelve o rechaza dependiendo del estado de inicialización
  return new Promise((resolve, reject) => {
    if (isKeycloakInitialized) {
      resolve(); // Ya está inicializado
      return;
    }

    keycloak.init({
      onLoad: 'check-sso', // Cambia esto si necesitas que inicie sesión al cargar
      checkLoginIframe: false,
      silentCheckSsoRedirectUri: window.location.origin + '/silent-check-sso.html',
      responseMode: 'query',
      // redirectUri: 'http://localhost:5173/user'  
    })
    .then((authenticated) => {
      if (authenticated) {
        console.log("Keycloak authenticated" , authenticated);
        localStorage.setItem("keycloak_token", keycloak.token); // Guarda el token
        localStorage.setItem("keycloak_refreshToken", keycloak.refreshToken); // Guarda el refresh token

        const roles = keycloak.tokenParsed?.realm_access?.roles || [];
        const currentPath = window.location.pathname; // Obtiene la ruta actual

        console.log(roles)
        if (currentPath === '/' || currentPath === '/index.html') {
          // Verifica si el usuario tiene el rol "uma_authorization"
          if (roles.includes('uma_authorization')) {
            // Redirige a la ruta del administrador
            window.location.href = 'http://localhost:5173/admin';
          } else {
            // Redirige a la ruta del usuario normal
            window.location.href = 'http://localhost:5173/user';
          }
        }
        

      } else {
        console.warn("User is not authenticated");
      }
      isKeycloakInitialized = true; // Marca como inicializado
      resolve(); // Resuelve la promesa
    })
    .catch((error) => {
      console.error("Keycloak initialization failed", error);
      reject(error); // Rechaza la promesa
    });
  });
};

export { keycloak, initKeycloak };

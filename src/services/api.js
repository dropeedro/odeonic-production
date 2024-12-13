import axios from 'axios';
import keycloak, { getToken } from '../keycloak';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',  // URL del backend de FastAPI
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${getToken()}`,  // Incluye el token en el header
  }
});

export default apiClient;

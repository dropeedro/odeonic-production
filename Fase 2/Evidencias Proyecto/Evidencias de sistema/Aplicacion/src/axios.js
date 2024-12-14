import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:8000', // URL del backend de FastAPI
});

export default instance;

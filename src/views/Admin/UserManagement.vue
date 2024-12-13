<template>
  <div class="user-list-container">
    <h1>Usuarios</h1>
    <div class="user-list">
      <div v-for="usuario in usuarios" :key="usuario._id" class="user-item">
        <span class="user-email">{{ usuario.email }}</span>
        <button 
          class="toggle-btn" 
          :class="{'blocked': usuario.isBlocked}"
          @click="toggleBloquear(usuario)">
          {{ usuario.isBlocked ? "Desbloquear" : "Bloquear" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      usuarios: []
    };
  },
  async created() {
    await this.fetchUsuarios();
  },
  methods: {
    async fetchUsuarios() {
      try {
        const response = await axios.get('http://localhost:8000/usuarios');
        // Cargar usuarios desde la base de datos y agregar el campo isBlocked localmente
        this.usuarios = response.data.map(usuario => ({
          ...usuario,
          isBlocked: false // Inicialmente todos los usuarios están desbloqueados localmente
        }));
      } catch (error) {
        console.error("Error al obtener usuarios:", error);
      }
    },
    toggleBloquear(usuario) {
      // Cambiar el estado de isBlocked para el usuario especificado solo en el frontend
      usuario.isBlocked = !usuario.isBlocked;
    }
  }
}
</script>

<style scoped>
.user-list-container {
  width: 80%;
  margin: 0 auto;
  text-align: center;
}

h1 {
  font-size: 2em;
  margin-bottom: 20px;
  color: #333;
}

.user-list {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.user-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 80%;
  padding: 10px;
  background-color: #f4f4f9;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease-in-out;
}

.user-item:hover {
  transform: translateY(-5px);
}

.user-email {
  font-size: 1.2em;
  font-weight: 600;
  color: #555;
}

.toggle-btn {
  padding: 8px 16px;
  background-color: #4CAF50;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: bold;
  transition: background-color 0.3s;
}

.toggle-btn:hover {
  background-color: #45a049;
}

.toggle-btn.blocked {
  background-color: #f44336;
}

.toggle-btn.blocked:hover {
  background-color: #d32f2f;
}
</style>

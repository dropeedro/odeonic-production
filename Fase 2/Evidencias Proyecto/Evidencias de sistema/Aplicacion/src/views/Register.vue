<template>
  <div class="bg-backgroundColor min-h-screen flex items-start justify-center mt-12">
    <div class="bg-backgroundColor p-8 rounded-lg shadow-2xl w-96">
      <h2 class="pt-8 text-3xl text-SecondaryColor font-bold mb-2">Register</h2>
      <p class="text-md text-SecondaryColor mb-6">Remember not to show your password to anyone!</p>

      <form @submit.prevent="handleRegister">
        <div class="grid grid-cols-2 gap-4 mb-4">
          <input type="text" v-model="firstName" placeholder="First Name" class="w-full px-3 py-2 border rounded-md" required>
          <input type="text" v-model="lastName" placeholder="Last Name" class="w-full px-3 py-2 border rounded-md" required>
        </div>
        <div class="grid grid-cols-2 gap-4 mb-4">
          <input type="text" v-model="birthDate" placeholder="Birth Date" class="w-full px-3 py-2 border rounded-md" required>
          <input type="text" v-model="country" placeholder="Country" class="w-full px-3 py-2 border rounded-md" required>
        </div>
        <div class="grid grid-cols-2 gap-4 mb-4">
          <input type="text" v-model="gender" placeholder="Gender" class="w-full px-3 py-2 border rounded-md" required>
          <input type="text" v-model="language" placeholder="Language" class="w-full px-3 py-2 border rounded-md" required>
        </div>
        <div class="mb-4">
          <input type="email" v-model="email" placeholder="Email" class="w-full px-3 py-2 border rounded-md" required>
        </div>
        <div class="mb-6">
          <input type="password" v-model="password" placeholder="Password" class="w-full px-3 py-2 border rounded-md" required>
        </div>
        <button type="submit" class="w-full bg-SecondaryColor text-backgroundColor py-2 rounded-md hover:bg-SecondaryColorDark transition duration-300">Register</button>
      </form>

      <div class="mt-6">
        <button @click="registerWithKeycloak" class="w-full bg-PrimaryColor text-backgroundColor py-2 rounded-md hover:PrimaryColorDark transition duration-300">Registrar con Keycloak</button>
      </div>
      <div class="mt-6 text-center">
        <p class="text-sm text-red-600">{{ errorMessage }}</p>
        <p class="text-sm text-green-600">{{ successMessage }}</p>
        <p class="text-sm text-SecondaryColor">You want to go back?</p>
        <div class="flex justify-center items-center">
          <a href="/Login" class="w-full flex justify-center items-center bg-transparent rounded-md">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-10 h-10 stroke-current text-PrimaryColor hover:text-PrimaryColorDark" viewBox="0 0 24 24" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path stroke="none" d="M0 0h24v24H0z" fill="none" />
              <path d="M5 12h14" />
              <path d="M5 12l4 4" />
              <path d="M5 12l4 -4" />
            </svg>
          </a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { keycloak } from '../keycloak'; 
export default {
  data() {
    return {
      firstName: '',
      lastName: '',
      birthDate: '',
      country: '',
      gender: '',
      language: '',
      email: '',
      password: '',
      errorMessage: '', // Variable para mensajes de error
      successMessage: '', // Variable para mensajes de éxito
    }
  },
  methods: {
    async handleRegister() {
      // Crear un objeto con los datos de registro
      const userData = {
        email: this.email,
        password: this.password
      };

      try {
        const response = await fetch('http://localhost:8000/users', { // Cambia la URL según sea necesario
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(userData),
        });

        if (!response.ok) {
          // Si la respuesta no es exitosa, lanza un error
          const errorData = await response.json();
          throw new Error(errorData.detail || 'Error en el registro');
        }

        // Si el registro es exitoso, muestra un mensaje de éxito
        const data = await response.json();
        this.successMessage = `Usuario registrado con éxito: ${data.email}`;
        this.errorMessage = ''; // Limpia el mensaje de error
      } catch (error) {
        // Manejar cualquier error que ocurra durante el registro
        this.errorMessage = error.message;
        this.successMessage = ''; // Limpia el mensaje de éxito
      }
    },
    registerWithKeycloak() {
      keycloak.register({
        redirectUri: window.location.origin, 
      });
    }
  }
}
</script>

<style scoped>

</style>

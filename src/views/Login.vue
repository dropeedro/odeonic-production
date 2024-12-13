<!-- <template>
  <div class="bg-secondaryWhiteColor min-h-screen flex items-start justify-center mt-12">
    <div class="bg-secondaryWhiteColor p-8 rounded-lg shadow-2xl w-96">
      <h2 class="pt-8 text-3xl text-primaryPurpleColor font-bold mb-2">Login</h2>
      <p class="text-md text-primaryPurpleColor mb-6">Remember not to show your password to anyone!</p>

      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <input type="email" v-model="email" placeholder="Email" class="w-full px-3 py-2 border rounded-md" required>
        </div>
        <div>
          <input type="password" v-model="password" placeholder="Password" class="w-full px-3 py-2 border rounded-md"
            required>
        </div>
        <div class="mt-2 text-center">
          <a href="/" class="text-sm text-primaryPurpleColor">You Forgot Your Password?</a>
        </div>
        <button type="submit"
          class="w-full bg-primaryPurpleColor text-secondaryWhiteColor py-2 rounded-md hover:bg-terciaryPurpleColor transition duration-300">Log
          in</button>
      </form>
      <div class="mt-2 text-center text-sm text-primaryPurpleColor">
        You can also log in with
      </div>
      <div class="mb-8 mt-2 flex justify-center space-x-4">
        <a href="#" class="text-2xl bg-plusGrayColor p-2 rounded-[4px]">
          <img src="../assets/InstagramIcon.svg" alt="Instagram" class="w-8 h-8" />
        </a>
        <a href="#" class="text-2xl bg-plusGrayColor p-2 rounded-[4px]">
          <img src="../assets/TiktokIcon.svg" alt="Tiktok" class="w-8 h-8" />
        </a>
        <a href="#" class="text-2xl bg-plusGrayColor p-2 rounded-[4px]">
          <img src="../assets/XIcon.svg" alt="X" class="w-8 h-8" />
        </a>
        <a href="#" class="text-2xl bg-plusGrayColor p-2 rounded-[4px]">
          <img src="../assets/FacebookIcon.svg" alt="Facebook" class="w-8 h-8" />
        </a>
        <a href="#" class="text-2xl bg-plusGrayColor p-2 rounded-[4px]">
          <img src="../assets/GoogleIcon.svg" alt="Google" class="w-8 h-8" />
        </a>
      </div>
      <div>
        <div class="mt-4 text-center text-sm text-primaryPurpleColor">
          You don't have an account?
        </div>
        <a href="/register"
          class="mb-1 w-full font-bold bg-plusGrayColor text-primaryPurpleColor py-2 rounded-md block text-center hover:bg-gray-300 transition duration-300">
          Register
        </a>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      email: '',
      password: ''
    }
  },
  methods: {
    handleLogin() {
      // Handle login logic here
      console.log('Login attempted with:', this.email, this.password)
    }
  }
}
</script> -->

<template>
  <div
    class="bg-backgroundColor min-h-screen flex items-start justify-center mt-12"
  >
    <div class="bg-backgroundColor p-8 rounded-lg shadow-2xl w-96">
      <h2 class="pt-8 text-3xl text-SecondaryColor font-bold mb-2">Login</h2>
      <p class="text-md text-SecondaryColor mb-6">
        Remember not to show your password to anyone!
      </p>

      <!-- Botón para iniciar sesión con Keycloak -->
      <div class="mt-4 flex justify-center">
        <button
          @click="loginWithKeycloak"
          class="w-full bg-SecondaryColor text-backgroundColor py-2 rounded-md hover:bg-SecondaryColorDark transition duration-300"
        >
          Login with Keycloak
        </button>
      </div>
    </div>
  </div>
</template>

<script>
// import keycloak from '../keycloak'; // Asegúrate de importar correctamente

// export default {
//   methods: {
//     loginWithKeycloak() {
//       // Iniciar Keycloak solo cuando el usuario haga clic en el botón
//       keycloak.init({ onLoad: 'login-required' })
//         .then(() => {
//           keycloak.login();
//         })
//         .catch((error) => {
//           console.error('Failed to initialize Keycloak', error);
//         });
//     },
//   },
// };
import { keycloak, initKeycloak } from "../keycloak";

export default {
  // methods: {
  //   async loginWithKeycloak() {
  //     try {
  //       // Asegúrate de que Keycloak esté inicializado
  //       await initKeycloak();

  //       // Luego intenta hacer el login
  //       keycloak.login();
  //     } catch (error) {
  //       console.error("Error during Keycloak login:", error);
  //     }
  //   }
  // }
  methods: {
    loginWithKeycloak() {
      initKeycloak()
        .then(() => {
          keycloak
            .login()
            .then(() => {
              this.$router.push("/Admin");
            })
            .catch((error) => {
              console.error("Error during Keycloak login", error);
            });
        })
        .catch((error) => {
          console.error("Error during Keycloak initialization", error);
        });
    },
  },
};
</script>

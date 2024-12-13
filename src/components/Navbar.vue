<template>
  <header class="bg-SecondaryColor sticky top-0 shadow-md px-4 py-2 z-50">
    <div class="flex items-center justify-between max-w-6xl mx-auto">
      <!-- Logo -->
      <h1 class="flex-shrink-0 text-4xl font-bold text-PrimaryColor">
        RIFF-ME
        <h5 class="text-sm font-medium">MUSIC GENERATOR</h5>
      </h1>

      <!-- Navigation -->
      <nav class="hidden md:block">
        <ul class="flex items-center space-x-4">
          <li
            class="p-4 border-b-2 border-PrimaryColor border-opacity-0 hover:border-opacity-100 hover:text-PrimaryColorDark text-PrimaryColor duration-200 cursor-pointer">
            <a href="/">Home</a>
          </li>
          <li
            class="p-4 border-b-2 border-PrimaryColor border-opacity-0 hover:border-opacity-100 hover:text-PrimaryColorDark text-PrimaryColor duration-200 cursor-pointer">
            <a href="#midi">Generate</a>
          </li>
          <li
            class="p-4 border-b-2 border-PrimaryColor border-opacity-0 hover:border-opacity-100 hover:text-PrimaryColorDark text-PrimaryColor duration-200 cursor-pointer">
            <a href="#about">About</a>
          </li>
          <li
            class="p-4 border-b-2 border-PrimaryColor border-opacity-0 hover:border-opacity-100 hover:text-PrimaryColorDark text-PrimaryColor duration-200 cursor-pointer">
            <a href="#plans">Pricing Plans</a>
          </li>
        </ul>
      </nav>

      <!-- Buttons -->
      <div class="flex items-center space-x-2">
        <button @click="loginWithKeycloak" class="text-PrimaryColor hover:text-PrimaryColorDark duration-200">
          <svg class="h-8 sm:h-10 p-1" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"
            viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round"
            stroke-linejoin="round">
            <path stroke="none" d="M0 0h24v24H0z" fill="none" />
            <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0" />
            <path d="M12 10m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0" />
            <path d="M6.168 18.849a4 4 0 0 1 3.832 -2.849h4a4 4 0 0 1 3.834 2.855" />
          </svg>
        </button>

        <!-- Hamburger Menu for Small Screens -->
        <button class="md:hidden text-PrimaryColor focus:outline-none" @click="toggleMenu">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="h-8">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Menu -->
    <div v-if="menuOpen" class="md:hidden bg-SecondaryColor py-4">
      <ul class="flex flex-col items-center space-y-2">
        <li>
          <a href="/" class="block py-2 text-PrimaryColor hover:text-PrimaryColorDark">Home</a>
        </li>
        <li>
          <a href="#midi" class="block py-2 text-PrimaryColor hover:text-PrimaryColorDark">Generate</a>
        </li>
        <li>
          <a href="#about" class="block py-2 text-PrimaryColor hover:text-PrimaryColorDark">About</a>
        </li>
        <li>
          <a href="#plans" class="block py-2 text-PrimaryColor hover:text-PrimaryColorDark">Pricing Plans</a>
        </li>
      </ul>
    </div>
  </header>
</template>

<script>
import { keycloak, initKeycloak } from "../keycloak";

export default {
  data() {
    return {
      menuOpen: false,
    };
  },
  methods: {
    toggleMenu() {
      this.menuOpen = !this.menuOpen;
    },
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

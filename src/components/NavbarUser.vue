<template>
  <header class="bg-SecondaryColor sticky top-0 shadow-md px-4 py-2 z-50">
    <div class="flex items-center justify-between max-w-6xl mx-auto">
      <!-- Logo -->
      <h2 class="flex-shrink-0 text-4xl font-bold text-PrimaryColor">
        RIFF-ME
        <h5 class="text-sm font-medium">MUSIC GENERATOR</h5>
      </h2>
      <!-- Navigation for larger screens -->
      <nav class="hidden md:block font-semibold text-md">
        <ul class="flex items-center space-x-4 text-PrimaryColor">
          <li class="p-4 hover:text-PrimaryColorDark text-PrimaryColor duration-200 cursor-pointer">
          </li>
          <li class="p-4 hover:text-PrimaryColorDark text-PrimaryColor duration-200 cursor-pointer">
          </li>
          <li class="p-4 hover:text-PrimaryColorDark text-PrimaryColor duration-200 cursor-pointer">
          </li>
        </ul>
      </nav>

      <!-- Profile icon with dropdown and Hamburger for small screens -->
      <div class="flex items-center space-x-2">
        <!-- Profile Dropdown -->
        <div class="relative" ref="dropdownRef">
          <a href="#" @click="toggleDropdown"
            class="flex items-center text-PrimaryColor hover:text-PrimaryColorDark duration-200">
            <svg class="h-8 sm:h-10 p-1" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" focusable="false"
              viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" fill="none" stroke-linecap="round"
              stroke-linejoin="round">
              <path stroke="none" d="M0 0h24v24H0z" fill="none" />
              <path d="M12 12m-9 0a9 9 0 1 0 18 0a9 9 0 1 0 -18 0" />
              <path d="M12 10m-3 0a3 3 0 1 0 6 0a3 3 0 1 0 -6 0" />
              <path d="M6.168 18.849a4 4 0 0 1 3.832 -2.849h4a4 4 0 0 1 3.834 2.855" />
            </svg>
          </a>
          <!-- Dropdown menu -->
          <div v-if="isDropdownOpen"
            class="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-md shadow-lg z-10">
            <button @click="openModal"
              class="block w-full rounded-md px-4 py-2 text-left text-SecondaryColor hover:bg-PrimaryColor hover:text-SecondaryColor duration-200">
              Cerrar sesión
            </button>
          </div>
        </div>

        <!-- Hamburger Menu -->
        <button class="md:hidden text-PrimaryColor focus:outline-none" @click="toggleMenu">
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5"
            stroke="currentColor" class="h-8">
            <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5M3.75 17.25h16.5" />
          </svg>
        </button>
      </div>
    </div>

    <!-- Mobile Navigation -->
    <div v-if="menuOpen" class="md:hidden bg-SecondaryColor py-4">
      <ul class="flex flex-col items-center space-y-2 text-PrimaryColor">
        <li>
          <router-link to="/admin" class="block py-2 hover:text-PrimaryColorDark" @click="menuOpen = false">
            Dashboard
          </router-link>
        </li>
        <li>
          <router-link to="/admin/plans" class="block py-2 hover:text-PrimaryColorDark" @click="menuOpen = false">
            Plans
          </router-link>
        </li>
        <li>
          <router-link to="/admin/users" class="block py-2 hover:text-PrimaryColorDark" @click="menuOpen = false">
            Users
          </router-link>
        </li>
      </ul>
    </div>
  </header>

  <!-- Modal -->
  <div v-if="isModalOpen" class="fixed inset-0 flex items-center justify-center z-50 bg-black bg-opacity-50"
    @click="closeModal">
    <div class="bg-white p-6 rounded-lg w-80" @click.stop>
      <h3 class="text-lg font-semibold text-center mb-4 text-SecondaryColor">
        ¿Estás seguro de que quieres cerrar sesión?
      </h3>
      <div class="flex justify-between">
        <button @click="logout" class="bg-PrimaryColor text-white px-4 py-2 rounded-lg hover:bg-PrimaryColorDark">
          Sí
        </button>
        <button @click="closeModal" class="bg-gray-300 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-400">
          No
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { keycloak } from "../keycloak";
import { useRouter } from "vue-router";

const router = useRouter();
const isDropdownOpen = ref(false);
const isModalOpen = ref(false);
const menuOpen = ref(false);

function toggleDropdown() {
  isDropdownOpen.value = !isDropdownOpen.value;
}

function toggleMenu() {
  menuOpen.value = !menuOpen.value;
}

function openModal() {
  isModalOpen.value = true;
  isDropdownOpen.value = false;
}

function closeModal() {
  isModalOpen.value = false;
}

function logout() {
  keycloak.logout({ redirectUri: "http://localhost:5173/login" }); // Redirige al login
  closeModal();
}
</script>

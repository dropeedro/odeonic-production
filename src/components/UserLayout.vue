<script setup>
import NavbarUser from '../components/NavbarUser.vue';
</script>

<template>
  <NavbarUser />
  <main>
    <div class="max-w-[1280px] mx-auto">
      <router-view />
    </div>
  </main>
</template>
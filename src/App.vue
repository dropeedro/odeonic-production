<template>
  <router-view />
 </template>

<script>
export default {
  mounted() {
    // Verifica si hay un parámetro de error en la URL y redirige
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has("error")) {
      this.$router.replace({ path: "/" }); // Redirige a la página principal para limpiar la URL
    }
  }
};
</script>
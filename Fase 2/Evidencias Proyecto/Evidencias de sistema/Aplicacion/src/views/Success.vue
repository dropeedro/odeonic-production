<template>
  <div class="flex flex-col items-center justify-center h-screen text-center">
    <img src="../assets/riffyellow.png" alt="riff logo" class="h-60" />
    <h2 class="text-8xl font-bold text-PrimaryColor mb-2">
      ¡Successful Payment !
    </h2>
    <p class="text-2xl text-SecondaryColor">
      Thank you for your purchase. The download will begin shortly...
    </p>
    <div class="mt-4 flex justify-center">
      <button
        @click="$router.push('/')"
        class="w-full bg-SecondaryColor text-backgroundColor py-2 rounded-md hover:bg-SecondaryColorDark transition duration-300 p-20"
      >
        Ir al Inicio
      </button>
    </div>
  </div>
</template>

<script>
export default {
  async mounted() {
    const urlParams = new URLSearchParams(window.location.search);
    const songId = urlParams.get("song_id");

    if (songId) {
      // Redirigir al backend para descargar la canción
      window.location.href = `http://localhost:8000/stripe/download-song?song_id=${songId}`;
    }
  },
};
</script>

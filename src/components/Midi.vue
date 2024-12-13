<template>
  <div class="pt-10 flex flex-col items-center justify-center bg-backgroundColor">
    <div class="p-2 rounded-lg max-w-3xl w-full">
      <!-- TITLE -->
      <div class="mx-auto mb-[60px] max-w-[510px] text-center">
        <h2 class="text-PrimaryColor mb-3 text-3xl leading-[1.208] font-bold text-dark sm:text-4xl md:text-[40px]">
          Let's Generate!
        </h2>
        <p class="text-base text-SecondaryColor">
          We invite you to experiment with our innovative music generator, which
          uses adjustable parameters to create unique melodies and harmonies.
        </p>
      </div>

      <div class="flex flex-col lg:flex-row justify-between items-start lg:space-x-4 space-y-6 lg:space-y-0">
        <!-- GENERATE MUSIC -->
        <div class="bg-backgroundColor p-6 rounded-lg w-full max-w-md">
          <h2 class="text-lg font-semibold mb-2 text-SecondaryColor">
            What's your content?
          </h2>
          <div class="relative mb-4">
            <select
              class="bg-backgroundColor text-SecondaryColor p-2 flex-grow rounded-md w-full appearance-none outline-none"
              style="outline: 2px solid #d9d9d9">
              <option value="Party">Party</option>
              <option value="Relaxing">Relaxing</option>
              <option value="Workout">Workout</option>
              <option value="Rock">Rock</option>
            </select>
            <div class="absolute right-0.5 top-1/2 transform -translate-y-1/2 bg-SecondaryColor p-2 rounded">
              <span class="text-white">&#9660;</span>
            </div>
          </div>

          <h2 class="text-lg font-semibold mb-2 text-SecondaryColor">
            How much music?
          </h2>
          <div class="relative mb-4">
            <select
              class="bg-backgroundColor text-SecondaryColor p-2 flex-grow rounded-md w-full appearance-none outline-none"
              style="outline: 2px solid #d9d9d9">
              <option value="30">30 seconds</option>
              <option value="60">60 seconds</option>
              <option value="120">120 seconds</option>
            </select>
            <div class="absolute right-0.5 top-1/2 transform -translate-y-1/2 bg-SecondaryColor p-2 rounded">
              <span class="text-white">&#9660;</span>
            </div>
          </div>

          <h2 class="text-lg font-semibold mb-4 text-SecondaryColor">
            Find your Groove
          </h2>
          <div v-for="(item, index) in grooves" :key="index" class="flex items-center justify-between mb-4">
            <span>{{ item.label }}</span>
            <input type="range" class="w-1/2" v-model="grooveValues[index]" :min="item.min" :max="item.max"
              @input="handleGrooveChange(index)" />
            <span>{{ item.value }}</span>
          </div>

          <!-- Play button -->
          <h2 class="text-lg font-semibold mb-2 text-SecondaryColor">
            Do you want to hear a preview?
          </h2>
          <button @click="playSongBasedOnParameters"
            class="bg-SecondaryColor text-secondaryWhiteColor p-1 rounded-md w-full">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-10 w-10 mx-auto" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path v-if="isPlaying" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M10 9v6m4-6v6" />
              <path v-else stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </button>
        </div>

        <!-- SHARE MUSIC -->
        <div class="bg-secondaryWhiteColor p-7 rounded-lg border-2 w-full max-w-md">
          <h2 class="text-lg font-bold text-SecondaryColor mb-2">
            Like it? Keep it!
          </h2>
          <button @click="redirectToCheckout" class="bg-plusGrayColor p-2 rounded-md mb-4">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-12 w-12" fill="none" viewBox="0 0 24 24"
              stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
          </button>
          <h3 class="text-lg font-bold text-SecondaryColor mb-2">Share it</h3>
          <div class="flex space-x-2">
            <button @click="shareOnSocialMedia('Instagram')" class="bg-plusGrayColor p-2 rounded-md">
              <img src="../assets/InstagramIcon.svg" alt="Instagram icon" class="h-12 w-12" />
            </button>
            <button @click="shareOnSocialMedia('TikTok')" class="bg-plusGrayColor p-2 rounded-md">
              <img src="../assets/TiktokIcon.svg" alt="TikTok icon" class="h-12 w-12" />
            </button>
            <button @click="shareOnSocialMedia('Twitter')" class="bg-plusGrayColor p-2 rounded-md">
              <img src="../assets/XIcon.svg" alt="Twitter icon" class="h-11 w-12" />
            </button>
            <button @click="shareOnSocialMedia('Facebook')" class="bg-plusGrayColor p-2 rounded-md">
              <img src="../assets/FacebookIcon.svg" alt="Facebook icon" class="h-12 w-12" />
            </button>
          </div>
          <h3 class="font-bold text-SecondaryColor mt-4 mb-1 text-lg" v-if="!isAuthenticated">
            And that's not all
          </h3>
          <p class="text-sm text-SecondaryColor mb-4" v-if="!isAuthenticated">
            Unlock more features when you create an account
          </p>
          <a v-if="!isAuthenticated" href="/register"
            class="bg-SecondaryColor text-secondaryWhiteColor py-4 px-4 rounded-md w-full mb-2 font-semibold block text-center">
            Create a free Account
          </a>
          <p class="text-sm text-center" v-if="!isAuthenticated">You already have an account?</p>
          <p class="text-lg text-center text-SecondaryColor font-semibold p-2" v-if="!isAuthenticated">
            <a href="/login" class="text-SecondaryColor">Log In</a>
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import PaymentButton from "./PaymentButton.vue";
import { loadStripe } from "@stripe/stripe-js";
import { keycloak } from "../keycloak";

export default {
  components: {
    PaymentButton,
  },
  name: "OdeonicInterface",
  data() {
    return {
      grooveValues: [50, 50, 50],
      selectedContent: "Party",
      selectedDuration: "30",
      audio: null,
      isPlaying: false,
      grooves: [
        { label: "Chilled", min: 0, max: 100, value: "Wild" },
        { label: "Weird", min: 0, max: 100, value: "Formal" },
        { label: "Barbeque", min: 0, max: 100, value: "Dance" },
      ],
    };
  },
  methods: {
    handleGrooveChange(index) {
      console.log(this.grooveValues[index]);
    },
    playSongBasedOnParameters() {
  const [param1, param2, param3] = this.grooveValues;
  const tolerance = 10;

  // Reiniciar la URL de la canción al comenzar una nueva reproducción
  this.songUrl = null;

  // Limpiar la canción anterior si hay una nueva reproducción
  if (this.audio) {
    this.audio.pause();
    this.audio.currentTime = 0;
  }

  // Verificar los valores específicos y asignar la canción correspondiente
  if (
    Math.abs(param1 - 70) <= tolerance &&
    Math.abs(param2 - 50) <= tolerance &&
    Math.abs(param3 - 20) <= tolerance
  ) {
    this.audio = new Audio("src/assets/songs/song1.mp3");
    this.songUrl = "https://your-public-server.com/song1.mp3";
  } else if (
    Math.abs(param1 - 10) <= tolerance &&
    Math.abs(param2 - 100) <= tolerance &&
    Math.abs(param3 - 50) <= tolerance
  ) {
    this.audio = new Audio("src/assets/songs/song2.mp3");
    this.songUrl = "https://your-public-server.com/song2.mp3";
  } else if (
    Math.abs(param1 - 20) <= tolerance &&
    Math.abs(param2 - 80) <= tolerance &&
    Math.abs(param3 - 10) <= tolerance
  ) {
    this.audio = new Audio("src/assets/songs/song3.mp3");
    this.songUrl = "https://your-public-server.com/song3.mp3";
  } else {
    this.audio = new Audio("src/assets/songs/default.mp3");
    this.songUrl = "https://your-public-server.com/default.mp3";
  }

  // Alternar el estado de reproducción
  if (this.isPlaying) {
    this.audio.pause();
    this.isPlaying = false;
    this.songUrl = null; // Limpiar la URL de la canción si se detiene
  } else {
    this.audio.play();
    this.isPlaying = true;
  }
},
shareOnSocialMedia(platform) {
  // Verificar si hay una canción seleccionada (es decir, si songUrl está definida)
  if (!this.songUrl) {
    alert("Ajusta los parámetros, reproduce una canción y asegúrate de no detenerla antes de compartir.");
    return;
  }

  const publicSongUrl = this.songUrl; // Asegúrate de que songUrl apunte a una URL pública.

  const socialMediaUrls = {
    Instagram: `https://www.instagram.com/sharer/sharer.php?u=${encodeURIComponent(publicSongUrl)}`,
    TikTok: `https://www.tiktok.com/share/video?url=${encodeURIComponent(publicSongUrl)}`,
    Twitter: `https://twitter.com/intent/tweet?url=${encodeURIComponent(publicSongUrl)}&text=Check out this awesome song!`,
    Facebook: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(publicSongUrl)}`,
  };

  // Abre la URL correspondiente en una nueva ventana
  if (socialMediaUrls[platform]) {
    window.open(socialMediaUrls[platform], "_blank");
  } else {
    console.error(`La plataforma ${platform} no está soportada.`);
  }
},
async redirectToCheckout() {
      const stripe = await loadStripe(
        "pk_test_51QBHvAGa2SYBUggvrPgqC8kSuy3yo9ZISsFK49FSExZeC185kj6brXyzhjJn9b9iBg2TSbHPp8Mv66CVNJrNdfeS00whcWaAYC"
      );

      // Determinar cuál canción se debe enviar basado en la lógica de tu app
      let songId;
      const [param1, param2, param3] = this.grooveValues;
      const tolerance = 10;

      if (
        Math.abs(param1 - 70) <= tolerance &&
        Math.abs(param2 - 50) <= tolerance &&
        Math.abs(param3 - 20) <= tolerance
      ) {
        songId = "song1";
      } else if (
        Math.abs(param1 - 10) <= tolerance &&
        Math.abs(param2 - 100) <= tolerance &&
        Math.abs(param3 - 50) <= tolerance
      ) {
        songId = "song2";
      } else if (
        Math.abs(param1 - 20) <= tolerance &&
        Math.abs(param2 - 80) <= tolerance &&
        Math.abs(param3 - 10) <= tolerance
      ) {
        songId = "song3";
      } else {
        songId = "default";
      }

      // Enviar el ID de la canción seleccionada al backend
      const response = await fetch(
        "http://localhost:8000/stripe/create-checkout-session",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ song_id: songId }),
        }
      );

      if (!response.ok) {
        const error = await response.json();
        console.error("Error al crear la sesión de pago:", error);
        return;
      }

      const { url } = await response.json();

      // Redirigir al usuario a la página de pago de Stripe
      window.location.href = url;
    },
  },

  created() {
    this.isAuthenticated = keycloak.authenticated; // Verifica si la sesión está activa
  },

};
</script>
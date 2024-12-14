<script setup>
import { onMounted } from "vue";
import { useRoute } from "vue-router";
import Midi from '../../components/Midi.vue';

const route = useRoute();

onMounted(async () => {
  const { success, email, plan } = route.query;

  if (success && email && plan) {
    console.log("Payment success detected."); // Log para depuración
    console.log("Params received:", { email, plan }); // Log para depuración

    try {
      const subscriptionData = {
        subscription_id: "sub_test_12345", // Simulado, reemplaza con el ID real si lo tienes
        status: "active",
        plan,
        start_date: Math.floor(Date.now() / 1000), // Tiempo actual
        end_date: Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60, // +30 días
      };

      console.log("Subscription data to update:", subscriptionData); // Log para depuración

      const response = await fetch("http://localhost:8000/api/update-subscription", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          user_email: email,
          subscription_data: subscriptionData,
        }),
      });

      if (response.ok) {
        console.log("Subscription updated successfully.");
      } else {
        const errorDetails = await response.json();
        console.error("Failed to update subscription:", errorDetails);
      }
    } catch (error) {
      console.error("Error updating subscription:", error);
    }
  } else {
    console.log("No payment success detected or missing params.");
  }
});
</script>
<template>
    <div>
      <!-- Sección del dashboard -->
      <section id="dashboard" class="py-8">
        <div class="container mx-auto px-4">
          <h1 class="text-3xl font-bold text-center mb-4">Welcome to Your Dashboard</h1>
          <p class="text-center text-lg text-gray-600">Manage your subscription and explore our platform.</p>
        </div>
      </section>
  
      <!-- Sección de MIDI -->
      <section id="midi" class="py-8">
        <div class="container mx-auto px-4">
          <Midi></Midi>
        </div>
      </section>
    </div>
  </template>
  
  <style>
  /* Estilo adicional si es necesario */
  </style>
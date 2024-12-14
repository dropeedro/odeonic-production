<template>
  <div class="admin-dashboard">
    <div class="dashboard-content">
      <!-- Título principal -->
      <div class="section-header">
        <h1
          class="text-3xl font-bold mb-6 pt-10 text-SecondaryColor text-center sm:text-left"
        >
          Admin Dashboard
        </h1>
      </div>

      <!-- Tarjeta de Total Plans -->
      <div class="grid grid-cols-1 gap-6 mb-6">
        <div
          class="card bg-white w-full p-6 rounded-lg border-2 border-plusGrayColor text-center"
        >
          <h2 class="text-xl font-bold text-gray-800 mb-4">Total Plans</h2>
          <p class="text-4xl font-bold text-PrimaryColor">{{ totalPlans }}</p>
        </div>
      </div>

      <!-- Grid de Canvas -->
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
        <!-- Card 1 -->
        <div
          class="card bg-white w-full p-6 rounded-lg border-2 border-plusGrayColor"
        >
          <canvas id="userChart"></canvas>
        </div>
        <!-- Card 2 -->
        <div
          class="card bg-white w-full p-6 rounded-lg border-2 border-plusGrayColor"
        >
          <canvas id="downloadsChart"></canvas>
        </div>
        <!-- Card 3 -->
        <div
          class="card bg-white w-full p-6 rounded-lg border-2 border-plusGrayColor"
        >
          <canvas id="earningsChart"></canvas>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, registerables } from "chart.js";
import axios from "../../axios"; // Asegúrate de usar la ruta correcta

Chart.register(...registerables);

export default {
  name: "DashboardContent",
  data() {
    return {
      totalPlans: 0, // Inicializar el conteo total de planes
    };
  },
  mounted() {
    this.fetchTotalPlans(); // Obtener el conteo de planes al cargar el componente

    // Ejemplo de gráfico para usuarios
    new Chart(document.getElementById("userChart"), {
      type: "line",
      data: {
        labels: ["Week 1", "Week 2", "Week 3", "Week 4"],
        datasets: [
          {
            label: "New Users",
            data: [30, 45, 25, 60],
            borderColor: "rgba(75, 192, 192, 1)",
            backgroundColor: "rgba(75, 192, 192, 0.2)",
            fill: true,
          },
        ],
      },
    });

    // Ejemplo de gráfico para descargas
    new Chart(document.getElementById("downloadsChart"), {
      type: "bar",
      data: {
        labels: ["January", "February", "March", "April"],
        datasets: [
          {
            label: "Downloads",
            data: [150, 200, 180, 220],
            backgroundColor: "rgba(54, 162, 235, 0.2)",
            borderColor: "rgba(54, 162, 235, 1)",
            borderWidth: 1,
          },
        ],
      },
    });

    // Ejemplo de gráfico para ganancias
    new Chart(document.getElementById("earningsChart"), {
      type: "doughnut",
      data: {
        labels: ["Plan A", "Plan B", "Plan C"],
        datasets: [
          {
            label: "Earnings",
            data: [500, 700, 400],
            backgroundColor: [
              "rgba(255, 99, 132, 0.2)",
              "rgba(75, 192, 192, 0.2)",
              "rgba(153, 102, 255, 0.2)",
            ],
            borderColor: [
              "rgba(255, 99, 132, 1)",
              "rgba(75, 192, 192, 1)",
              "rgba(153, 102, 255, 1)",
            ],
            borderWidth: 1,
          },
        ],
      },
    });
  },
  methods: {
    async fetchTotalPlans() {
      try {
        const response = await axios.get("/plans"); // Solicita todos los planes
        this.totalPlans = response.data.length; // Asigna el número total de planes
      } catch (error) {
        console.error("Error fetching total plans:", error);
      }
    },
  },
};
</script>
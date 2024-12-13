<template>
  <div class="admin-dashboard px-4 sm:px-6 lg:px-8">
    <div class="dashboard-content">
      <div class="plan-management">
        <div class="section-header text-center sm:text-left">
          <h1 class="text-3xl font-bold mb-6 pt-10 text-SecondaryColor">
            Plan Management
          </h1>
        </div>

        <!-- Formulario para agregar nuevo plan -->
        <div
          class="plan-form bg-backgroundColor p-6 sm:p-8 rounded-lg border-2 border-plusGrayColor mb-10 max-w-3xl mx-auto">
          <h2 class="text-2xl font-semibold mb-4 text-SecondaryColor">
            Add New Plan
          </h2>
          <input v-model="newPlan.name" placeholder="Plan Name"
            class="input-field mb-4 border-2 border-plusGrayColor p-3 rounded-lg w-full" />
          <input v-model.number="newPlan.price" type="number" placeholder="Plan Price (USD)"
            class="input-field mb-4 border-2 border-plusGrayColor p-3 rounded-lg w-full" />
          <textarea v-model="newPlan.description" placeholder="Plan Description"
            class="input-field mb-4 border-2 border-plusGrayColor p-3 rounded-lg w-full"></textarea>
          <textarea v-model="newPlan.features" placeholder="Plan Features (comma separated)"
            class="input-field mb-4 border-2 border-plusGrayColor p-3 rounded-lg w-full"></textarea>
          <input v-model="newPlan.type" placeholder="plan id (one word)" class="input-field mb-4 border-2 border-plusGrayColor p-3 rounded-lg w-full"/>
          <button @click="createPlan"
            class="primary-btn w-full py-3 text-backgroundColor bg-green-500 hover:bg-green-600 rounded-md">
            Add Plan
          </button>
        </div>

        <!-- Listado de planes disponibles -->
        <div class="plans-list">
          <h1 class="text-3xl font-bold mb-6 text-SecondaryColor text-center sm:text-left">
            Available Plans
          </h1>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <div v-for="plan in plans" :key="plan._id"
              class="plan-card relative z-10 mb-10 overflow-hidden rounded-lg border-2 border-plusGrayColor bg-white py-6 sm:py-8 px-6 sm:px-8 transition-transform duration-300 hover:transform hover:translate-y-1">
              <span class="mb-3 block text-lg font-semibold text-PrimaryColor">{{ plan.name }}</span>
              <h2 class="mb-5 text-2xl sm:text-4xl font-bold text-gray-900">
                <span class="text-PrimaryColor">${{ plan.price }}</span>
                <span class="text-base font-medium text-SecondaryColor">
                  / month
                </span>
              </h2>
              <p class="mb-8 border-b border-plusGrayColor pb-8 text-base text-SecondaryColor">
                {{ plan.description }}
              </p>
              <div class="features-list mb-4">
                <h3 class="font-semibold text-SecondaryColor">Features:</h3>
                <ul>
                  <li v-for="(feature, index) in plan.features" :key="index" class="text-SecondaryColor">
                    • {{ feature }}
                  </li>
                </ul>
              </div>
              <div class="flex justify-between mt-6">
                <button @click="editPlan(plan)"
                  class="edit-btn text-white bg-PrimaryColor hover:bg-PrimaryColorDark px-4 py-2 rounded-md">
                  Edit
                </button>
                <button @click="deletePlan(plan.type)"
                  class="delete-btn text-white bg-red-500 hover:bg-red-600 px-4 py-2 rounded-md">
                  Delete
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- Modal de edición -->
        <div v-if="selectedPlan"
          class="fixed inset-0 bg-gray-800 bg-opacity-50 flex justify-center items-center z-50 px-4">
          <div class="modal-content bg-white p-6 sm:p-8 rounded-lg shadow-lg w-full max-w-md">
            <h2 class="text-2xl font-semibold mb-4">Edit Plan</h2>
            <input v-model="selectedPlan.name" placeholder="Plan Name"
              class="input-field mb-4 border-2 border-plusGrayColor p-3 rounded-lg w-full" @input="console.log('Plan Name Updated:', selectedPlan.name)"  />
            <input v-model.number="selectedPlan.price" type="number" placeholder="Plan Price (USD)"
              class="input-field mb-4 border-2 border-plusGrayColor p-3 rounded-lg w-full" />
            <textarea v-model="selectedPlan.description" placeholder="Plan Description"
              class="input-field mb-4 border-2 border-plusGrayColor p-3 rounded-lg w-full"></textarea>
            <textarea v-model="selectedPlan.featuresString" placeholder="Plan Features (comma separated)"
              class="input-field mb-4 border-2 border-plusGrayColor p-3 rounded-lg w-full"></textarea>
            <input v-model="selectedPlan.type" placeholder="plan id (one word)" class="input-field mb-4 border-2 border-plusGrayColor p-3 rounded-lg w-full"/>

            <div class="flex justify-between mt-6">
              <button @click="updatePlan"
                class="primary-btn py-2 px-4 text-white bg-green-500 hover:bg-green-600 rounded-md">
                Save Changes
              </button>
              <button @click="cancelEdit"
                class="secondary-btn py-2 px-4 text-white bg-gray-400 hover:bg-gray-500 rounded-md">
                Cancel
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "../../axios";

export default {
  name: "PlanManagement",
  data() {
    return {
      plans: [],
      newPlan: {
        name: "",
        price: "",
        description: "",
        features: "",  // Usando "features" de manera consistente
      },
      selectedPlan: null,
    };
  },
  mounted() {
    this.fetchPlans();
  },
  methods: {
    async fetchPlans() {
      try {
        const response = await axios.get("/plans");
        this.plans = response.data.map(plan => ({
          ...plan,
          _id: plan._id || null,
          features: plan.features ? plan.features.split(",") : []
        }));
      } catch (error) {
        console.error("Error fetching plans:", error);
      }
    },
    async createPlan() {
      if (!this.newPlan.name || !this.newPlan.price || !this.newPlan.description) {
        alert("Please fill all fields");
        return;
      }

      try {
        const newPlan = {
          name: this.newPlan.name,
          price: this.newPlan.price,
          description: this.newPlan.description,
          features: this.newPlan.features,
          type: this.newPlan.type.trim(),
        };
        await axios.post("/plans", newPlan);
        this.fetchPlans();
        this.newPlan = { name: "", price: "", description: "", features: "" };
      } catch (error) {
        console.error("Error creating plan:", error);
      }
    },

    editPlan(plan) {
      console.log("Editing Plan:", plan); // Verifica el plan que se está editando
      this.selectedPlan = { ...plan, featuresString: plan.features.join(", ") };
    },

    async updatePlan() {
      if (!this.selectedPlan || !this.selectedPlan.type) {
        console.error("No plan selected or missing type");
        alert("Error: Missing type for the selected plan");
        return;
      }

      try {
        const updatedPlan = {
          name: this.selectedPlan.name.trim(),
          price: parseFloat(this.selectedPlan.price),
          description: this.selectedPlan.description.trim(),
          features: this.selectedPlan.featuresString.split(",").map(f => f.trim()).join(","),
          type: this.selectedPlan.type.trim(), // Es necesario para identificar el plan
        };

        console.log("Sending Updated Plan:", updatedPlan); // Depuración
        await axios.put(`/plans/${this.selectedPlan.type}`, updatedPlan);
        this.fetchPlans();
        this.selectedPlan = null; // Limpia el modal de edición
      } catch (error) {
        console.error("Error updating plan:", error.response?.data || error.message);
        alert(`Error updating plan: ${error.response?.data?.detail || error.message}`);
      }
    },

    async deletePlan(planType) {
      if (!confirm(`Are you sure you want to delete the plan of type '${planType}'?`)) {
        return;
      }

      try {
        console.log(`Deleting plan with type: ${planType}`); // Depuración
        await axios.delete(`/plans/${planType}`); // Usa el campo 'type' como parámetro
        this.fetchPlans(); // Refresca la lista de planes
        alert(`Plan of type '${planType}' deleted successfully`);
      } catch (error) {
        console.error("Error deleting plan:", error.response?.data || error.message);
        alert(`Error deleting plan: ${error.response?.data?.detail || error.message}`);
      }
    },

    cancelEdit() {
      this.selectedPlan = null; // Close modal
    },
  },
};
</script>

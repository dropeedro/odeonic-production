<!-- <script setup lang="ts">
import { ref } from "vue";

// Datos de los planes
const pricingPlans = ref([
  {
    id: "personal", // ID único para identificar el plan
    name: "Personal",
    price: "$5.00",
    description: "Perfect for using in a personal website or a client project.",
    features: [
      "1 User",
      "All UI components",
      "Lifetime access",
      "Free updates",
      "Use on 1 (one) project",
      "3 Months support",
    ],
    buttonText: "Choose Personal",
  },
  {
    id: "business", // ID único para identificar el plan
    name: "Business",
    price: "$10.00",
    description: "Perfect for using in a Business website or a client project.",
    features: [
      "5 Users",
      "All UI components",
      "Lifetime access",
      "Free updates",
      "Use on 3 (three) projects",
      "4 Months support",
    ],
    buttonText: "Choose Business",
  },
]);

// Función para manejar la suscripción a un plan
  const subscribeToPlan = async (planId: string, email: string) => {
  try {
    console.log("Enviando plan_id:", planId, "email:", email); // Log para depuración
    const response = await fetch("http://localhost:8000/api/create-subscription-session", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ plan_id: planId, email }),
    });

    if (!response.ok) {
      const errorDetails = await response.json();
      console.error("Error en el backend:", errorDetails); // Log para ver el detalle exacto del error
      throw new Error("Error creating Stripe session.");
    }

    const data = await response.json();
    if (data.url) {
      window.location.href = data.url; // Redirige a Stripe Checkout
    } else {
      alert("Error: No URL returned from Stripe.");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred while subscribing to the plan.");
  }
};


</script> -->

<!-- <template>
  
  <section class="pricing-section bg-backgroundColor py-12">
    <div class="container mx-auto">
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold text-PrimaryColor">Our Pricing Plans</h2>
        <p class="text-base text-SecondaryColor mt-4">
          We offer a variety of plans to suit your needs and budget. Choose the plan that
          best fits your musical goals and start exploring everything our platform has to
          offer.
        </p>
      </div>
      <div class="flex flex-wrap justify-center">
        <div
          v-for="plan in pricingPlans"
          :key="plan.id"
          class="max-w-sm mx-4 mb-8 bg-white rounded-lg shadow-md border border-stroke p-6"
        >
          <h3 class="text-xl font-bold text-PrimaryColor">{{ plan.name }}</h3>
          <p class="text-3xl font-bold text-dark mt-4">{{ plan.price }}</p>
          <p class="text-base text-SecondaryColor mt-2">{{ plan.description }}</p>
          <ul class="mt-4 mb-6 space-y-2">
            <li
              v-for="feature in plan.features"
              :key="feature"
              class="text-base text-SecondaryColor"
            >
              - {{ feature }}
            </li>
          </ul>
          <button
            @click="subscribeToPlan(plan.id, '123@example.com')" 
            class="w-full py-2 px-4 bg-PrimaryColor text-white font-medium rounded-md hover:bg-yellow-300 transition"
          >
            {{ plan.buttonText }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<style>
.pricing-section {
  background-color: #f9f9f9;
}
</style>  -->

<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";

const router = useRouter();

const pricingPlans = ref([
  {
    id: "personal",
    name: "Personal",
    price: "$5.00",
    description: "Perfect for using in a personal website or a client project.",
    features: [
      "1 User",
      "All UI components",
      "Lifetime access",
      "Free updates",
      "Use on 1 (one) project",
      "3 Months support",
    ],
    buttonText: "Choose Personal",
  },
  {
    id: "business",
    name: "Business",
    price: "$10.00",
    description: "Perfect for using in a Business website or a client project.",
    features: [
      "5 Users",
      "All UI components",
      "Lifetime access",
      "Free updates",
      "Use on 3 (three) projects",
      "4 Months support",
    ],
    buttonText: "Choose Business",
  },
]);

const subscribeToPlan = async (planId: string, email: string) => {
  try {
    const response = await fetch("http://localhost:8000/api/create-subscription-session", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ plan_id: planId, email }),
    });

    if (!response.ok) {
      throw new Error("Error creating Stripe session.");
    }

    const data = await response.json();
    if (data.url) {
      // Redirigir al usuario a Stripe Checkout
      window.location.href = data.url;
    } else {
      alert("Error: No URL returned from Stripe.");
    }
  } catch (error) {
    console.error("Error:", error);
    alert("An error occurred while subscribing to the plan.");
  }
};

const updateSubscription = async (email: string, subscriptionData: object) => {
  try {
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

    if (!response.ok) {
      throw new Error("Failed to update subscription.");
    }

    const result = await response.json();
    console.log("Subscription updated:", result);
  } catch (error) {
    console.error("Error updating subscription:", error);
  }
};

const onSuccess = async (email: string) => {
  // Datos simulados de suscripción; reemplaza esto con los valores reales si puedes recuperarlos
  const subscriptionData = {
    subscription_id: "sub_test_12345",
    status: "active",
    plan: "personal",
    start_date: Math.floor(Date.now() / 1000), // Unix timestamp actual
    end_date: Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60, // +30 días
  };

  await updateSubscription(email, subscriptionData);
  alert("Subscription updated successfully.");
  router.push("/dashboard");
};
</script>

<template>
  <section class="pricing-section bg-backgroundColor py-12">
    <div class="container mx-auto">
      <div class="text-center mb-12">
        <h2 class="text-4xl font-bold text-PrimaryColor">Our Pricing Plans</h2>
        <p class="text-base text-SecondaryColor mt-4">
          Choose the plan that best fits your goals.
        </p>
      </div>
      <div class="flex flex-wrap justify-center">
        <div
          v-for="plan in pricingPlans"
          :key="plan.id"
          class="max-w-sm mx-4 mb-8 bg-white rounded-lg shadow-md border p-6"
        >
          <h3 class="text-xl font-bold text-PrimaryColor">{{ plan.name }}</h3>
          <p class="text-3xl font-bold text-dark mt-4">{{ plan.price }}</p>
          <p class="text-base text-SecondaryColor mt-2">{{ plan.description }}</p>
          <ul class="mt-4 mb-6 space-y-2">
            <li v-for="feature in plan.features" :key="feature" class="text-base text-SecondaryColor">
              - {{ feature }}
            </li>
          </ul>
          <button
            @click="subscribeToPlan(plan.id, 'usuario@example.com')"
            class="w-full py-2 px-4 bg-PrimaryColor text-white font-medium rounded-md hover:bg-yellow-300 transition"
          >
            {{ plan.buttonText }}
          </button>
        </div>
      </div>
    </div>
  </section>
</template>

<style>
.pricing-section {
  background-color: #f9f9f9;
}
</style>
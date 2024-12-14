<template>
    <div>
      <button @click="redirectToCheckout">Pay Stripe</button>
    </div>
  </template>
  
  <script>
  import { loadStripe } from '@stripe/stripe-js';
  
  export default {
    methods: {
      async redirectToCheckout() {
        // Cargar la clave pública de Stripe
        const stripe = await loadStripe('pk_test_51N6fflGY6BYBTtJUjZVZvvWJA5oXOcB0YnVhZwG5h98S1jP2XgkPDXFa1InKHpzDzySncTf6Ym83YJM46g0PLSOL00zp7CIhww');
  
        // Hacer una solicitud al backend para crear una sesión de pago
        const response = await fetch('http://localhost:8000/create-checkout-session', {
          method: 'POST',
        });
        
        const { url } = await response.json();
  
        // Redirigir al usuario a la página de pago de Stripe
        stripe.redirectToCheckout({ sessionId: url });
      }
    }
  };
  </script>
  
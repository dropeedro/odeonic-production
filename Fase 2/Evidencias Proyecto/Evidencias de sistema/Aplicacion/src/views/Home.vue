<!-- views/Home.vue -->
<script setup>
import Plans from '../components/Plans.vue';
import Midi from '../components/Midi.vue';
import Aboutus from '../components/aboutus.vue';
</script>

<template>
  <div>
    <section id="midi">
      <div>
        <Midi></Midi>
      </div>
    </section>
    <section id="about">
      <div>
        <aboutus></aboutus>
      </div>
    </section>
    <section id="plans">
      <div>
        <Plans></Plans>
      </div>
    </section>
  </div>
</template>

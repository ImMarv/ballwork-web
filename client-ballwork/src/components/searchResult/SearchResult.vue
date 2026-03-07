<script setup lang="ts">

defineProps<{
  result: any
}>()

</script>

<template>

<div class="result-card">

  <!-- Player -->

  <div v-if="result.nationality">
    <img :src="result.photo" alt="Player Photo">
    <strong>{{ result.name }}</strong>
    <p>Date of Birth: {{ result.dob }}</p>
    <p>Position: {{ result.position }}</p>
    <p>Nationality: {{ result.nationality }}</p>
  </div>

  <!-- Team -->

  <div v-else-if="result.country && typeof result.country === 'string'">
    <img :src="result.logoUrl" alt="Team Logo" style="width: 50px; height: 50px; object-fit: contain; margin-right: 10px;">
    <strong>{{ result.name }}</strong>
    <p>{{ result.country }}</p>
  </div>

  <!-- Competition -->

  <div v-else-if="result.country && typeof result.country === 'object'">
    <strong>{{ result.name }}</strong>
    <p>{{ result.country.name }}</p>
  </div>

</div>

</template>

<style scoped src="./SearchResult.css">
</style>
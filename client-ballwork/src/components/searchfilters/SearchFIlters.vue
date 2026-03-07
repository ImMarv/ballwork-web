<script setup lang="ts">
import { ref } from 'vue';

const emit = defineEmits<{
  filterChanged: [filter: string];
}>();

const selectedFilter = ref('player'); // Default to 'player'

function onFilterChange() {
  emit('filterChanged', selectedFilter.value);
}
</script>

<template>
  <div class="search-filters">
    <label for="filter-select">Filter by:</label>
    <select id="filter-select" v-model="selectedFilter" @change="onFilterChange">
      <option value="player">Player</option>
      <option value="team">Team</option>
      <option value="competition">Competition</option>
      <option value="all">All</option>
    </select>
  </div>
</template>

<style scoped src="./SearchFilters.css">
</style>
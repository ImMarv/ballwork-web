<template>
    <div class="search-wrapper">
      <input
        type="text"
        v-model="query"
        @input="handleInput"
        placeholder="Search players, clubs..."
        class="search-input"
      />
  
      <SearchSuggestions
        v-if="showSuggestions"
        :results="results"
      />
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from "vue";
  import SearchSuggestions from "./SearchSuggestions.vue";
  import { search } from "../services/searchService";
  
  const query = ref("");
  const results = ref([]);
  const showSuggestions = ref(false);
  
  const handleInput = async () => {
    if (query.value.length < 2) {
      showSuggestions.value = false;
      return;
    }
  
    results.value = await search(query.value);
    showSuggestions.value = true;
  };
  </script>
  
  <style scoped>
  .search-wrapper {
    position: relative;
    width: 500px;
  }
  
  .search-input {
    width: 100%;
    padding: 14px 18px;
    border-radius: 25px;
    border: none;
    font-size: 1rem;
    outline: none;
  }
  </style>
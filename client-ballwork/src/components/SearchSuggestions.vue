<template>
    <ul class="suggestions">
      <li v-for="(item, index) in results" :key="index">
        {{ item }}
      </li>
    </ul>
  </template>
  
  <script setup>
  defineProps({
    results: Array
  });
  </script>
  
  <style scoped>
  .suggestions {
    position: absolute;
    top: 55px;
    width: 100%;
    background: #1f1f2e;
    border-radius: 10px;
    list-style: none;
    padding: 10px 0;
    margin: 0;
    box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
  }
  
  .suggestions li {
    padding: 10px 18px;
    cursor: pointer;
  }
  
  .suggestions li:hover {
    background: #2c2c44;
  }
  </style>
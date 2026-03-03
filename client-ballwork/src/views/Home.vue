<template>
    <div class="home">
      <h1 class="title">Ballwork</h1>
      <p class="subtitle">a football searcher</p>
  
      <SearchBar />
    </div>
  </template>
  
  <script setup>
  import SearchBar from "../components/SearchBar.vue";
  </script>
  
  <style scoped>
  .home {
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background: linear-gradient(135deg, #0f0c29, #1c1c3c);
    color: white;
  }
  
  .title {
    font-size: 4rem;
    font-weight: 700;
    margin: 0;
  }
  
  .subtitle {
    margin-top: -10px;
    margin-bottom: 30px;
    font-size: 1.2rem;
    color: #4da3ff;
  }
  </style>
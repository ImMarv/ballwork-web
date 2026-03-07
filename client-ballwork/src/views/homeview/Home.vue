<script setup lang="ts">

import { ref } from "vue"
import { useRouter } from "vue-router"

import SearchBar from "../../components/searchbar/SearchBar.vue"
import SearchFilters from "../../components/searchfilters/SearchFilters.vue"

const router = useRouter()

const selectedFilter = ref("player")

function updateFilter(filter: string) {
  selectedFilter.value = filter
}

function handleSearch(query: string) {

  if (!query.trim()) return

  router.push({
    name: "search",
    query: {
      q: query,
      type: selectedFilter.value
    }
  })

}

</script>

<template>

<div class="home">

  <h1>Ballwork</h1>
  <h2>a football searcher</h2>

  <SearchBar @search="handleSearch" />

  <SearchFilters @filterChanged="updateFilter" />

</div>

</template>

<style scoped src="./Home.css">
</style>
<script setup lang="ts">

import { ref } from "vue"

import SearchBar from "../../components/searchbar/SearchBar.vue"
import SearchFilters from "../../components/searchfilters/SearchFilters.vue"

import { statsService } from "../../services/statsService"

const selectedFilter = ref("player")

function updateFilter(filter: string) {
  selectedFilter.value = filter
}

async function handleSearch(query: string, limit: number) {

  let results

  switch (selectedFilter.value) {

    case "player":
      results = await statsService.searchPlayers(query, limit)
      break

    case "team":
      results = await statsService.searchTeams(query, limit)
      break

    case "competition":
      results = await statsService.searchCompetitions(query, limit)
      break

    case "All":
      results = await statsService.unifiedSearch(query)
      break

  }

  console.log(results)

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
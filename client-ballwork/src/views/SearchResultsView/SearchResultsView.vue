<script setup lang="ts">

import { ref, onMounted } from "vue"
import { useRoute } from "vue-router"

import { statsService } from "../../services/statsService"
import SearchResult from "../../components/searchResult/SearchResult.vue"

const route = useRoute()

const results = ref<any[]>([])

const query = route.query.q as string
const type = route.query.type as string

async function loadResults() {

  let data

  switch (type) {

    case "player":
      data = await statsService.searchPlayers(query)
      results.value = data
      break

    case "team":
      data = await statsService.searchTeams(query)
      results.value = data
      break

    case "competition":
      data = await statsService.searchCompetitions(query)
      results.value = data
      break

    case "all":
      data = await statsService.unifiedSearch(query)
      results.value = [...data.players, ...data.teams, ...data.competitions]
      break

  }

}

onMounted(loadResults)

</script>

<template>

<div class="results-view">

  <h2>Results for "{{ query }}"</h2>

  <div v-if="results.length === 0">
    No results found
  </div>

  <SearchResult
  v-for="item in results"
  :key="item.id"
  :result="item"
  />

</div>

</template>

<style scoped>

.results-view {
  max-width: 700px;
  margin: auto;
  padding-top: 40px;
}

</style>
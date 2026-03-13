<script setup lang="ts">

import { ref } from "vue"


const emit = defineEmits(["search"])

const query = ref("")

function submit() {
  emit("search", query.value)
}

</script>

<template>

<div class="search-bar">

<input
v-model="query"
placeholder="Search..."
@keyup.enter="submit"
/>

<button @click="submit">
Search
</button>

</div>

</template>
<style scoped src="./SearchBar.css">
</style>
import { createRouter, createWebHistory } from "vue-router"

import Home from "../views/homeview/Home.vue"
import SearchResultsView from "../views/SearchResultsView/SearchResultsView.vue"

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: "/",
      name: "home",
      component: Home
    },
    {
      path: "/search",
      name: "search",
      component: SearchResultsView
    }
  ]
})

export default router
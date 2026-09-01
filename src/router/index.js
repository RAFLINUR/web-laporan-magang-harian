import { createRouter, createWebHistory } from "vue-router";
import Dashboard from "../views/Dashboard.vue";
import Laporan from "../views/Laporan.vue";

const routes = [
  { path: "/", name: "dashboard", component: Dashboard },
  { path: "/laporan", name: "laporan", component: Laporan },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

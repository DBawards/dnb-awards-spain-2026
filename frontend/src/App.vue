<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed } from 'vue'
const route = useRoute()
const isHome = computed(() => route.path === '/')
</script>

<template>
  <nav v-if="!isHome" class="navbar">
    <div class="container nav-inner">
      <router-link to="/" class="logo">DnB Awards 2026</router-link>
      <div class="nav-links">
        <router-link to="/categorias">Categorías</router-link>
        <router-link to="/resultados">Resultados</router-link>
      </div>
    </div>
  </nav>
  <router-view />
</template>

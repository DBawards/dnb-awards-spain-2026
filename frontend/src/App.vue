<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed, ref } from 'vue'

const route = useRoute()
const isHome = computed(() => route.path === '/')
const menuOpen = ref(false)
</script>

<template>
  <nav v-if="!isHome" class="navbar">
    <div class="container">
      <div class="nav-inner">
        <router-link to="/" class="logo" @click="menuOpen = false">DnB Awards 2026</router-link>
        <button class="nav-toggle" :class="{ open: menuOpen }" @click="menuOpen = !menuOpen" aria-label="Menú">
          <span></span><span></span><span></span>
        </button>
        <div class="nav-links" :class="{ open: menuOpen }" @click="menuOpen = false">
          <router-link to="/categorias">Categorías</router-link>
          <router-link to="/resultados">Resultados</router-link>
        </div>
      </div>
    </div>
  </nav>
  <router-view />
</template>

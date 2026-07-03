<script setup>
import { RouterView, useRoute } from 'vue-router'
import { computed, ref, watch } from 'vue'

const route = useRoute()
const isHome = computed(() => route.path === '/')
const menuOpen = ref(false)
const transitionName = ref('slide-left')

watch(() => route.path, (to, from) => {
  const toDepth = to.split('/').length
  const fromDepth = from.split('/').length
  transitionName.value = toDepth >= fromDepth ? 'slide-left' : 'slide-right'
})
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
  <router-view v-slot="{ Component }">
    <transition :name="transitionName" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

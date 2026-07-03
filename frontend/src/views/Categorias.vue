<script setup>
import { ref, onMounted } from 'vue'
const categorias = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/categorias`)
    if (!res.ok) throw new Error('Error al cargar')
    categorias.value = await res.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="page">
    <div class="container">
      <h1>Categorías</h1>
      <p class="subtitle">Explora las categorías y vota a tus favoritos</p>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <span>Cargando categorías...</span>
      </div>
      <div v-else-if="error" class="empty">
        <p>No se pudieron cargar las categorías. Intenta de nuevo.</p>
        <router-link to="/" class="btn btn-primary">Volver al inicio</router-link>
      </div>
      <div v-else class="grid">
        <div v-for="(cat, i) in categorias" :key="cat.id" class="card card-lg">
          <span class="card-badge">{{ String(i + 1).padStart(2, '0') }}</span>
          <h2>{{ cat.nombre }}</h2>
          <p>{{ cat.descripcion }}</p>
          <router-link :to="`/votar/${cat.id}`" class="btn btn-primary">Votar</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

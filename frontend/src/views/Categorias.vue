<script setup>
import { ref, onMounted } from 'vue'
const categorias = ref([])
onMounted(async () => {
  const res = await fetch('http://localhost:8000/api/categorias')
  categorias.value = await res.json()
})
</script>

<template>
  <div class="page">
    <div class="container">
      <h1>Categorías</h1>
      <p class="subtitle">Explora las categorías y vota a tus favoritos</p>
      <div class="grid">
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

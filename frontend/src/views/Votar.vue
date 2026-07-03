<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import VoteCelebration from '../components/VoteCelebration.vue'

const props = defineProps({ id: String })
const router = useRouter()
const categoria = ref(null)
const categorias = ref([])
const nominados = ref([])
const selected = ref(null)
const voted = ref(false)
const showCelebration = ref(false)
const showConfirm = ref(false)
const voterHash = ref('')
const error = ref('')
const loading = ref(true)

const STORAGE_KEY = 'dnb_awards_voted'

const categoriaIndex = computed(() =>
  categorias.value.findIndex(c => c.id === Number(props.id))
)

const prevCategoria = computed(() =>
  categoriaIndex.value > 0 ? categorias.value[categoriaIndex.value - 1] : null
)

const nextCategoria = computed(() =>
  categoriaIndex.value < categorias.value.length - 1 ? categorias.value[categoriaIndex.value + 1] : null
)

const selectedNominee = computed(() =>
  nominados.value.find(n => n.id === selected.value)
)

const categoriesVoted = computed(() => {
  const stored = localStorage.getItem(STORAGE_KEY)
  return stored ? JSON.parse(stored) : []
})

onMounted(() => {
  voterHash.value = 'anon-' + Math.random().toString(36).slice(2, 10)
  if (categoriesVoted.value.includes(Number(props.id))) {
    voted.value = true
  }
  load()
})

async function load() {
  loading.value = true
  error.value = ''
  try {
    const [catRes, nomRes] = await Promise.all([
      fetch(`${import.meta.env.VITE_API_URL}/api/categorias`),
      fetch(`${import.meta.env.VITE_API_URL}/api/nominaciones/${props.id}`)
    ])
    if (!catRes.ok || !nomRes.ok) throw new Error('Error al cargar datos')
    categorias.value = await catRes.json()
    categoria.value = categorias.value.find(c => c.id === Number(props.id))
    nominados.value = await nomRes.json()
  } catch (e) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function abrirConfirmacion(id) {
  if (voted.value) return
  selected.value = id
  showConfirm.value = true
}

async function confirmarVoto() {
  if (!selected.value) return
  showConfirm.value = false
  error.value = ''
  try {
    const res = await fetch(`${import.meta.env.VITE_API_URL}/api/votar`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ nominacion_id: selected.value, voter_hash: voterHash.value })
    })
    if (!res.ok) {
      const data = await res.json()
      throw new Error(data.detail || 'Error al votar')
    }
    voted.value = true
    const votedList = categoriesVoted.value
    if (!votedList.includes(Number(props.id))) {
      votedList.push(Number(props.id))
      localStorage.setItem(STORAGE_KEY, JSON.stringify(votedList))
    }
    showCelebration.value = true
    load()
  } catch (e) {
    error.value = e.message
  }
}

// Swipe
let touchStartX = 0
function onTouchStart(e) {
  touchStartX = e.changedTouches[0].screenX
}
function onTouchEnd(e) {
  if (voted.value) return
  const delta = touchStartX - e.changedTouches[0].screenX
  if (Math.abs(delta) > 50) {
    if (delta > 0 && nextCategoria.value) {
      router.push(`/votar/${nextCategoria.value.id}`)
    } else if (delta < 0 && prevCategoria.value) {
      router.push(`/votar/${prevCategoria.value.id}`)
    }
  }
}
</script>

<template>
  <div class="page" @touchstart="onTouchStart" @touchend="onTouchEnd">
    <div class="container">
      <router-link to="/categorias" class="back-link">← Categorías</router-link>

      <div class="cat-progress" v-if="categorias.length">
        <span class="cat-progress-text">{{ categoriaIndex + 1 }} / {{ categorias.length }}</span>
        <div class="cat-progress-bar">
          <div class="cat-progress-fill" :style="{ width: ((categoriaIndex + 1) / categorias.length * 100) + '%' }"></div>
        </div>
      </div>

      <div v-if="loading" class="loading">
        <div class="spinner"></div>
        <span>Cargando nominaciones...</span>
      </div>

      <template v-else>
        <h1 v-if="categoria">{{ categoria.nombre }}</h1>
        <p class="subtitle" v-if="categoria">{{ categoria.descripcion }}</p>

        <div v-if="error && !loading" class="alert alert-error">{{ error }}</div>

        <div v-if="voted" class="alert alert-success">
          ¡Voto emitido correctamente!
          <span style="display:block;font-size:0.85rem;margin-top:4px;font-weight:400">Tu voto ya cuenta</span>
        </div>

        <div class="nominees">
          <div v-for="n in nominados" :key="n.id"
            :class="['nominee-card', { selected: selected === n.id }]"
            @click="abrirConfirmacion(n.id)">
            <div class="nominee-info">
              <h3>{{ n.artista }}</h3>
              <p v-if="n.track" class="track">{{ n.track }}</p>
              <p v-if="n.descripcion" class="desc">{{ n.descripcion }}</p>
            </div>
            <div class="nominee-votes">
              <span class="vote-count">{{ n.votos }}</span>
              <span class="vote-label">votos</span>
            </div>
            <div :class="['radio', { active: selected === n.id }]">
              <div class="radio-dot"></div>
            </div>
          </div>
        </div>

        <div v-if="!nominados.length && !loading && !error" class="empty">
          <p>No hay nominaciones en esta categoría todavía.</p>
        </div>

        <div class="cat-nav" v-if="categorias.length > 1">
          <router-link v-if="prevCategoria" :to="`/votar/${prevCategoria.id}`" class="btn btn-secondary btn-small">← {{ prevCategoria.nombre }}</router-link>
          <span v-else></span>
          <router-link v-if="nextCategoria" :to="`/votar/${nextCategoria.id}`" class="btn btn-secondary btn-small">{{ nextCategoria.nombre }} →</router-link>
        </div>
      </template>

      <template v-if="voted">
        <VoteCelebration v-if="showCelebration" @done="showCelebration = false" />
      </template>
    </div>
  </div>

  <Teleport to="body">
    <div v-if="showConfirm" class="sheet-overlay" @click="showConfirm = false">
      <div class="sheet" @click.stop>
        <div class="sheet-handle"></div>
        <h3 class="sheet-title">Confirmar voto</h3>
        <div class="sheet-nominee" v-if="selectedNominee">
          <strong>{{ selectedNominee.artista }}</strong>
          <span v-if="selectedNominee.track" class="track">{{ selectedNominee.track }}</span>
          <p v-if="selectedNominee.descripcion" class="desc" style="margin-top:6px;display:block">{{ selectedNominee.descripcion }}</p>
        </div>
        <p class="sheet-note">Tu voto es único por categoría. No podrás cambiarlo después.</p>
        <div class="sheet-actions">
          <button class="btn btn-primary btn-large" @click="confirmarVoto">Confirmar voto</button>
          <button class="btn btn-secondary btn-large" @click="showConfirm = false">Cancelar</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const canvas = ref(null)
let anim = null

onMounted(() => {
  const c = canvas.value
  const ctx = c.getContext('2d')
  let w, h

  function resize() {
    w = c.width = window.innerWidth
    h = c.height = window.innerHeight
  }
  resize()
  window.addEventListener('resize', resize)

  const particles = []
  const count = 60
  for (let i = 0; i < count; i++) {
    particles.push({
      x: Math.random() * w,
      y: Math.random() * h,
      size: Math.random() * 2 + 0.5,
      speedX: (Math.random() - 0.5) * 0.3,
      speedY: (Math.random() - 0.5) * 0.3 - 0.1,
      opacity: Math.random() * 0.5 + 0.05,
      hue: Math.random() > 0.5 ? 350 : 150,
    })
  }

  let phase = 0
  function draw() {
    ctx.clearRect(0, 0, w, h)
    phase += 0.005

    // Pulso suave de luz central
    const pulse = Math.sin(phase) * 0.3 + 0.5
    const grad = ctx.createRadialGradient(w / 2, h / 2, 0, w / 2, h / 2, Math.max(w, h) * 0.7)
    grad.addColorStop(0, `rgba(255, 0, 85, ${pulse * 0.06})`)
    grad.addColorStop(0.5, `rgba(0, 255, 136, ${pulse * 0.03})`)
    grad.addColorStop(1, 'rgba(0,0,0,0)')
    ctx.fillStyle = grad
    ctx.fillRect(0, 0, w, h)

    // Partículas
    particles.forEach(p => {
      p.x += p.speedX
      p.y += p.speedY

      if (p.x < 0) p.x = w
      if (p.x > w) p.x = 0
      if (p.y < 0) p.y = h
      if (p.y > h) p.y = 0

      const alpha = p.opacity + Math.sin(phase * 2 + p.x * 0.01) * 0.1
      ctx.beginPath()
      ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2)
      ctx.fillStyle = `hsla(${p.hue}, 80%, 60%, ${Math.max(0, alpha)})`
      ctx.fill()
    })

    anim = requestAnimationFrame(draw)
  }
  draw()

  onUnmounted(() => {
    cancelAnimationFrame(anim)
    window.removeEventListener('resize', resize)
  })
})
</script>

<template>
  <canvas ref="canvas" class="bg-particles" />
</template>

<style scoped>
.bg-particles {
  position: fixed;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 0;
  pointer-events: none;
}
</style>

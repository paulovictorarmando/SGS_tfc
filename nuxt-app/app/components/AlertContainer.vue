<script setup lang="ts">
const alertStore = useAlertStore()

const getAlertClass = (type: string) => {
  switch (type) {
    case 'success':
      return 'alert alert-success alert-soft shadow-lg'
    case 'error':
      return 'alert alert-error alert-soft shadow-lg'
    default:
      return 'alert alert-info alert-soft shadow-lg'
  }
}
</script>

<template>
  <div class="fixed top-4 right-4 flex flex-col gap-2 z-50">
    <div
      v-for="alert in alertStore.alerts"
      :key="alert.id"
      :class="getAlertClass(alert.type)"
    >
      <span>{{ alert.message }}</span>

      <button
        class="btn btn-xs btn-circle btn-ghost"
        @click="alertStore.removeAlert(alert.id)"
      >
        ✕
      </button>
    </div>
  </div>
</template>
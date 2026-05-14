export const useAlertStore = defineStore('alerts', () => {
  const alerts = ref<
    { id: number; message: string; type: 'error' | 'success' }[]
  >([])

  const addAlert = (message: string, type: 'error' | 'success' = 'error') => {
    const id = Date.now()

    alerts.value.push({
      id,
      message,
      type
    })

    // auto remove depois de 5s
    setTimeout(() => {
      removeAlert(id)
    }, 5000)
  }

  const removeAlert = (id: number) => {
    alerts.value = alerts.value.filter(a => a.id !== id)
  }

  return {
    alerts,
    addAlert,
    removeAlert
  }
})
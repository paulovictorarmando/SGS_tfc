export default defineNuxtRouteMiddleware((to) => {
  const publicPages = ["/login"];

  // Só executa no client
  if (import.meta.server) return;

  const accessToken = typeof window !== 'undefined' ? localStorage.getItem('access_token') : null;

  // Se não tem token e tenta acessar página privada
  if (!accessToken && !publicPages.includes(to.path)) {
    return navigateTo("/login");
  }

  // Se tem token e tenta acessar login, vai para home
  if (accessToken && to.path === "/login") {
    return navigateTo("/home");
  }
});

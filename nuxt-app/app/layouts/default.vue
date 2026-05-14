<template>
  <div class="flex flex-col min-h-screen">
    <Header />

    <div class="flex flex-1 overflow-hidden">
      <aside
        class="hidden md:block bg-base-200 border-r border-base-300 overflow-y-auto"
      >
        <Aside />
      </aside>

      <main class="flex-1 overflow-y-auto bg-base-50">
        <Main />
      </main>
    </div>
  </div>
</template>

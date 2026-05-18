<template>
  <div class="flex flex-col h-screen">
    <header class="sticky top-0 z-50">
      <Header />
    </header>

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

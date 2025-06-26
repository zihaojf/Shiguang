<script setup lang="ts">
import TheHeader from './components/TheHeader.vue'
</script>

<template>
  <div id="app">
    <TheHeader v-if="!['/login', '/register', '/login/', '/register/'].includes($route.path)" />
    <router-view></router-view>
  </div>
</template>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html,
body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
}
#app {
  width: 100%;
  height: 100%;
}
</style>

<template>
  <q-layout view="lHh Lpr lFf">
    <q-page-container>
      <q-toggle :model-value="isDarkMode" @update:model-value="toggleTheme" />
      <router-view />
      <q-page-scroller reverse position="bottom-right" :scroll-offset="20" :offset="[0, 18]">
        <q-btn fab icon="keyboard_arrow_down" color="accent" />
      </q-page-scroller>
    </q-page-container>
  </q-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useQuasar } from 'quasar'

defineOptions({
  name: 'MainLayout'
})

const $q = useQuasar()
const isDarkMode = ref($q.dark.isActive)

function toggleTheme(value: boolean) {
  isDarkMode.value = value
  $q.dark.set(value)
}
</script>

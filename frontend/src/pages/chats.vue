<script setup lang="ts">
import EncryptedMessengerService from 'src/api'
import { ref } from 'vue'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const chats = ref({
  total: 0,
  pages: 0,
  current: 1,
  data: []
})
const page = ref(1)

const socket = new WebSocket('ws://localhost:8201')

socket.onopen = (e) => {
  socket.send(
    JSON.stringify({
      type: 'listen',
      user_id: $q.cookies.get('id_access')
    })
  )
}

socket.onmessage = (event) => {
  console.log(event.data)
}

socket.onclose = () => {
  console.log('closed')
}

socket.onerror = (e) => {
  console.error(e)
}

async function getChats() {
  try {
    const { data } = await EncryptedMessengerService.getAllChats(page.value)
    chats.value = data
  } catch (e) {
    console.error(e)
  }
}

getChats()
</script>

<template>
  <q-btn to="/register">Выйти</q-btn>
  <pre>{{ chats }}</pre>
</template>

<style scoped></style>

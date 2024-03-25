<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { ChatMessageData } from 'src/api/chat/types'
import { useRoute } from 'vue-router'
import { useUserStore } from 'stores/user'
import { storeToRefs } from 'pinia'
import { FILES_PATH, FILE_FORMATS } from 'src/constants'
import { formatDate } from 'src/helpers/formatDate'
import { useChatStore } from 'stores/chat'

const route = useRoute()
const id = computed(() => route.params.id as string)

const { user } = storeToRefs(useUserStore())
const { fetchAllMessages } = useChatStore()
const { messages } = storeToRefs(useChatStore())

const messagesPage = ref(1)

async function loadMore(index, done) {
  messagesPage.value++
  await fetchAllMessages(id.value, messagesPage.value)
  done(messages.value.current > messages.value.pages)
}

const reverseMessages = computed(() => {
  return [...messages.value.data].reverse()
})

watch(
  id,
  async (value) => {
    console.log(value)
    messagesPage.value = 1
    await fetchAllMessages(value, messagesPage.value)
  },
  { immediate: true }
)

const socket = new WebSocket('ws://localhost:8201')

socket.onopen = () => {
  socket.send(
    JSON.stringify({
      type: 'listen',
      user_id: user.value.id
    })
  )
}

socket.onmessage = (event) => {
  const message: ChatMessageData = JSON.parse(event.data).data
  if (message.chat_id === id.value) {
    messages.value.data.unshift(message)
  }
}

socket.onerror = (e) => {
  console.error(e)
}
</script>

<template>
  <q-page class="chat">
    <div class="chat__messages">
      <q-infinite-scroll reverse @load="loadMore">
        <q-chat-message
          v-for="msg in reverseMessages"
          :key="msg.id"
          :sent="msg.user_id === user.id"
          :bg-color="msg.user_id === user.id ? 'accent' : 'secondary'"
          text-color="white"
        >
          <template #stamp>
            <div class="text-right">
              {{ formatDate(msg.relevance) }}
            </div>
          </template>
          <div v-if="msg.content">{{ msg.content }}</div>
          <div v-if="msg.file">
            <img
              v-if="FILE_FORMATS.includes(msg.file.split('.')[1])"
              height="350px"
              width="250px"
              :src="`${FILES_PATH}${msg.file}`"
            />
            <a v-else :href="`${FILES_PATH}${msg.file}`" download>{{ msg.file }}</a>
          </div>
        </q-chat-message>
        <template #loading>
          <div class="row justify-center q-my-md">
            <q-spinner name="dots" size="40px" />
          </div>
        </template>
      </q-infinite-scroll>
      <q-page-scroller reverse position="bottom-right" :scroll-offset="200" :offset="[15, 25]">
        <q-btn fab icon="keyboard_arrow_down" color="accent" />
      </q-page-scroller>
    </div>
  </q-page>
</template>

<style scoped lang="scss">
.chat {
  padding: 20px;
  display: flex;
  flex-direction: column;
  background-color: $main-dark;

  &__messages {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    position: relative;
  }
}
</style>

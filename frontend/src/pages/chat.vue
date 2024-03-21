<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import ChatService from 'src/api/chat'
import { AllChatMessagesData, ChatMessageData } from 'src/api/chat/types'
import { useRoute } from 'vue-router'
import { useQuasar } from 'quasar'

const $q = useQuasar()
const route = useRoute()
const id = computed(() => route.params.id as string)
const ownerId = computed(() => route.query.owner_id as string)
const messages = ref<AllChatMessagesData>({
  total: 0,
  pages: 0,
  current: 1,
  data: []
})
const message = ref('')
const file = ref<File>()
const page = ref(1)

async function fetchAllMessages() {
  try {
    const { data } = await ChatService.getAllChatMessages({
      chat_id: id.value,
      page: page.value
    })
    if (data.current > 1) {
      messages.value.current = data.current
      messages.value.data = messages.value.data.concat(data.data)
    } else {
      messages.value = data
    }
  } catch (e) {
    console.error(e)
  }
}

async function loadMore() {
  page.value++
  await fetchAllMessages()
}

async function sendMessage() {
  try {
    if (message.value) {
      const formData = new FormData()
      formData.append('chat_id', id.value)
      formData.append('content', message.value)
      if (file.value) {
        formData.append('file', file.value)
      }
      formData.append('relevance', new Date().toISOString())
      const { data } = await ChatService.addChatMessage(formData)
      messages.value.data.unshift(data)
      message.value = ''
    }
  } catch (e) {
    console.error(e)
  }
}

const reverseMessages = computed(() => {
  return [...messages.value.data].reverse()
})

watch(
  id,
  async () => {
    await fetchAllMessages()
  },
  { immediate: true }
)

const socket = new WebSocket('ws://localhost:8201')

socket.onopen = () => {
  socket.send(
    JSON.stringify({
      type: 'listen',
      user_id: $q.cookies.get('id_access')
    })
  )
}

socket.onmessage = (event) => {
  const message: ChatMessageData = JSON.parse(event.data).data
  if (message.chat_id === id.value) {
    messages.value.data.unshift(message)
  }
}

socket.onclose = () => {
  console.log('closed')
}

socket.onerror = (e) => {
  console.error(e)
}
</script>

<template>
  <q-page class="chat">
    <div class="chat__messages">
      <q-chat-message
        v-for="msg in reverseMessages"
        :key="msg.id"
        :text="[msg.content]"
        :stamp="msg.relevance"
        :sent="msg.user_id === ownerId"
        :bg-color="msg.user_id === ownerId ? 'amber-7' : 'primary'"
        text-color="white"
      >
      </q-chat-message>
      <!--          <div class="absolute-bottom-right">-->
      <!--            <q-fab color="deep-orange" icon="keyboard_arrow_down" direction="down" />-->
      <!--          </div>-->
    </div>
    <q-input
      v-model="message"
      class="chat__input"
      standout="bg-light-blue-7 text-white"
      label="Введите сообщение"
      clearable
      @keyup.enter="sendMessage"
    />
  </q-page>
</template>

<style scoped lang="scss">
.chat {
  display: flex;
  flex-direction: column;
  padding: 20px;
  background-color: $main-dark;

  &__messages {
    //max-height: calc(100vh - 126px);
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    position: relative;
    padding-right: 20px;
  }

  &__input {
    margin-top: 10px;
  }
}
</style>

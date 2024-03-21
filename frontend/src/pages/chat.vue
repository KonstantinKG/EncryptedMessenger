<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import ChatService from 'src/api/chat'
import { AllChatMessagesData, ChatMessageData } from 'src/api/chat/types'
import { useRoute } from 'vue-router'
import { useQuasar } from 'quasar'
import { useUserStore } from 'stores/user'
import { storeToRefs } from 'pinia'
import { FILES_PATH, FILE_FORMATS } from 'src/constants'
import { formatDate } from 'src/helpers/formatDate'
import { useChatStore } from 'stores/chat'

const $q = useQuasar()
const route = useRoute()
const id = computed(() => route.params.id as string)

const { user } = storeToRefs(useUserStore())
const { fetchAllMessages } = useChatStore()
const { messages, messagesPage } = storeToRefs(useChatStore())

const messagesWrapper = ref<HTMLDivElement | null>(null)

fetchAllMessages(id.value)

async function loadMore() {
  messagesPage.value++
  await fetchAllMessages(id.value)
}

const reverseMessages = computed(() => {
  return [...messages.value.data].reverse()
})

watch(
  id,
  async (value) => {
    await fetchAllMessages(value)
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
    window.scrollTo({ top: messagesWrapper.value?.scrollHeight, behavior: 'smooth' })
  }
}

socket.onerror = (e) => {
  console.error(e)
}
</script>

<template>
  <q-page class="chat">
    <div ref="messagesWrapper" class="chat__messages">
      <q-chat-message
        v-for="msg in reverseMessages"
        :key="msg.id"
        :sent="msg.user_id === user.id"
        :bg-color="msg.user_id === user.id ? 'accent' : 'primary'"
        text-color="white"
      >
        <template #stamp>
          <div class="text-right">
            {{ formatDate(msg.relevance) }}
          </div>
        </template>
        <div>{{ msg.content }}</div>
        <div v-if="msg.file">
          <q-img
            v-if="FILE_FORMATS.includes(msg.file.split('.')[1])"
            height="350px"
            width="250px"
            :src="`${FILES_PATH}${msg.file}`"
          />
          <a v-else :href="`${FILES_PATH}${msg.file}`" download>{{ msg.file }}</a>
        </div>
      </q-chat-message>
      <q-page-scroller reverse position="bottom-right" :scroll-offset="200" :offset="[15, 25]">
        <q-btn fab icon="keyboard_arrow_down" color="accent" />
      </q-page-scroller>
    </div>
    <!--    <q-toolbar class="chat__toolbar">-->
    <!--      <q-input-->
    <!--        v-model="message"-->
    <!--        class="chat__input"-->
    <!--        standout="bg-light-blue-7 text-white"-->
    <!--        label="Введите сообщение"-->
    <!--        clearable-->
    <!--        @keyup.enter="sendMessage"-->
    <!--      />-->
    <!--      <label class="cursor-pointer">-->
    <!--        <q-icon size="25px" name="attachment" class="rotate-135" />-->
    <!--        <input type="file" hidden @change="onSelectFile($event.target as HTMLInputElement)" />-->
    <!--      </label>-->
    <!--    </q-toolbar>-->
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

  //&__toolbar {
  //  margin-top: 10px;
  //  gap: 10px;
  //}
  //
  //&__input {
  //  flex: 1 1 auto;
  //}
}
</style>

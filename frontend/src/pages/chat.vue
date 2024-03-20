<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import ChatService from 'src/api/chat'
import { AllChatMessagesData } from 'src/api/chat/types'
import { useRoute } from 'vue-router'

// const messages = ref([
//   {
//     text: ['Здарова'],
//     sent: true,
//     stamps: '12:26',
//     name: '',
//     avatar: 'https://cdn.quasar.dev/img/avatar3.jpg'
//   },
//   {
//     text: ['hello'],
//     sent: false,
//     stamps: '12:27',
//     name: 'Илья',
//     avatar: 'https://cdn.quasar.dev/img/avatar5.jpg'
//   }
// ])

const route = useRoute()
const id = computed(() => route.params.id as string)
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
    const formData = new FormData()
    formData.append('chat_id', id.value)
    formData.append('content', message.value)
    if (file.value) {
      formData.append('file', file.value)
    }
    formData.append('relevance', new Date().toISOString())
    const { data } = await ChatService.addChatMessage(formData)
    messages.value.data.push(data)
    message.value = ''
  } catch (e) {
    console.error(e)
  }
}

fetchAllMessages()
</script>

<template>
  <q-page>
    <div class="chat">
      <div class="container">
        <div class="chat__messages scroll">
          <q-chat-message>
            <template #label>
              <q-badge label="16 марта" color="dark" />
            </template>
          </q-chat-message>
          <!--          <q-chat-message-->
          <!--            v-for="(msg, index) in messages.data"-->
          <!--            :key="index"-->
          <!--            :sent="msg.sent"-->
          <!--            :text="msg.content"-->
          <!--            :stamp="msg.relevance"-->
          <!--            :name="msg.name"-->
          <!--            :avatar="msg.avatar"-->
          <!--            :bg-color="msg.sent ? 'amber-7' : 'primary'"-->
          <!--            text-color="white"-->
          <!--          />-->
          <q-chat-message
            v-for="msg in messages.data"
            :key="msg.id"
            :text="msg.content"
            :stamp="msg.relevance"
            text-color="white"
          />
          <div class="absolute-bottom">
            <q-fab color="deep-orange" icon="keyboard_arrow_down" direction="down" />
          </div>
        </div>
        {{messages.data}}
        <q-input
          v-model="message"
          class="chat__input"
          standout="bg-light-blue-7 text-white"
          label="Введите сообщение"
          clearable
          @keyup.enter="sendMessage"
        />
      </div>
    </div>
  </q-page>
</template>

<style scoped lang="scss">
.chat {
  display: flex;
  flex-direction: column;
  align-items: center;
  height: 100vh;
  padding: 20px;
  background-color: $dark;

  .container {
    height: 100%;
    display: flex;
    flex-direction: column;
    max-width: 1000px;
    width: 100%;
  }

  &__messages {
    position: relative;
    padding-right: 20px;
    flex-grow: 1;
  }

  &__input {
    margin-top: 10px;
  }
}
</style>

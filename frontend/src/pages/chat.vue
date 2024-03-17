<script setup lang="ts">
import { reactive, ref } from 'vue'

const messages = reactive([
  {
    text: ['Здарова'],
    sent: true,
    stamps: '12:26',
    name: '',
    avatar: 'https://cdn.quasar.dev/img/avatar3.jpg'
  },
  {
    text: ['hello'],
    sent: false,
    stamps: '12:27',
    name: 'Илья',
    avatar: 'https://cdn.quasar.dev/img/avatar5.jpg'
  }
])

const message = ref('')

function sendMessage() {
  messages.push({
    text: [message.value],
    sent: true,
    stamps: '12:26',
    name: '',
    avatar: 'https://cdn.quasar.dev/img/avatar3.jpg'
  })
  message.value = ''
}
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
          <q-chat-message
            v-for="(msg, index) in messages"
            :key="index"
            :sent="msg.sent"
            :text="msg.text"
            :stamp="msg.stamps"
            :name="msg.name"
            :avatar="msg.avatar"
            :bg-color="msg.sent ? 'amber-7' : 'primary'"
            text-color="white"
          />
          <!--        <div class="absolute-bottom">-->
          <!--          <q-fab color="deep-orange" icon="keyboard_arrow_down" direction="down" />-->
          <!--        </div>-->
        </div>
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

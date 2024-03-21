import { defineStore } from 'pinia'
import { ref } from 'vue'
import ChatService from 'src/api/chat'
import { AllChatMessagesData } from 'src/api/chat/types'


export const useChatStore = defineStore('chat-store', () => {
  const messages = ref<AllChatMessagesData>({
    total: 0,
    pages: 0,
    current: 1,
    data: []
  })
  const message = ref('')
  const file = ref<File>()
  const messagesPage = ref(1)

  async function fetchAllMessages(id: string) {
    try {
      const { data } = await ChatService.getAllChatMessages({
        chat_id: id,
        page: messagesPage.value
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

  async function sendMessage(id: string) {
    try {
      if (message.value) {
        const formData = new FormData()
        formData.append('chat_id', id)
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


  return { message, messages, file, messagesPage, sendMessage, fetchAllMessages }
})

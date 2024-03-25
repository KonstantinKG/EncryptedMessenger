import { defineStore } from 'pinia'
import { ref } from 'vue'
import ChatService from 'src/api/chat'
import SearchService from 'src/api/search'
import { AllChatMessagesData, AllChatsData, ChatData } from 'src/api/chat/types'
import { useQuasar } from 'quasar'

export const useChatStore = defineStore('chat-store', () => {
  const chats = ref<AllChatsData>({
    total: 0,
    pages: 0,
    current: 1,
    data: []
  })
  const chatsPage = ref(1)
  const messages = ref<AllChatMessagesData>({
    total: 0,
    pages: 0,
    current: 1,
    data: []
  })
  const message = ref('')
  const file = ref<File | null>(null)
  const searchMessagesName = ref('')
  const $q = useQuasar()

  async function fetchChats() {
    try {
      const { data } = await ChatService.getAllChats(chatsPage.value)
      if (data.current > 1) {
        chats.value.current = data.current
        chats.value.data = chats.value.data.concat(data.data)
      } else {
        chats.value = data
      }
    } catch (e) {
      console.error(e)
    }
  }

  async function fetchAllMessages(id: string, page: number) {
    try {
      const { data } = await ChatService.getAllChatMessages({
        chat_id: id,
        page
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

  async function searchMessages(id: string) {
    try {
      const { data } = await SearchService.searchMessages({
        page: 1,
        content: searchMessagesName.value,
        chat_id: id
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
      const formData = new FormData()
      formData.append('chat_id', id)
      if (message.value) {
        formData.append('content', message.value)
      }
      if (file.value) {
        formData.append('file', file.value)
      }
      formData.append('relevance', new Date().toISOString())
      const { data } = await ChatService.addChatMessage(formData)
      messages.value.data.unshift(data)
      message.value = ''
      file.value = null
    } catch (e) {
      console.error(e)
    }
  }

  async function deleteChat(chat: ChatData) {
    try {
      await ChatService.deleteChat(chat.id)
      const index = chats.value.data.findIndex((el) => el.id === chat.id)
      chats.value.data.splice(index, 1)
      chats.value.total--
      $q.notify({
        message: `Чат ${chat.name} успешно удален`,
        color: 'primary',
        position: 'top-right',
        timeout: 3000,
        actions: [
          {
            icon: 'close',
            color: 'white',
            round: true,
            handler: () => {}
          }
        ]
      })
    } catch (e) {
      console.error(e)
    }
  }

  return {
    chats,
    chatsPage,
    message,
    messages,
    searchMessagesName,
    file,
    fetchChats,
    sendMessage,
    fetchAllMessages,
    searchMessages,
    deleteChat
  }
})

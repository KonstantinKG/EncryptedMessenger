import { defineStore } from 'pinia'
import { UserData } from 'src/api/users/types'
import { ref } from 'vue'
import UsersService from 'src/api/users'


export const useUserStore = defineStore('counter', () => {
  const user = ref<UserData>({
    id: '',
    username: '',
    image: null
  })

  async function getUser(id: string) {
    try {
      const { data } = await UsersService.getUser(id)
      user.value = data
    } catch (e) {
      console.error(e)
    }
  }

  return { user, getUser }
})

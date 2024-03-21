import { defineStore } from 'pinia'
import { UserData } from 'src/api/users/types'
import { ref } from 'vue'
import UsersService from 'src/api/users'


export const useUserStore = defineStore('user-store', () => {
  const user = ref<UserData>({
    id: '',
    username: '',
    image: null
  })

  async function fetchUser(id: string) {
    try {
      const { data } = await UsersService.getUser(id)
      user.value = data
    } catch (e) {
      console.error(e)
    }
  }

  async function fetchUsers(id: string) {
    try {
      const { data } = await UsersService.getAllUsers(id)
      // user.value = data
    } catch (e) {
      console.error(e)
    }
  }

  return { user, fetchUser, fetchUsers }
})

<script setup lang="ts">
import { reactive, ref } from 'vue'
import AuthService from 'src/api/auth'
import { Login } from 'src/api/auth/types'
import { useRouter } from 'vue-router'
import { useQuasar } from 'quasar'
import { useUserStore } from 'stores/user'

const store = useUserStore()
const router = useRouter()
const $q = useQuasar()
const form = reactive<Login>({
  username: '',
  password: ''
})
const isPassword = ref(true)

async function onSubmit() {
  try {
    const formData = new FormData()
    for (const key in form) {
      formData.append(key, form[key])
    }
    const { data } = await AuthService.login(formData)
    $q.cookies.set('id_access', data.id)
    await store.getUser(data.id)
    $q.notify({
      message: 'Вы вошли в аккаунт!',
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
    await router.push('/chats')
  } catch (e) {
    $q.notify({
      message: e.response.data.errors[0],
      color: 'red',
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
    console.error(e)
  }
}
</script>

<template>
  <div class="container">
    <q-form class="form" @submit.prevent="onSubmit">
      <q-input v-model="form.username" label="Введите никнейм" />
      <q-input
        v-model="form.password"
        :type="isPassword ? 'password' : 'text'"
        label="Введите пароль"
      >
        <template #append>
          <q-icon
            :name="isPassword ? 'visibility_off' : 'visibility'"
            class="cursor-pointer"
            @click="isPassword = !isPassword"
          />
        </template>
      </q-input>
      <q-btn padding="10px" color="primary" type="submit">Войти</q-btn>
      <div class="text-center">
        Нет аккаута?
        <router-link to="/register">Зарегистроваться</router-link>
      </div>
    </q-form>
  </div>
</template>

<style scoped lang="scss">
.container {
  max-width: 400px;
  margin: 0 auto;
  display: grid;
  place-items: center;
  height: 100vh;
}

.form {
  width: 100%;
  display: grid;
  gap: 20px;
  padding: 20px;
  border: 1px solid $grey-9;
  border-radius: 10px;
}
</style>

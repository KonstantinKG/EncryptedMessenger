import { api } from 'boot/axios'
import { AxiosResponse } from 'axios'
import { Login, Register, AuthData } from './types'
import type { PromiseResponse } from 'src/api/types'

class AuthService {
  private readonly RESOURCE = '/auth'

  getData = <T>(response: AxiosResponse<T>) => response.data

  async register(params: Register): PromiseResponse<AuthData> {
    return await api.post(`${this.RESOURCE}/register`, params).then(this.getData)
  }

  async login(params: Login): PromiseResponse<AuthData> {
    return await api.post(`${this.RESOURCE}/login`, params).then(this.getData)
  }
}

export default new AuthService()

import { api } from 'boot/axios'
import { AxiosResponse } from 'axios'
import { UserData, AllUsersData, SelfUpdate } from './types'
import type { PromiseResponse } from 'src/api/types'

class UsersService {
  private readonly RESOURCE = '/user'

  getData = <T>(response: AxiosResponse<T>) => response.data

  async selfUpdate(params: SelfUpdate): PromiseResponse<UserData> {
    return await api.put(`${this.RESOURCE}`, params).then(this.getData)
  }

  async selfDelete(): PromiseResponse<string> {
    return await api.delete(`${this.RESOURCE}`).then(this.getData)
  }

  async getAllUsers(page: number): PromiseResponse<AllUsersData> {
    return await api.get(`${this.RESOURCE}/all`, { params: { page } }).then(this.getData)
  }

  async getUser(id: string): PromiseResponse<UserData> {
    return await api.get(`${this.RESOURCE}`, { params: { id } }).then(this.getData)
  }
}

export default new UsersService()

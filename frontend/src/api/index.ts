import { api } from 'boot/axios'
import { AxiosResponse } from 'axios'
import {
  CreateChat,
  UpdateChat,
  Login,
  Register,
  SelfUpdate,
  AddChatMembers,
  GetAllChatMessages,
  AddChatMessage,
  SearchUsers,
  SearchMembers,
  SearchMessages,
  SearchChats
} from './types'

type PromiseResponse<T> = Promise<{ data: T }>

class EncryptedMessengerService {
  private readonly RESOURCE_CHAT = 'chat'
  private readonly RESOURCE_SEARCH = 'search'

  getData = <T>(response: AxiosResponse<T>) => response.data

  async register(params: Register): PromiseResponse<any> {
    return await api.post('/auth/register', params).then(this.getData)
  }

  async login(params: Login): PromiseResponse<any> {
    return await api.post('/auth/login', params).then(this.getData)
  }

  async update(params: SelfUpdate): PromiseResponse<any> {
    return await api.put('/user', params).then(this.getData)
  }

  async delete(): PromiseResponse<any> {
    return await api.delete('/user').then(this.getData)
  }

  async getUser(id: string): PromiseResponse<any> {
    return await api.get('/user', { params: { id } }).then(this.getData)
  }

  async getAllUsers(page: number): PromiseResponse<any> {
    return await api.get('/user/all', { params: { page } }).then(this.getData)
  }

  async getChat(chat_id: string): PromiseResponse<any> {
    return await api.get(`${this.RESOURCE_CHAT}/get`, { params: { chat_id } }).then(this.getData)
  }

  async getAllChats(page: number): PromiseResponse<any> {
    return await api.get(`${this.RESOURCE_CHAT}/all`, { params: { page } }).then(this.getData)
  }

  async createChat(params: CreateChat): PromiseResponse<any> {
    return await api.post(`${this.RESOURCE_CHAT}/all`, params).then(this.getData)
  }

  async updateChat(params: UpdateChat): PromiseResponse<any> {
    return await api.post(`${this.RESOURCE_CHAT}/all`, params).then(this.getData)
  }

  async deleteChat(id: string): PromiseResponse<any> {
    return await api.delete(`${this.RESOURCE_CHAT}/delete/${id}`).then(this.getData)
  }

  async getAllChatMembers(chat_id: string): PromiseResponse<any> {
    return await api
      .get(`${this.RESOURCE_CHAT}/members/all`, { params: { chat_id } })
      .then(this.getData)
  }

  async addChatMembers(params: AddChatMembers): PromiseResponse<any> {
    return await api.post(`${this.RESOURCE_CHAT}/members/add`, params).then(this.getData)
  }

  async getAllChatMessages(params: GetAllChatMessages): PromiseResponse<any> {
    return await api.get(`${this.RESOURCE_CHAT}/messages/all`, { params }).then(this.getData)
  }

  async addChatMessage(params: AddChatMessage): PromiseResponse<any> {
    return await api.post(`${this.RESOURCE_CHAT}/messages/add`, params).then(this.getData)
  }

  async searchUsers(params: SearchUsers): PromiseResponse<any> {
    return await api.get(`${this.RESOURCE_SEARCH}/users`, { params }).then(this.getData)
  }

  async searchMembers(params: SearchMembers): PromiseResponse<any> {
    return await api.get(`${this.RESOURCE_SEARCH}/members`, { params }).then(this.getData)
  }

  async searchMessages(params: SearchMessages): PromiseResponse<any> {
    return await api.get(`${this.RESOURCE_SEARCH}/messages`, { params }).then(this.getData)
  }

  async searchChats(params: SearchChats): PromiseResponse<any> {
    return await api.get(`${this.RESOURCE_SEARCH}/chats`, { params }).then(this.getData)
  }
}

export default new EncryptedMessengerService()

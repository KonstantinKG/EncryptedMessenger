import { api } from 'boot/axios'
import { AxiosResponse } from 'axios'
import {
  CreateChat,
  ChatData,
  AllChatsData,
  UpdateChat,
  AddChatMember,
  ChatMemberData,
  DeleteChatMember,
  AddChatMessage,
  ChatMessageData,
  GetAllChatMessages,
  AllChatMessagesData
} from './types'
import type { UserData } from 'src/api/users/types'
import type { PromiseResponse } from 'src/api/types'

class ChatService {
  private readonly RESOURCE = '/chat'

  getData = <T>(response: AxiosResponse<T>) => response.data

  async createChat(params: CreateChat): PromiseResponse<ChatData> {
    return await api.post(`${this.RESOURCE}`, params).then(this.getData)
  }

  async getAllChats(page: number): PromiseResponse<AllChatsData> {
    return await api.get(`${this.RESOURCE}/all`, { params: { page } }).then(this.getData)
  }

  async getChat(chat_id: string): PromiseResponse<ChatData> {
    return await api.get(`${this.RESOURCE}/get`, { params: { chat_id } }).then(this.getData)
  }

  async updateChat(params: UpdateChat): PromiseResponse<ChatData> {
    return await api.post(`${this.RESOURCE}/all`, params).then(this.getData)
  }

  async deleteChat(id: string): PromiseResponse<string> {
    return await api.delete(`${this.RESOURCE}`, { params: { id } }).then(this.getData)
  }

  async getAllChatMembers(chat_id: string): PromiseResponse<UserData[]> {
    return await api.get(`${this.RESOURCE}/member/all`, { params: { chat_id } }).then(this.getData)
  }

  async addChatMember(params: AddChatMember): PromiseResponse<ChatMemberData> {
    return await api.post(`${this.RESOURCE}/member/add`, params).then(this.getData)
  }

  async deleteChatMember(params: DeleteChatMember): PromiseResponse<string> {
    return await api.delete(`${this.RESOURCE}/member`, { data: params }).then(this.getData)
  }

  async addChatMessage(params: AddChatMessage): PromiseResponse<ChatMessageData> {
    return await api.post(`${this.RESOURCE}/message`, params).then(this.getData)
  }

  async getAllChatMessages(params: GetAllChatMessages): PromiseResponse<AllChatMessagesData> {
    return await api.get(`${this.RESOURCE}/message/all`, { params }).then(this.getData)
  }
}

export default new ChatService()

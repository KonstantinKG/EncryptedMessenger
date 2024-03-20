import { api } from 'boot/axios'
import { AxiosResponse } from 'axios'
import {
  SearchUsersParams,
  SearchUsersData,
  SearchMembersParams,
  SearchMembersData,
  SearchMessagesParams,
  SearchMessagesData,
  SearchChatsParams,
  SearchChatsData
} from './types'
import type { PromiseResponse } from 'src/api/types'

class SearchService {
  private readonly RESOURCE = '/search'

  getData = <T>(response: AxiosResponse<T>) => response.data

  async searchUsers(params: SearchUsersParams): PromiseResponse<SearchUsersData> {
    return await api.get(`${this.RESOURCE}/users`, { params }).then(this.getData)
  }

  async searchMembers(params: SearchMembersParams): PromiseResponse<SearchMembersData> {
    return await api.get(`${this.RESOURCE}/members`, { params }).then(this.getData)
  }

  async searchMessages(params: SearchMessagesParams): PromiseResponse<SearchMessagesData> {
    return await api.get(`${this.RESOURCE}/messages`, { params }).then(this.getData)
  }

  async searchChats(params: SearchChatsParams): PromiseResponse<SearchChatsData> {
    return await api.get(`${this.RESOURCE}/chats`, { params }).then(this.getData)
  }
}

export default new SearchService()

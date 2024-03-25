import type { Pagination } from 'src/api/types'
import type { UserData } from 'src/api/users/types'
import type { ChatMessageData, ChatData } from 'src/api/chat/types'

export interface SearchUsersParams {
  page: number
  username: string
}

export interface SearchUsersData extends Pagination {
  data: UserData[]
}

export interface SearchMembersParams extends SearchUsersParams {
  chat_id: string
}

export interface SearchMembersData extends Pagination {
  data: UserData[]
}

export interface SearchMessagesParams extends Pick<SearchMembersParams, 'page' | 'chat_id'> {
  content: string
}

export interface SearchMessagesData extends Pagination {
  data: ChatMessageData[]
}

export interface SearchChatsParams {
  page: number
  name: string
}

export interface SearchChatsData extends Pagination {
  data: ChatData[]
}

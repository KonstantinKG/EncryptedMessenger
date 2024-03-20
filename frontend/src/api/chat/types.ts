import type { Pagination } from 'src/api/types'

export interface CreateChat {
  name: string
  image?: File
  members: string[]
}

export interface ChatData {
  id: string
  name: string
  image: string | null
  owner_id: string
}

export interface AllChatsData extends Pagination {
  data: ChatData[]
}

export interface UpdateChat {
  chat_id: string
  name?: string
  image?: File
}

export interface AddChatMember {
  chat_id: string
  members: string[]
}

export interface ChatMemberData {
  chat_id: string
  user_id: string
}

export interface DeleteChatMember {
  chat_id: string
  members: string[]
}

export interface AddChatMessage {
  chat_id: string
  content?: string
  file?: File
  relevance: string
}

export interface ChatMessageData {
  id: string
  content: string
  file: string | null
  user_id: string
  chat_id: string
  relevance: string
}

export interface GetAllChatMessages {
  chat_id: string
  page: number
}

export interface AllChatMessagesData extends Pagination {
  data: ChatMessageData[]
}

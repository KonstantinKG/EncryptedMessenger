export interface Login {
  username: string
  password: string
}

export interface Register extends Login {
  image?: File
}

export interface SelfUpdate {
  username?: string
  image?: File
}

export interface CreateChat {
  name: string
  image?: File
  members: string[]
}

export interface UpdateChat {
  chat_id: string
  name?: string
  image?: File
}

export interface AddChatMembers {
  chat_id: string
  members: string[]
}

export interface GetAllChatMessages {
  chat_id: string
  page: number
}

export interface AddChatMessage {
  chat_id: string
  content?: string
  file?: File
  relevance: string
}

export interface SearchUsers {
  page: number
  username: string
}

export interface SearchMembers extends SearchUsers {
  chat_id: string
}

export interface SearchMessages extends Pick<SearchMembers, 'page' | 'chat_id'> {
  content: string
}

export interface SearchChats {
  page: number
  name: string
}

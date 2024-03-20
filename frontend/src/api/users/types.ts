import type { Pagination } from 'src/api/types'

export interface UserData {
  id: string
  username: string
  image: string | null
}

export interface AllUsersData extends Pagination {
  data: UserData[]
}

export interface SelfUpdate {
  username?: string
  image?: File
}

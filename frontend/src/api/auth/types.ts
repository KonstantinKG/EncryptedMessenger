export interface Login {
  username: string
  password: string
}

export interface Register extends Login {
  image?: File
}

export interface AuthData {
  id: string
  key: string
}

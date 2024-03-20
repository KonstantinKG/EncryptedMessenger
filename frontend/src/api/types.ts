export type PromiseResponse<T> = Promise<{ data: T }>

export interface Pagination {
  total: number
  pages: number
  current: number
}

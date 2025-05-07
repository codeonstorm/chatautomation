import { Service } from './service'

export interface User {
  id: number
  email: string
  name: string
  role: string,
  status: string,
  last_login: string | null,
  verified: boolean,
  created_at: string
  services:  Service[]
}
export interface Service {
  id: number
  plan_id: number
  status: string
  created_at: string
  expired_at: string | null
  plan: plan
}

export interface plan {
  id: number
  description: string
  billing_cycle: string
  trial_period: number
  created_at: string
  name: string
  price: number
  status: string
  features: string
  deleted_at: string | null
}
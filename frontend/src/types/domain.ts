export interface Domain {
  domain: string;
  uuid: string;
  service_id: number;
  status: string;
  created_at: string;
}

export interface DomainDeleteResponse { 
  success: boolean,
  message: string
}

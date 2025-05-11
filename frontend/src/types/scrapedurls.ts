export interface ScrapedUrls {
  id: number;
  url: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface WebCrawProgress {
  id: number;
  url: string;
  message_id: string;
  meta_data: string;
  type: string;
  status: string;
  progess: number;
  created_at: string;
  updated_at: string;
}

export interface TaskProgress {
  id: number;
  url: string;
  message_id: string;
  meta_data: string;
  type: string;
  status: string;
  progess: number;
  created_at: string;
  updated_at: string;
}
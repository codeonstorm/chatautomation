export interface Chatbot {
  name: string;
  description: string;
  behavior: string;
  system_prompt: string;
  temperature: number;
  primary_color: string;
  secondary_color: string;
  uuid: string | null;
  service_id: number | null;
  created_at: string | null;
  last_trained: string | null;
  status: 'enabled' | 'disabled';
}

 
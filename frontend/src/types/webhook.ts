export interface Webhook {
  name: string;
  description?: string | null;
  endpoint: string;
  basic_auth?: Record<string, string> | null;
  header?: Record<string, string> | null;
  status: StatusEnum;
  id: number;
  service_id: number;
  chatbot_uuid: string;
  created_at: string;
  updated_at: string;
}

export type StatusEnum = 'enabled' | 'disabled';

// Store only a single webhook per chatbot_uuid
export type WebhookState = {
  [chatbot_uuid: string]: Webhook;
};

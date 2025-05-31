export interface Entity {
  name: string;
  description?: string | null;
  entity_type: string;
  value: Record<string, string[]>;
  id: number | null;
  service_id: number | null;
  chatbot_uuid: string | null;
  created_at: string | null;
  updated_at: string | null;
}

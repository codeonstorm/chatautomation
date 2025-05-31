export interface Intent {
  name: string;
  description?: string | null;
  phrases: string[];
  default_intent_responses: string[];
  action: {
    name: string;
    webhook: boolean;
    parameters: {
      parameter: string;
      required: boolean;
      message?: string | null;
    }[];
  };
  id: number | null;
  service_id: number | null;
  chatbot_uuid: string | null;
  created_at: string | null;
  updated_at: string | null;
}
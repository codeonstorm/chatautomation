export interface ChatUser {
  uuid: string;
  session_uuid: string;
  domain_uuid: string;
  chatbot_uuid: string;
  user_data: {
    name: string | null;
    phone: string | null;
    email: string | null;
  }
  timestamp: string;
  latest_msg: {
    id: number;
    chatuser: string;
    type: string;
    msg: string;
    feedback: string;
    timestamp: string;
  }
};


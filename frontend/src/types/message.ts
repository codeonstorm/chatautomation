export interface Message {
  session_uuid: string
  msg: string
  type: "user" | "assistant"
  feedback: "positive" | "negative" | "neutral"
  timestamp: string
  senderName?: string
  senderAvatar?: string
}
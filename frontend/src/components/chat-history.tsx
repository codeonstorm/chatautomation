import { ScrollArea } from "@/components/ui/scroll-area"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { cn } from "@/lib/utils"

interface Message {
  id: string
  content: string
  sender: "user" | "bot"
  timestamp: string
  senderName: string
  senderAvatar?: string
}

interface ChatHistoryProps {
  clientId: string
}

// Mock chat history data
const chatHistories: Record<string, Message[]> = {
  "1": [
    {
      id: "1-1",
      content: "Hello! How can I help you today?",
      sender: "bot",
      timestamp: "10:00 AM",
      senderName: "Support Bot",
    },
    {
      id: "1-2",
      content: "I'm having trouble with my account. I can't log in.",
      sender: "user",
      timestamp: "10:02 AM",
      senderName: "John Doe",
    },
    {
      id: "1-3",
      content:
        "I'm sorry to hear that. Let me help you troubleshoot. Can you tell me what error message you're seeing?",
      sender: "bot",
      timestamp: "10:03 AM",
      senderName: "Support Bot",
    },
    {
      id: "1-4",
      content: "It says 'Invalid credentials' but I'm sure my password is correct.",
      sender: "user",
      timestamp: "10:05 AM",
      senderName: "John Doe",
    },
    {
      id: "1-5",
      content: "Let me check your account status. Can you confirm the email address you're using to log in?",
      sender: "bot",
      timestamp: "10:06 AM",
      senderName: "Support Bot",
    },
    {
      id: "1-6",
      content: "It's john@example.com",
      sender: "user",
      timestamp: "10:08 AM",
      senderName: "John Doe",
    },
    {
      id: "1-7",
      content:
        "Thank you. I've checked your account and it appears to be locked due to multiple failed login attempts. I've unlocked it for you. Please try logging in again.",
      sender: "bot",
      timestamp: "10:10 AM",
      senderName: "Support Bot",
    },
    {
      id: "1-8",
      content: "It worked! Thanks for your help!",
      sender: "user",
      timestamp: "10:15 AM",
      senderName: "John Doe",
    },
    {
      id: "1-9",
      content: "You're welcome! Is there anything else I can help you with today?",
      sender: "bot",
      timestamp: "10:16 AM",
      senderName: "Support Bot",
    },
    {
      id: "1-10",
      content: "No, that's all. Thank you!",
      sender: "user",
      timestamp: "10:18 AM",
      senderName: "John Doe",
    },
  ],
  "2": [
    {
      id: "2-1",
      content: "Hi there! How can I assist you today?",
      sender: "bot",
      timestamp: "Yesterday, 2:30 PM",
      senderName: "Support Bot",
    },
    {
      id: "2-2",
      content: "I'd like to know more about your premium plan.",
      sender: "user",
      timestamp: "Yesterday, 2:32 PM",
      senderName: "Jane Smith",
    },
    {
      id: "2-3",
      content:
        "Our premium plan includes advanced analytics, priority support, and unlimited API calls. It costs $49/month. Would you like more details?",
      sender: "bot",
      timestamp: "Yesterday, 2:33 PM",
      senderName: "Support Bot",
    },
    {
      id: "2-4",
      content: "Yes, please. What kind of analytics are included?",
      sender: "user",
      timestamp: "Yesterday, 2:35 PM",
      senderName: "Jane Smith",
    },
    {
      id: "2-5",
      content:
        "The analytics package includes user behavior tracking, conversion funnels, custom event tracking, and detailed reports that can be exported in various formats.",
      sender: "bot",
      timestamp: "Yesterday, 2:37 PM",
      senderName: "Support Bot",
    },
    {
      id: "2-6",
      content: "That sounds good. I'll check and get back to you.",
      sender: "user",
      timestamp: "Yesterday, 2:40 PM",
      senderName: "Jane Smith",
    },
  ],
  "3": [
    {
      id: "3-1",
      content: "Hello! Welcome to our support chat. How may I help you?",
      sender: "bot",
      timestamp: "2 days ago, 11:20 AM",
      senderName: "Support Bot",
    },
    {
      id: "3-2",
      content: "Can you help me with my account? I can't find my purchase history.",
      sender: "user",
      timestamp: "2 days ago, 11:22 AM",
      senderName: "Robert Johnson",
    },
    {
      id: "3-3",
      content:
        "I'd be happy to help you with that. To access your purchase history, please go to your account settings and click on the 'Purchase History' tab in the sidebar.",
      sender: "bot",
      timestamp: "2 days ago, 11:23 AM",
      senderName: "Support Bot",
    },
    {
      id: "3-4",
      content: "I don't see that tab in my account.",
      sender: "user",
      timestamp: "2 days ago, 11:25 AM",
      senderName: "Robert Johnson",
    },
    {
      id: "3-5",
      content: "Let me check your account type. Some features may be limited based on your subscription level.",
      sender: "bot",
      timestamp: "2 days ago, 11:26 AM",
      senderName: "Support Bot",
    },
  ],
}

export function ChatHistory({ clientId }: ChatHistoryProps) {
  const messages = chatHistories[clientId] || []

  if (messages.length === 0) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center text-muted-foreground">
          <p>No chat history available</p>
        </div>
      </div>
    )
  }

  // Group messages by date
  const groupedMessages: { date: string; messages: Message[] }[] = []
  let currentDate = ""

  messages.forEach((message) => {
    const messageDatePart = message.timestamp.includes(",") ? message.timestamp.split(",")[0] : "Today"

    if (messageDatePart !== currentDate) {
      currentDate = messageDatePart
      groupedMessages.push({
        date: currentDate,
        messages: [message],
      })
    } else {
      groupedMessages[groupedMessages.length - 1].messages.push(message)
    }
  })

  return (
    <ScrollArea className="flex-1 p-4">
      <div className="space-y-6">
        {groupedMessages.map((group, groupIndex) => (
          <div key={groupIndex} className="space-y-4">
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <span className="w-full border-t" />
              </div>
              <div className="relative flex justify-center text-xs uppercase">
                <span className="bg-background px-2 text-muted-foreground">{group.date}</span>
              </div>
            </div>

            {group.messages.map((message) => (
              <div
                key={message.id}
                className={cn("flex items-start gap-3 max-w-[80%]", message.sender === "user" ? "ml-auto" : "")}
              >
                {message.sender === "bot" && (
                  <Avatar className="h-8 w-8">
                    <AvatarImage src="/bot-avatar.png" alt="Bot" />
                    <AvatarFallback>BOT</AvatarFallback>
                  </Avatar>
                )}
                <div
                  className={cn(
                    "rounded-lg p-3",
                    message.sender === "user" ? "bg-primary text-primary-foreground" : "bg-muted",
                  )}
                >
                  <div className="mb-1 text-xs font-medium">
                    {message.senderName}
                    <span className="ml-2 text-xs font-normal opacity-70">
                      {message.timestamp.includes(",") ? message.timestamp.split(",")[1].trim() : message.timestamp}
                    </span>
                  </div>
                  <p className="text-sm">{message.content}</p>
                </div>
                {message.sender === "user" && (
                  <Avatar className="h-8 w-8">
                    <AvatarImage src={message.senderAvatar} alt={message.senderName} />
                    <AvatarFallback>{message.senderName.substring(0, 2).toUpperCase()}</AvatarFallback>
                  </Avatar>
                )}
              </div>
            ))}
          </div>
        ))}
      </div>
    </ScrollArea>
  )
}


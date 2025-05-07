"use client"

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"
import { ChatUser } from "@/types/chatuser"

// interface Client {
//   id: string
//   name: string
//   email: string
//   lastMessage: string
//   lastMessageTime: string
//   unread: number
//   avatar: string
// }

interface ClientListProps {
  clients: ChatUser[]
  selectedClientId: string | null
  onClientSelect: (clientId: string) => void
}

export function ClientList({ clients, selectedClientId, onClientSelect }: ClientListProps) {
  if (clients.length === 0) {
    return <div className="p-8 text-center text-muted-foreground">No clients found</div>
  }

  return (
    <div className="divide-y">
      {clients.map((client) => (
        <div
          key={client.uuid}
          className={cn(
            "flex items-start gap-3 p-3 cursor-pointer hover:bg-muted/50 transition-colors",
            selectedClientId === client.uuid && "bg-muted",
          )}
          onClick={() => onClientSelect(client.uuid)}
        >
          <Avatar className="h-10 w-10 flex-shrink-0">
            <AvatarImage src="" alt={client.user_data.name || "Unknown User"} />
            {/* <AvatarImage src={client.avatar} alt={client.user_data.name} /> */}
            <AvatarFallback>{client.user_data.name && client.user_data.name.substring(0, 2).toUpperCase()}</AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-medium truncate">{client.user_data.name}</h4>
              <span className="text-xs text-muted-foreground whitespace-nowrap">{client.latest_msg && client.latest_msg.timestamp.replace("T", " ")}</span>
            </div>
            <p className="text-xs text-muted-foreground truncate">{client.user_data.email}</p>
            <p className="text-xs truncate mt-1">{client.latest_msg && client.latest_msg.msg}</p>
          </div>
          {/* {client.unread > 0 && (
            <Badge variant="default" className="ml-auto">
              {client.unread}
            </Badge>
          )} */}
        </div>
      ))}
    </div>
  )
}


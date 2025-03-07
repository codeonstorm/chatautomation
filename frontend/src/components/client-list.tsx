"use client"

import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Badge } from "@/components/ui/badge"
import { cn } from "@/lib/utils"

interface Client {
  id: string
  name: string
  email: string
  lastMessage: string
  lastMessageTime: string
  unread: number
  avatar: string
}

interface ClientListProps {
  clients: Client[]
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
          key={client.id}
          className={cn(
            "flex items-start gap-3 p-3 cursor-pointer hover:bg-muted/50 transition-colors",
            selectedClientId === client.id && "bg-muted",
          )}
          onClick={() => onClientSelect(client.id)}
        >
          <Avatar className="h-10 w-10 flex-shrink-0">
            <AvatarImage src={client.avatar} alt={client.name} />
            <AvatarFallback>{client.name.substring(0, 2).toUpperCase()}</AvatarFallback>
          </Avatar>
          <div className="flex-1 min-w-0">
            <div className="flex items-center justify-between">
              <h4 className="text-sm font-medium truncate">{client.name}</h4>
              <span className="text-xs text-muted-foreground whitespace-nowrap">{client.lastMessageTime}</span>
            </div>
            <p className="text-xs text-muted-foreground truncate">{client.email}</p>
            <p className="text-xs truncate mt-1">{client.lastMessage}</p>
          </div>
          {client.unread > 0 && (
            <Badge variant="default" className="ml-auto">
              {client.unread}
            </Badge>
          )}
        </div>
      ))}
    </div>
  )
}


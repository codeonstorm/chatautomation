"use client"

import { useState } from "react"
import { Card, CardContent } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { ScrollArea } from "@/components/ui/scroll-area"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Search, Calendar, Download, Filter } from "lucide-react"
import { ClientList } from "@/components/client-list"
import { ChatHistory } from "@/components/chat-history"

// Mock data for clients
const clients = [
  {
    id: "1",
    name: "John Doe",
    email: "john@example.com",
    lastMessage: "Thanks for your help!",
    lastMessageTime: "2 hours ago",
    unread: 0,
    avatar: "",
  },
  {
    id: "2",
    name: "Jane Smith",
    email: "jane@example.com",
    lastMessage: "I'll check and get back to you",
    lastMessageTime: "Yesterday",
    unread: 2,
    avatar: "",
  },
  {
    id: "3",
    name: "Robert Johnson",
    email: "robert@example.com",
    lastMessage: "Can you help me with my account?",
    lastMessageTime: "2 days ago",
    unread: 0,
    avatar: "",
  },
  {
    id: "4",
    name: "Emily Davis",
    email: "emily@example.com",
    lastMessage: "The issue has been resolved",
    lastMessageTime: "3 days ago",
    unread: 0,
    avatar: "",
  },
  {
    id: "5",
    name: "Michael Wilson",
    email: "michael@example.com",
    lastMessage: "I need assistance with my order",
    lastMessageTime: "1 week ago",
    unread: 0,
    avatar: "",
  },
]

export default function ChatHistoryPage() {
  const [selectedClient, setSelectedClient] = useState<string | null>(null)
  const [searchQuery, setSearchQuery] = useState("")

  const filteredClients = clients.filter(
    (client) =>
      client.name.toLowerCase().includes(searchQuery.toLowerCase()) ||
      client.email.toLowerCase().includes(searchQuery.toLowerCase()),
  )

  const selectedClientData = clients.find((client) => client.id === selectedClient)

  return (
    <div className="flex-1 flex h-[calc(100vh-4rem)]">
      {/* Left sidebar - Client list */}
      <div className="w-80 border-r flex flex-col">
        <div className="p-4 border-b">
          <div className="relative">
            <Search className="absolute left-2.5 top-2.5 h-4 w-4 text-muted-foreground" />
            <Input
              type="search"
              placeholder="Search clients..."
              className="pl-8"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
        </div>
        <Tabs defaultValue="all" className="w-full">
          <div className="px-4 pt-2">
            <TabsList className="w-full">
              <TabsTrigger value="all" className="flex-1">
                All
              </TabsTrigger>
              <TabsTrigger value="unread" className="flex-1">
                Unread
              </TabsTrigger>
              <TabsTrigger value="flagged" className="flex-1">
                Flagged
              </TabsTrigger>
            </TabsList>
          </div>
          <TabsContent value="all" className="m-0">
            <ScrollArea className="h-[calc(100vh-12rem)]">
              <ClientList
                clients={filteredClients}
                selectedClientId={selectedClient}
                onClientSelect={setSelectedClient}
              />
            </ScrollArea>
          </TabsContent>
          <TabsContent value="unread" className="m-0">
            <ScrollArea className="h-[calc(100vh-12rem)]">
              <ClientList
                clients={filteredClients.filter((client) => client.unread > 0)}
                selectedClientId={selectedClient}
                onClientSelect={setSelectedClient}
              />
            </ScrollArea>
          </TabsContent>
          <TabsContent value="flagged" className="m-0">
            <div className="p-8 text-center text-muted-foreground">No flagged conversations</div>
          </TabsContent>
        </Tabs>
      </div>

      {/* Main content - Chat history */}
      <div className="flex-1 flex flex-col">
        {selectedClient ? (
          <>
            <div className="p-4 border-b flex justify-between items-center">
              <div className="flex items-center">
                <Avatar className="h-10 w-10 mr-4">
                  <AvatarImage src={selectedClientData?.avatar} alt={selectedClientData?.name} />
                  <AvatarFallback>{selectedClientData?.name.substring(0, 2).toUpperCase()}</AvatarFallback>
                </Avatar>
                <div>
                  <h2 className="text-lg font-semibold">{selectedClientData?.name}</h2>
                  <p className="text-sm text-muted-foreground">{selectedClientData?.email}</p>
                </div>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" size="sm">
                  <Calendar className="h-4 w-4 mr-2" />
                  Filter by date
                </Button>
                <Button variant="outline" size="sm">
                  <Download className="h-4 w-4 mr-2" />
                  Export
                </Button>
                <Button variant="outline" size="sm">
                  <Filter className="h-4 w-4 mr-2" />
                  Filter
                </Button>
              </div>
            </div>
            <ChatHistory clientId={selectedClient} />
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center">
            <Card className="w-[400px]">
              <CardContent className="pt-6 text-center">
                <div className="mb-4 text-muted-foreground">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="h-12 w-12 mx-auto mb-2"
                  >
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
                  </svg>
                  <h3 className="text-lg font-medium mt-2">No conversation selected</h3>
                  <p className="text-sm">Select a client from the list to view their chat history</p>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </div>
  )
}


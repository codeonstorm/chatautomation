"use client";

import React, { useEffect, useRef, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Search, Calendar, Download, Filter } from "lucide-react";
import { ClientList } from "@/components/client-list";
import { ChatHistory } from "@/components/chat-history";

import { addChatUsers } from "@/redux/store/features/chathistory/chathistory";
import { useAppDispatch } from "@/redux/store/hooks";
import type { ChatUser } from "@/types/chatuser";
import { useSelector } from "react-redux";
import type { RootState } from "@/redux/store/store";
import { getChatUsers } from "@/services/chatuser";
import { SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import { Separator } from "@radix-ui/react-separator";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { DarkModeToggle } from "@/components/darkmodetoogle";

export default function ChatHistoryPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = React.use(params);
  const dispatch = useAppDispatch();
  const fetchedRef = useRef(false);
  const chat_clients: ChatUser[] = useSelector(
    (state: RootState) => state.chatuser[id] || []
  );

  useEffect(() => {
    if (!id || fetchedRef.current) return;
    fetchedRef.current = true;
    const chatuser = async () => {
      dispatch(addChatUsers({ chatbot_uuid: id, users: [] }));
      const chatusersdata: ChatUser[] = await getChatUsers(id);
      dispatch(addChatUsers({ chatbot_uuid: id, users: chatusersdata }));
    };
    chatuser();
  }, [dispatch, id]);

  const [selectedClient, setSelectedClient] = useState<string | null>(null);
  const [searchQuery, setSearchQuery] = useState("");

  const filteredClients = chat_clients.filter(
    (client) =>
      (client.user_data?.name &&
        client.user_data.name
          .toLowerCase()
          .includes(searchQuery.toLowerCase())) ||
      (client.user_data?.email &&
        client.user_data.email
          .toLowerCase()
          .includes(searchQuery.toLowerCase()))
  );

  const selectedClientData = chat_clients.find(
    (client) => client.uuid === selectedClient
  );

  return (
    <SidebarInset>
      <header className="flex h-16 shrink-0 items-center justify-between gap-2 px-4 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12">
        {" "}
        <div className="flex items-center gap-2 px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 h-4" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem className="hidden md:block">
                <BreadcrumbLink href="/dashboard">Dashboard</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator className="hidden md:block" />
              <BreadcrumbItem>
                <BreadcrumbPage>Chatbot Traning</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>
        <DarkModeToggle />
      </header>

      <div className="flex-1 flex h-[calc(100vh-4rem)]">
        {/* <div className="flex flex-1 flex-col gap-4 p-4 pt-0"> */}
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
                      clients={filteredClients.filter((client) => 0 > 0)}
                      // clients={filteredClients.filter((client) => client.unread > 0)}
                      selectedClientId={selectedClient}
                      onClientSelect={setSelectedClient}
                    />
                  </ScrollArea>
                </TabsContent>
                <TabsContent value="flagged" className="m-0">
                  <div className="p-8 text-center text-muted-foreground">
                    No flagged conversations
                  </div>
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
                        <AvatarImage
                          src="/placeholder.svg"
                          alt={
                            selectedClientData?.user_data.name || "Unknown User"
                          }
                        />
                        <AvatarFallback>
                          {selectedClientData &&
                            selectedClientData.user_data.name &&
                            selectedClientData.user_data.name
                              .substring(0, 2)
                              .toUpperCase()}
                        </AvatarFallback>
                      </Avatar>
                      <div>
                        <h2 className="text-lg font-semibold">
                          {selectedClientData?.user_data?.name}
                        </h2>
                        <p className="text-sm text-muted-foreground">
                          {selectedClientData?.user_data?.email}
                        </p>
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
                        <h3 className="text-lg font-medium mt-2">
                          No conversation selected
                        </h3>
                        <p className="text-sm">
                          Select a client from the list to view their chat
                          history
                        </p>
                      </div>
                    </CardContent>
                  </Card>
                </div>
              )}
            </div>
          </div>
        {/* </div> */}
      </div>
    </SidebarInset>
  );
}

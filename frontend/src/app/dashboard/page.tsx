"use client"

import { AppSidebar } from "../../components/app-sidebar";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Separator } from "@/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Users, DollarSign, FolderKanban } from "lucide-react";
import { DarkModeToggle } from "@/components/darkmodetoogle";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import {
  MessageSquare,
  Globe,
  ActivityIcon as Function,
  Code,
} from "lucide-react";

import { ChatbotList } from "../../components/lists/chatbot-list";
import { DomainList } from "../../components/lists/domain-list";
import { FunctionList } from "../../components/lists/function-list";
import { EmbedCode } from "../../components/embed-code";


import { useEffect } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/context/auth-context"


// Mock data for the chart
const chartData = [
  { name: "Jan", value: 400 },
  { name: "Feb", value: 300 },
  { name: "Mar", value: 500 },
  { name: "Apr", value: 450 },
  { name: "May", value: 470 },
  { name: "Jun", value: 600 },
];

export default function Page() {
  const { isAuthenticated, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading) {
      if (isAuthenticated) {
        router.push("/dashboard")
      } else {
        router.push("/login")
      }
    }
  }, [isAuthenticated, isLoading, router])
  
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center justify-between gap-2 px-4 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12">
          <div className="flex items-center gap-2 px-4">
            <SidebarTrigger className="-ml-1" />
            <Separator orientation="vertical" className="mr-2 h-4" />
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem className="hidden md:block">
                  <BreadcrumbLink href="#">Dashboard</BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator className="hidden md:block" />
                <BreadcrumbItem>
                  <BreadcrumbPage>Overview</BreadcrumbPage>
                </BreadcrumbItem>
              </BreadcrumbList>
            </Breadcrumb>
          </div>
          <div className="px-4">
          <DarkModeToggle />
          </div>
        </header>

        <div className="flex flex-1 flex-col gap-4 p-4 pt-2">
          <div className="px-4">
            <div className="grid gap-4 md:grid-cols-4">
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    Total Chatbots
                  </CardTitle>
                  <MessageSquare className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">12</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    Active Domains
                  </CardTitle>
                  <Globe className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">8</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    Custom Functions
                  </CardTitle>
                  <Function className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">5</div>
                </CardContent>
              </Card>
              <Card>
                <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                  <CardTitle className="text-sm font-medium">
                    Total Interactions
                  </CardTitle>
                  <Code className="h-4 w-4 text-muted-foreground" />
                </CardHeader>
                <CardContent>
                  <div className="text-2xl font-bold">1,234</div>
                </CardContent>
              </Card>
            </div>

            <div className="mt-5">
              <Card>
                <CardContent>
                  <Tabs defaultValue="chatbots" className="w-full pt-6">
                    <TabsList className="py-4">
                      <TabsTrigger
                        className="data-[state=active]:bg-yellow-500 data-[state=active]:text-white px-4 py-1 rounded-md"
                        value="chatbots"
                      >
                        Chatbots
                      </TabsTrigger>
                      <TabsTrigger
                        className="data-[state=active]:bg-yellow-500 data-[state=active]:text-white px-4 py-1 rounded-md"
                        value="domains"
                      >
                        Domains
                      </TabsTrigger>
                      <TabsTrigger
                        className="data-[state=active]:bg-yellow-500 data-[state=active]:text-white px-4 py-1 rounded-md"
                        value="functions"
                      >
                        Functions
                      </TabsTrigger>
                      <TabsTrigger
                        className="data-[state=active]:bg-yellow-500 data-[state=active]:text-white px-4 py-1 rounded-md"
                        value="embed"
                      >
                        Embed Code
                      </TabsTrigger>
                    </TabsList>
                    <TabsContent value="chatbots">
                      <ChatbotList />
                    </TabsContent>
                    <TabsContent value="domains">
                      <DomainList />
                    </TabsContent>
                    <TabsContent value="functions">
                      <FunctionList />
                    </TabsContent>
                    <TabsContent value="embed">
                      <EmbedCode />
                    </TabsContent>
                  </Tabs>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}

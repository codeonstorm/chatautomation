"use client";

import { useEffect, useState } from "react";
import { Input } from "@/components/ui/input";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import {
  LineChart,
  BarChart,
  PieChart,
  Activity,
  Zap,
  Brain,
  Clock,
} from "lucide-react";
import { ClientList } from "@/components/client-list";
import { ChatHistory } from "@/components/chat-history";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Separator } from "@/components/ui/separator";
import { SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from "@/components/ui/breadcrumb";
import { DarkModeToggle } from "@/components/darkmodetoogle";
import { useAuth } from "@/context/auth-context";
import { getIngestionProgress } from "@/services/scrapedurls";
import { TaskProgress } from "@/types/scrapedurls";

export default function TrainingProgressPage() {
  // Sample training data
  const models = [
    {
      id: 1,
      name: "Chatbot Alpha",
      progress: 78,
      status: "Training",
      epochs: "34/50",
      startTime: "2 hours ago",
      estimatedCompletion: "1 hour remaining",
    },
    {
      id: 2,
      name: "Customer Support Bot",
      progress: 100,
      status: "Completed",
      epochs: "50/50",
      startTime: "Yesterday",
      estimatedCompletion: "Completed",
    },
    {
      id: 3,
      name: "Data Analyzer",
      progress: 45,
      status: "Training",
      epochs: "23/50",
      startTime: "4 hours ago",
      estimatedCompletion: "3 hours remaining",
    },
    {
      id: 4,
      name: "Content Generator",
      progress: 12,
      status: "Training",
      epochs: "6/50",
      startTime: "1 hour ago",
      estimatedCompletion: "8 hours remaining",
    },
  ];

  const {user} = useAuth()
  const [tasks, setTasks] = useState<TaskProgress[]>([])
  useEffect(() => {
    if(!user?.services[0].id) return
    const fetchTrainingData = async () => {
      try {
        const data:TaskProgress[] = await getIngestionProgress(user.services[0].id);
        setTasks(data)
        console.log(data);
      } catch (error) {
        console.error("Error fetching training data:", error);
      }
    };

    fetchTrainingData();
    const interval = setInterval(fetchTrainingData, 5000);

    return () => clearInterval(interval);
  }, [user]);

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
      
      <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
        {/* Summary Cards */}
        <div className="grid gap-4 md:grid-cols-4">
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Active Training Jobs
              </CardTitle>
              <Activity className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">3</div>
              <p className="text-xs text-muted-foreground">+2 from yesterday</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Compute Usage
              </CardTitle>
              <Zap className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">245 GPU hours</div>
              <p className="text-xs text-muted-foreground">
                +18% from last week
              </p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Models Completed
              </CardTitle>
              <Brain className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">12</div>
              <p className="text-xs text-muted-foreground">+3 this month</p>
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">
                Avg. Training Time
              </CardTitle>
              <Clock className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">8.2 hours</div>
              <p className="text-xs text-muted-foreground">
                -12% from previous
              </p>
            </CardContent>
          </Card>
        </div>

        {/* Visualization Tabs */}
        {/* <Card>
          <CardHeader>
            <CardTitle>Training Metrics</CardTitle>
            <CardDescription>
              View detailed training metrics and progress
            </CardDescription>
          </CardHeader>
          <CardContent>
            <Tabs defaultValue="progress">
              <TabsList className="mb-4">
                <TabsTrigger value="progress">
                  <LineChart className="mr-2 h-4 w-4" />
                  Progress
                </TabsTrigger>
                <TabsTrigger value="loss">
                  <BarChart className="mr-2 h-4 w-4" />
                  Loss
                </TabsTrigger>
                <TabsTrigger value="resources">
                  <PieChart className="mr-2 h-4 w-4" />
                  Resources
                </TabsTrigger>
              </TabsList>
              <TabsContent
                value="progress"
                className="h-80 rounded-md bg-muted/50 flex items-center justify-center"
              >
                <p className="text-muted-foreground">
                  Progress chart visualization would appear here
                </p>
              </TabsContent>
              <TabsContent
                value="loss"
                className="h-80 rounded-md bg-muted/50 flex items-center justify-center"
              >
                <p className="text-muted-foreground">
                  Loss metrics visualization would appear here
                </p>
              </TabsContent>
              <TabsContent
                value="resources"
                className="h-80 rounded-md bg-muted/50 flex items-center justify-center"
              >
                <p className="text-muted-foreground">
                  Resource allocation visualization would appear here
                </p>
              </TabsContent>
            </Tabs>
          </CardContent>
        </Card> */}

        {/* Active Training Jobs */}
        <Card>
          <CardHeader>
            <CardTitle>Active Training Jobs</CardTitle>
            <CardDescription>
              Monitor your ongoing model training sessions
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-6">
              {tasks.map((task) => (
                <div key={task.id} className="space-y-2">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium">{task.type}/embedding</h4>
                      {/* <p className="text-sm text-muted-foreground">
                        {task.status} • Epochs: {task.epochs}
                      </p> */}
                    </div>
                    <div className="text-right text-sm">
                      <p>Started: {task.created_at.replace('T', ' ')}</p>
                      {/* <p className="text-muted-foreground">
                        {task.estimatedCompletion}
                      </p> */}
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <progress value={task.progess} className="h-2" />
                    <span className="text-sm font-medium">
                      {task.progess}%
                    </span>
                  </div>
                  <div className="flex justify-end gap-2">
                    {task.status === "Training" && (
                      <Button variant="outline" size="sm">
                        Pause
                      </Button>
                    )}
                    <Button variant="outline" size="sm">
                      View Details
                    </Button>
                  </div>
                  {task.id !== tasks.length && <Separator className="mt-4" />}
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
    </SidebarInset>
  );
}

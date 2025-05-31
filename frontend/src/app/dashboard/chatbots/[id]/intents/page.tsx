"use client";
import { MessageSquare, Plus, Trash2 } from "lucide-react";
import Link from "next/link";

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  AlertDialogTrigger,
} from "@/components/ui/alert-dialog";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
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
import { useParams } from "next/navigation";
import { use, useEffect, useState } from "react";
import { useAuth } from "@/context/auth-context";
import { deleteIntent, getIntents } from "@/services/intents_service";
import { Intent } from "@/types/intent";

// Sample data for intents
// const intents = [
//   {
//     id: "1",
//     name: "Greeting",
//     description: "Handles user greetings",
//     trainingPhrases: 15,
//     lastUpdated: "2 days ago",
//   },
//   {
//     id: "2",
//     name: "Order Status",
//     description: "Checks status of an order",
//     trainingPhrases: 24,
//     lastUpdated: "5 hours ago",
//   },
//   {
//     id: "3",
//     name: "Product Inquiry",
//     description: "Handles questions about products",
//     trainingPhrases: 32,
//     lastUpdated: "1 day ago",
//   },
//   {
//     id: "4",
//     name: "Support Request",
//     description: "Handles customer support requests",
//     trainingPhrases: 18,
//     lastUpdated: "3 days ago",
//   },
//   {
//     id: "5",
//     name: "Feedback",
//     description: "Collects user feedback",
//     trainingPhrases: 12,
//     lastUpdated: "1 week ago",
//   },
// ];

export default function IntentsPage() {
  const { user } = useAuth();
  const params = useParams();
  const [intents, setIntents] = useState<Intent[]>([]);
  const id = params.id as string;

  useEffect(() => {
    const fetchIntent = async () => {
      if (!user) {
        // console.error("User or services not available");
        return;
      }
      try {
        const intents: Intent[] = await getIntents(user?.services[0].id, id);
        setIntents(intents);
      } catch (error) {
        // console.error("Error fetching entities:", error);
      }
    };

    fetchIntent();
  }, [user, id]);

  const handleDelete = async (intentid: string) => {
    if (!user || !user.services || user.services.length === 0) return;
    try {
      await deleteIntent(user?.services[0].id, id, intentid)
      setIntents((prev) => prev.filter((intent) => String(intent.id) != intentid));
    } catch (error) {
      console.log('itrnt not deleted')
      // Optionally handle error
    }
  };
  

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
          <div className="space-y-6 py-6">
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">Intents</h1>
                <p className="text-muted-foreground">
                  Manage and train your conversation intents.
                </p>
              </div>
              <Button asChild>
                <Link href={`/dashboard/chatbots/${id}/intents/create`}>
                  <Plus className="mr-2 h-4 w-4" />
                  Create Intent
                </Link>
              </Button>
            </div>

            <Card>
              <CardHeader>
                <CardTitle>All Intents</CardTitle>
                <CardDescription>
                  View and manage all your conversation intents.
                </CardDescription>
                <div className="flex items-center gap-2">
                  <Input placeholder="Search intents..." className="max-w-sm" />
                </div>
              </CardHeader>
              <CardContent>
                <Table>
                  <TableHeader>
                    <TableRow>
                      <TableHead>Name</TableHead>
                      <TableHead>Description</TableHead>
                      <TableHead>Training Phrases</TableHead>
                      <TableHead>Last Updated</TableHead>
                      <TableHead className="text-right">Actions</TableHead>
                    </TableRow>
                  </TableHeader>
                  <TableBody>
                    {intents.map((intent) => (
                      <TableRow key={intent.id}>
                        <TableCell className="font-medium">
                          <div className="flex items-center gap-2">
                            <MessageSquare className="h-4 w-4 text-muted-foreground" />
                            {intent.name}
                          </div>
                        </TableCell>
                        <TableCell>{intent.description}</TableCell>
                        <TableCell>{intent.phrases.length}</TableCell>
                        <TableCell>{intent.updated_at}</TableCell>
                        <TableCell className="text-right">
                          <div className="flex justify-end gap-2">
                            <Button asChild variant="ghost" size="sm">
                              <Link
                                href={`/dashboard/chatbots/${id}/intents/edit/${intent.id}`}
                              >
                                Edit
                              </Link>
                            </Button>
                            <AlertDialog>
                              <AlertDialogTrigger asChild>
                                <Button
                                  variant="outline"
                                  size="sm"
                                  className="text-red-500 hover:text-red-700"
                                >
                                  <Trash2 className="h-4 w-4 mr-1" /> Delete
                                </Button>
                              </AlertDialogTrigger>
                              <AlertDialogContent>
                                <AlertDialogHeader>
                                  <AlertDialogTitle>
                                    Are you sure?
                                  </AlertDialogTitle>
                                  <AlertDialogDescription>
                                    This action cannot be undone. This will
                                    permanently delete the chatbot and all its
                                    data.
                                  </AlertDialogDescription>
                                </AlertDialogHeader>
                                <AlertDialogFooter>
                                  <AlertDialogCancel>Cancel</AlertDialogCancel>
                                  <AlertDialogAction
                                    onClick={() => handleDelete(String(intent.id))}
                                    className="bg-red-500 hover:bg-red-700"
                                  >
                                    Delete
                                  </AlertDialogAction>
                                </AlertDialogFooter>
                              </AlertDialogContent>
                            </AlertDialog>
                            {/* <Button asChild variant="ghost" size="sm">
                              <Link
                                href={`/dashboard/intents/${intent.id}/train`}
                              >
                                Train
                              </Link>
                            </Button> */}
                          </div>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </SidebarInset>
  );
}

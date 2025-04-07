"use client";

import type React from "react";
import { fileMetaType } from "@/types/file";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Separator } from "@/components/ui/separator";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { AppSidebar } from "@/components/app-sidebar";
// import { useToast } from "@/components/ui/use-toast"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { DarkModeToggle } from "@/components/darkmodetoogle";
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
import {
  FileText,
  // Globe,
  Upload,
  Trash2,
  Play,
  File,
  FileSpreadsheet,
  FileIcon as FilePresentation,
  Eye,
} from "lucide-react";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";

import {
  MessageSquare,
  Globe,
  ActivityIcon as Function,
  Code,
} from "lucide-react";

import { getFileList } from "@/services/filemanager";
import { convertSize } from "@/lib/utils";

interface Progress {
  [key: string]: number;
}

export default function ChatbotTrainingPage() {
  const params = useParams();
  const router = useRouter();
  // const { toast } = useToast()
  const [isLoading, setIsLoading] = useState(false);
  const [chatbot, setChatbot] = useState<{ id: string; name: string } | null>(
    null
  );
  const [url, setUrl] = useState("");
  const [trainingData, setTrainingData] = useState<fileMetaType[]>([]);

  useEffect(() => {
    // In a real app, fetch the chatbot details
    setChatbot({
      id: params.id as string,
      name: `Chatbot #${params.id}`,
    });
  }, [params.id]);

  const [uploading, setUploading] = useState<boolean>(false);
  const [progress, setProgress] = useState<Progress>({});

  useEffect(() => {
    if (!chatbot) return;
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/resumablejs/resumable.js";
    script.async = true;
    document.body.appendChild(script);
    script.onload = () => {
      const r = new Resumable({
        target: "http://127.0.0.1:8000/api/v1/1/filemanager/uploads",
        chunkSize: 1 * 1024 * 1024,
        simultaneousUploads: 3,
        testChunks: true,
      });

      r.assignBrowse(document.getElementById("files") as HTMLElement);

      r.on("fileAdded", (file: any) => {
        setUploading(true);
        setProgress((prev) => ({ ...prev, [file.uniqueIdentifier]: 0 }));
        r.upload();
      });

      r.on("fileProgress", (file: any) => {
        const progressPercentage = Math.floor(file.progress() * 100);
        setProgress((prev) => ({
          ...prev,
          [file.uniqueIdentifier]: progressPercentage,
        }));
      });

      r.on("fileSuccess", (file: any) => {
        setProgress((prev) => ({ ...prev, [file.uniqueIdentifier]: 100 }));
        setUploading(false);
      });

      r.on("fileError", (file: any, message: string) => {
        alert(`Error uploading ${file.fileName}: ${message}`);
        setUploading(false);
      });
    };
  }, [chatbot]);

  useEffect(() => {
    const fetchFileList = async () => {
      try {
        const fileList = await getFileList();
        console.log(fileList); // Log the file list if you want to check its value
        setTrainingData(fileList);
      } catch (err) {
        console.error("Error fetching file list:", err);
      }
    };

    fetchFileList(); // Call the async function
  }, [params.id, uploading]);

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files;
    if (!files || files.length === 0) return;

    // In a real app, you would upload these files to your server
    // For now, we'll just add them to our local state
    const newTrainingData = Array.from(files).map((file, index) => {
      const fileType = file.name.split(".").pop()?.toUpperCase() || "Unknown";
      return {
        id: Date.now() + index,
        name: file.name,
        type: fileType,
        size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
        source: "File Upload",
        dateAdded: new Date().toISOString().split("T")[0],
      };
    });

    setTrainingData([...trainingData, ...newTrainingData]);
    // toast({
    //   title: "Files uploaded",
    //   description: `${files.length} file(s) have been added for training.`,
    // })
  };

  const handleUrlAdd = () => {
    if (!url) return;

    // Validate URL
    try {
      new URL(url);
    } catch (e) {
      // toast({
      //   variant: "destructive",
      //   title: "Invalid URL",
      //   description: "Please enter a valid URL.",
      // })
      return;
    }

    // Add URL to training data
    setTrainingData([
      ...trainingData,
      {
        id: Date.now(),
        name: url,
        type: "Website",
        source: "URL",
        dateAdded: new Date().toISOString().split("T")[0],
      },
    ]);

    // toast({
    //   title: "URL added",
    //   description: "The URL has been added for training.",
    // })
    setUrl("");
  };

  const handleDelete = (name: string) => {
    setTrainingData(trainingData.filter((item) => item.name !== name));
    // toast({
    //   title: "Item removed",
    //   description: "The training data has been removed.",
    // })
  };

  const handleStartTraining = () => {
    setIsLoading(true);

    // In a real app, you would call your API to start the training process
    setTimeout(() => {
      setIsLoading(false);
      // toast({
      //   title: "Training started",
      //   description: "Your chatbot is now being trained with the provided data.",
      // })
    }, 2000);
  };

  const getFileIcon = (type: string) => {
    switch (type) {
      case "pdf":
        return <FileText className="h-4 w-4 text-red-500" />;
      case "docx":
        return <File className="h-4 w-4 text-blue-500" />;
      case "xlsx":
        return <FileSpreadsheet className="h-4 w-4 text-green-500" />;
      case "pptx":
        return <FilePresentation className="h-4 w-4 text-orange-500" />;
      case "ppt":
        return <FilePresentation className="h-4 w-4 text-orange-500" />;
      case "website":
        return <Globe className="h-4 w-4 text-purple-500" />;
      default:
        return <File className="h-4 w-4" />;
    }
  };

  if (!chatbot) {
    return <div className="p-8">Loading...</div>;
  }

  return (
    <SidebarProvider>
      <AppSidebar />
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

            <div className="container mx-auto py-6 mt-4">
              <Card>
                <CardHeader>
                  <CardTitle>Registered Domain</CardTitle>
                  <CardDescription>
                    List of Registered domain for this chatbot.
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Name</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Size</TableHead>
                        <TableHead>Chat Preview</TableHead>
                        <TableHead>Date Added</TableHead>
                        <TableHead>Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {trainingData.length === 0 ? (
                        <TableRow>
                          <TableCell
                            colSpan={6}
                            className="text-center py-4 text-muted-foreground"
                          >
                            No training data available
                          </TableCell>
                        </TableRow>
                      ) : (
                        trainingData.map((item, i) => (
                          <TableRow key={item.name}>
                            <TableCell>
                              <div className="flex items-center gap-2">
                                {getFileIcon(item.extension)}
                                <span className="truncate max-w-[250px]">
                                  {item.name}
                                </span>
                              </div>
                            </TableCell>
                            <TableCell>{item.extension}</TableCell>
                            <TableCell>
                              {(item.size_kb && convertSize(item.size_kb)) ||
                                "N/A"}
                            </TableCell>
                            <TableCell>
                            <Button
                              variant="outline"
                              size="sm"
                              className="text-blue-500 hover:text-blue-700"
                              onClick={() => router.push(`/dashboard/chat-history`)}>
                              <Eye className="h-4 w-4 mr-1" /> Preview
                            </Button>
                            </TableCell>
                            <TableCell>{item.created_at}</TableCell>
                            <TableCell>
                              <AlertDialog>
                                <AlertDialogTrigger asChild>
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    className="text-red-500 hover:text-red-700"
                                  >
                                    <Trash2 className="h-4 w-4" />
                                  </Button>
                                </AlertDialogTrigger>
                                <AlertDialogContent>
                                  <AlertDialogHeader>
                                    <AlertDialogTitle>
                                      Are you sure?
                                    </AlertDialogTitle>
                                    <AlertDialogDescription>
                                      This will remove this item from your
                                      training data. This action cannot be
                                      undone.
                                    </AlertDialogDescription>
                                  </AlertDialogHeader>
                                  <AlertDialogFooter>
                                    <AlertDialogCancel>
                                      Cancel
                                    </AlertDialogCancel>
                                    <AlertDialogAction
                                      onClick={() => handleDelete(item.name)}
                                      className="bg-red-500 hover:bg-red-700"
                                    >
                                      Delete
                                    </AlertDialogAction>
                                  </AlertDialogFooter>
                                </AlertDialogContent>
                              </AlertDialog>
                            </TableCell>
                          </TableRow>
                        ))
                      )}
                    </TableBody>
                  </Table>
                </CardContent>
              </Card>
            </div>
          </div>
        </div>
      </SidebarInset>
    </SidebarProvider>
  );
}

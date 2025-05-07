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
import { getScrapedUrls, startWebCrawler } from "@/services/scrapedurls";
import { ScrapedUrls } from "@/types/scrapedurls";
import { useAppDispatch, useAppSelector } from "@/redux/store/hooks";
import { addUrl } from "@/redux/store/features/scrapedurl/scrapedurl";
import { RootState } from "@/redux/store/store";
import { useAuth } from "@/context/auth-context";
import { Chatbot } from "@/types/chatbot";
import { getChatbot } from "@/services/chatbot";

interface Progress {
  [key: string]: number;
}

export default function ChatbotTrainingPage() {
  const params = useParams();
  const router = useRouter();

  // urls
  const dispatch = useAppDispatch();
  const webUrls: ScrapedUrls[] = useAppSelector(
    (state: RootState) => state.scrapedurls
  );
  // const { toast } = useToast()
  const [isLoading, setIsLoading] = useState(false);
  const [chatbot, setChatbot] = useState<Chatbot | null>(
    null
  );
  const [url, setUrl] = useState("");
  const [trainingData, setTrainingData] = useState<fileMetaType[]>([]);
  const { user } = useAuth();

  useEffect(() => {
    if (!user) {
      return;
    }
    const chatbot_uuid = params.id as string;
    const fetchchatbot = async (serviceid: number, chatbot_uuid: string) => {
      const bot: Chatbot = await getChatbot(serviceid, chatbot_uuid);
      return bot;
    };
    (async () => {
      const chatbot: Chatbot = await fetchchatbot(user.services[0].id, chatbot_uuid);
      setChatbot(chatbot);
    })();
  }, [user, params.id]);

  const [uploading, setUploading] = useState<boolean>(false);
  const [progress, setProgress] = useState<Progress>({});

  useEffect(() => {
    if (!chatbot) return;
    const script = document.createElement("script");
    script.src = "https://cdn.jsdelivr.net/npm/resumablejs/resumable.js";
    script.async = true;
    document.body.appendChild(script);
    script.onload = () => {
      const r: any = new Resumable({
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
    console.log(user)
    if (!user) {
      return 
    }

    const fetchFileList = async (serviceid: number) => {
      try {
        const fileList = await getFileList(serviceid);
        console.log(fileList); // Log the file list if you want to check its value
        setTrainingData(fileList);
      } catch (err) {
        console.error("Error fetching file list:", err);
      }
    };

    fetchFileList(user?.services[0].id); // Call the async function
  }, [user, params.id, uploading]);

  // urls
  useEffect(() => {
    if (!isLoading && user) {
      const scrapedUrls = async (serviceid: number) => {
        const urls: ScrapedUrls[] = await getScrapedUrls(serviceid);
        dispatch(addUrl(urls));
      };
      scrapedUrls(user.services[0].id);
    }
  }, [user, params.id]);

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

  const handleUrlAdd = async () => {
    if (!url) return;

    // Validate URL
    // await startWebCrawler(serviceid, url);
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
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h1 className="text-3xl font-bold tracking-tight">
                      {chatbot.name} - Training
                    </h1>
                    <p className="text-muted-foreground">
                      Add training data to improve your chatbot's knowledge and
                      responses.
                    </p>
                  </div>
                  {/* <Button onClick={() => router.back()} variant="outline">
                Back to Chatbots
              </Button> */}
                </div>
              </CardHeader>
              <CardContent>
                <Tabs defaultValue="upload" className="space-y-6">
                  <TabsList>
                    <TabsTrigger value="upload">Upload Files</TabsTrigger>
                    <TabsTrigger value="url">Add URLs</TabsTrigger>
                    <TabsTrigger value="manage">
                      Manage Training Data
                    </TabsTrigger>
                  </TabsList>

                  <TabsContent value="upload">
                    <Card>
                      <CardHeader>
                        <CardTitle>Upload Training Files</CardTitle>
                        {/* <CardDescription>
                            Upload PDF, DOC, DOCX, XLS, XLSX, PPT, or PPTX files
                            to train your chatbot.
                          </CardDescription> */}
                      </CardHeader>
                      <CardContent>
                        <div className="grid w-full items-center gap-4">
                          <div className="flex flex-col space-y-1.5">
                            {/* <Label htmlFor="files">Upload Training Files</Label> */}
                            <div className="flex items-center gap-2">
                              <Input
                                className="hidden"
                                id="files"
                                type="file"
                                multiple
                                accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx"
                                onChange={handleFileUpload}
                              />
                            </div>
                            <p className="text-sm text-muted-foreground">
                              Supported file types: PDF, DOC, DOCX, XLS, XLSX,
                              PPT, PPTX
                            </p>
                          </div>
                        </div>
                      </CardContent>
                      <CardFooter className="flex justify-between">
                        <Button
                          variant="outline"
                          onClick={() =>
                            document.getElementById("files")?.click()
                          }
                        >
                          <Upload className="h-4 w-4 mr-2" /> Select Files
                        </Button>
                        {
                          <div className="mt-4">
                            {Object.entries(progress).map(([key, value]) => (
                              <div key={key} className="mb-2">
                                <span className="text-gray-600">
                                  File {key}:{" "}
                                </span>
                                <span className="font-semibold">{value}%</span>
                                <div className="w-full bg-gray-300 rounded-full h-2.5">
                                  <div
                                    className="bg-green-600 h-2.5 rounded-full"
                                    style={{ width: `${value}%` }}
                                  ></div>
                                </div>
                              </div>
                            ))}
                          </div>
                        }
                      </CardFooter>
                    </Card>
                  </TabsContent>

                  <TabsContent value="url">
                    <Card>
                      <CardHeader>
                        <CardTitle>Add URLs</CardTitle>
                        <CardDescription>
                          Add website or blog URLs to train your chatbot with
                          online content.
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <div className="grid w-full items-center gap-4">
                          <div className="flex flex-col space-y-1.5">
                            <Label htmlFor="url">Website URL</Label>
                            <div className="flex items-center gap-2">
                              <Input
                                id="url"
                                placeholder="https://example.com"
                                value={url}
                                onChange={(e) => setUrl(e.target.value)}
                              />
                              <Button onClick={handleUrlAdd}>Add</Button>
                            </div>
                            <p className="text-sm text-muted-foreground">
                              Enter the full URL including https:// or http://
                            </p>
                          </div>
                          <Table>
                            <TableHeader>
                              <TableRow>
                                <TableHead>URL</TableHead>
                                <TableHead>Status</TableHead>
                                <TableHead>Created At</TableHead>
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
                                webUrls.map((item, i) => (
                                  <TableRow key={item.id}>
                                    <TableCell>
                                      <div className="flex items-center gap-2">
                                        {getFileIcon("website")}
                                        <span className="truncate max-w-[250px]">
                                          {item.url}
                                        </span>
                                      </div>
                                    </TableCell>
                                    <TableCell>{item.status}</TableCell>
                                    <TableCell>{item.updated_at}</TableCell>
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
                                              This will remove this item from
                                              your training data. This action
                                              cannot be undone.
                                            </AlertDialogDescription>
                                          </AlertDialogHeader>
                                          <AlertDialogFooter>
                                            <AlertDialogCancel>
                                              Cancel
                                            </AlertDialogCancel>
                                            <AlertDialogAction
                                              onClick={() =>
                                                handleDelete(item.name)
                                              }
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
                        </div>
                      </CardContent>
                    </Card>
                  </TabsContent>

                  <TabsContent value="manage">
                    <Card>
                      <CardHeader>
                        <CardTitle>Manage Training Data</CardTitle>
                        <CardDescription>
                          View and manage all training data for this chatbot.
                        </CardDescription>
                      </CardHeader>
                      <CardContent>
                        <Table>
                          <TableHeader>
                            <TableRow>
                              <TableHead>Name</TableHead>
                              <TableHead>Type</TableHead>
                              <TableHead>Size</TableHead>
                              <TableHead>Source</TableHead>
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
                                    {(item.size_kb &&
                                      convertSize(item.size_kb)) ||
                                      "N/A"}
                                  </TableCell>
                                  <TableCell>{"File Upload"}</TableCell>
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
                                            onClick={() =>
                                              handleDelete(item.name)
                                            }
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
                  </TabsContent>
                </Tabs>
              </CardContent>
            </Card>

            <div className="mt-8">
              <Separator className="my-6" />
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold mb-2">Start Training</h2>
                  <p className="text-muted-foreground">
                    Train your chatbot with the data you've provided. This
                    process may take some time depending on the amount of data.
                  </p>
                </div>
                <Button
                  size="lg"
                  onClick={handleStartTraining}
                  disabled={isLoading || trainingData.length === 0}
                  className="gap-2"
                >
                  {isLoading ? (
                    <>Processing...</>
                  ) : (
                    <>
                      <Play className="h-4 w-4" /> Start Training
                    </>
                  )}
                </Button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </SidebarInset>
  );
}

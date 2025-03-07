"use client"

import type React from "react"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Separator } from "@/components/ui/separator"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { AppSidebar } from "@/components/app-sidebar"
// import { useToast } from "@/components/ui/use-toast"
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb"
import { ModeToggle } from "@/components/darkmode/modetoogle"
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
} from "@/components/ui/alert-dialog"
import {
  FileText,
  Globe,
  Upload,
  Trash2,
  Play,
  File,
  FileSpreadsheet,
  FileIcon as FilePresentation,
} from "lucide-react"
import { SidebarInset, SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"


export default function ChatbotTrainingPage() {
  const params = useParams()
  const router = useRouter()
  // const { toast } = useToast()
  const [isLoading, setIsLoading] = useState(false)
  const [chatbot, setChatbot] = useState<{ id: string; name: string } | null>(null)
  const [url, setUrl] = useState("")
  const [trainingData, setTrainingData] = useState<
    {
      id: number
      name: string
      type: string
      size?: string
      source: string
      dateAdded: string
    }[]
  >([
    {
      id: 1,
      name: "Product Documentation.pdf",
      type: "PDF",
      size: "2.4 MB",
      source: "File Upload",
      dateAdded: "2024-03-01",
    },
    {
      id: 2,
      name: "FAQ List.docx",
      type: "DOCX",
      size: "1.2 MB",
      source: "File Upload",
      dateAdded: "2024-03-02",
    },
    {
      id: 3,
      name: "https://example.com/blog",
      type: "Website",
      source: "URL",
      dateAdded: "2024-03-03",
    },
    {
      id: 4,
      name: "Sales Data.xlsx",
      type: "XLSX",
      size: "3.5 MB",
      source: "File Upload",
      dateAdded: "2024-03-04",
    },
    {
      id: 5,
      name: "Company Presentation.pptx",
      type: "PPTX",
      size: "5.1 MB",
      source: "File Upload",
      dateAdded: "2024-03-05",
    },
  ])

  useEffect(() => {
    // In a real app, fetch the chatbot details
    setChatbot({
      id: params.id as string,
      name: `Chatbot #${params.id}`,
    })
  }, [params.id])

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const files = event.target.files
    if (!files || files.length === 0) return

    // In a real app, you would upload these files to your server
    // For now, we'll just add them to our local state
    const newTrainingData = Array.from(files).map((file, index) => {
      const fileType = file.name.split(".").pop()?.toUpperCase() || "Unknown"
      return {
        id: Date.now() + index,
        name: file.name,
        type: fileType,
        size: `${(file.size / (1024 * 1024)).toFixed(1)} MB`,
        source: "File Upload",
        dateAdded: new Date().toISOString().split("T")[0],
      }
    })

    setTrainingData([...trainingData, ...newTrainingData])
    // toast({
    //   title: "Files uploaded",
    //   description: `${files.length} file(s) have been added for training.`,
    // })
  }

  const handleUrlAdd = () => {
    if (!url) return

    // Validate URL
    try {
      new URL(url)
    } catch (e) {
      // toast({
      //   variant: "destructive",
      //   title: "Invalid URL",
      //   description: "Please enter a valid URL.",
      // })
      return
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
    ])

    // toast({
    //   title: "URL added",
    //   description: "The URL has been added for training.",
    // })
    setUrl("")
  }

  const handleDelete = (id: number) => {
    setTrainingData(trainingData.filter((item) => item.id !== id))
    // toast({
    //   title: "Item removed",
    //   description: "The training data has been removed.",
    // })
  }

  const handleStartTraining = () => {
    setIsLoading(true)

    // In a real app, you would call your API to start the training process
    setTimeout(() => {
      setIsLoading(false)
      // toast({
      //   title: "Training started",
      //   description: "Your chatbot is now being trained with the provided data.",
      // })
    }, 2000)
  }

  const getFileIcon = (type: string) => {
    switch (type) {
      case "PDF":
        return <FileText className="h-4 w-4 text-red-500" />
      case "DOCX":
        return <File className="h-4 w-4 text-blue-500" />
      case "XLSX":
        return <FileSpreadsheet className="h-4 w-4 text-green-500" />
      case "PPTX":
        return <FilePresentation className="h-4 w-4 text-orange-500" />
      case "Website":
        return <Globe className="h-4 w-4 text-purple-500" />
      default:
        return <File className="h-4 w-4" />
    }
  }

  if (!chatbot) {
    return <div className="p-8">Loading...</div>
  }

  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <header className="flex h-16 shrink-0 items-center justify-between gap-2 px-4 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12">          <div className="flex items-center gap-2 px-4">
            <SidebarTrigger className="-ml-1" />
            <Separator orientation="vertical" className="mr-2 h-4" />
            <Breadcrumb>
              <BreadcrumbList>
                <BreadcrumbItem className="hidden md:block">
                  <BreadcrumbLink href="#">Dashboard</BreadcrumbLink>
                </BreadcrumbItem>
                <BreadcrumbSeparator className="hidden md:block" />
                <BreadcrumbItem>
                  <BreadcrumbPage>Chatbot Traning</BreadcrumbPage>
                </BreadcrumbItem>
              </BreadcrumbList>
            </Breadcrumb>
          </div>
        <ModeToggle/>
       </header>
        <div className="flex flex-1 flex-col gap-4 p-4 pt-2">

          <div className="container mx-auto py-6">
            <div className="flex items-center justify-between mb-6">
              <div>
                <h1 className="text-3xl font-bold tracking-tight">{chatbot.name} - Training</h1>
                <p className="text-muted-foreground">Add training data to improve your chatbot's knowledge and responses.</p>
              </div>
              <Button onClick={() => router.back()} variant="outline">
                Back to Chatbots
              </Button>
            </div>

            <Tabs defaultValue="upload" className="space-y-6">
              <TabsList>
                <TabsTrigger value="upload">Upload Files</TabsTrigger>
                <TabsTrigger value="url">Add URLs</TabsTrigger>
                <TabsTrigger value="manage">Manage Training Data</TabsTrigger>
              </TabsList>

              <TabsContent value="upload">
                <Card>
                  <CardHeader>
                    <CardTitle>Upload Training Files</CardTitle>
                    <CardDescription>
                      Upload PDF, DOC, DOCX, XLS, XLSX, PPT, or PPTX files to train your chatbot.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <div className="grid w-full items-center gap-4">
                      <div className="flex flex-col space-y-1.5">
                        <Label htmlFor="files">Files</Label>
                        <div className="flex items-center gap-2">
                          <Input
                            id="files"
                            type="file"
                            multiple
                            accept=".pdf,.doc,.docx,.xls,.xlsx,.ppt,.pptx"
                            onChange={handleFileUpload}
                          />
                        </div>
                        <p className="text-sm text-muted-foreground">
                          Supported file types: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX
                        </p>
                      </div>
                    </div>
                  </CardContent>
                  <CardFooter className="flex justify-between">
                    <Button variant="outline" onClick={() => document.getElementById("files")?.click()}>
                      <Upload className="h-4 w-4 mr-2" /> Select Files
                    </Button>
                  </CardFooter>
                </Card>
              </TabsContent>

              <TabsContent value="url">
                <Card>
                  <CardHeader>
                    <CardTitle>Add URLs</CardTitle>
                    <CardDescription>Add website or blog URLs to train your chatbot with online content.</CardDescription>
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
                        <p className="text-sm text-muted-foreground">Enter the full URL including https:// or http://</p>
                      </div>
                    </div>
                  </CardContent>
                </Card>
              </TabsContent>

              <TabsContent value="manage">
                <Card>
                  <CardHeader>
                    <CardTitle>Manage Training Data</CardTitle>
                    <CardDescription>View and manage all training data for this chatbot.</CardDescription>
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
                            <TableCell colSpan={6} className="text-center py-4 text-muted-foreground">
                              No training data available
                            </TableCell>
                          </TableRow>
                        ) : (
                          trainingData.map((item) => (
                            <TableRow key={item.id}>
                              <TableCell>
                                <div className="flex items-center gap-2">
                                  {getFileIcon(item.type)}
                                  <span className="truncate max-w-[250px]">{item.name}</span>
                                </div>
                              </TableCell>
                              <TableCell>{item.type}</TableCell>
                              <TableCell>{item.size || "N/A"}</TableCell>
                              <TableCell>{item.source}</TableCell>
                              <TableCell>{item.dateAdded}</TableCell>
                              <TableCell>
                                <AlertDialog>
                                  <AlertDialogTrigger asChild>
                                    <Button variant="ghost" size="sm" className="text-red-500 hover:text-red-700">
                                      <Trash2 className="h-4 w-4" />
                                    </Button>
                                  </AlertDialogTrigger>
                                  <AlertDialogContent>
                                    <AlertDialogHeader>
                                      <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                                      <AlertDialogDescription>
                                        This will remove this item from your training data. This action cannot be undone.
                                      </AlertDialogDescription>
                                    </AlertDialogHeader>
                                    <AlertDialogFooter>
                                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                                      <AlertDialogAction
                                        onClick={() => handleDelete(item.id)}
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

            <div className="mt-8">
              <Separator className="my-6" />
              <div className="flex items-center justify-between">
                <div>
                  <h2 className="text-xl font-semibold mb-2">Start Training</h2>
                  <p className="text-muted-foreground">
                    Train your chatbot with the data you've provided. This process may take some time depending on the amount
                    of data.
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
      </SidebarInset>
    </SidebarProvider>
  )
}


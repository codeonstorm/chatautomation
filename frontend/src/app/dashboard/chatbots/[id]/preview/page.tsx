"use client"

import { useState, useEffect } from "react"
import { useParams, useRouter } from "next/navigation"
import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Separator } from "@/components/ui/separator"
import { Switch } from "@/components/ui/switch"
import { Label } from "@/components/ui/label"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Laptop, Smartphone, Tablet, ArrowLeft, ExternalLink, Maximize2, Minimize2 } from "lucide-react"
import { Chatbot } from "@/types/chatbot"
import { RootState } from "@/redux/store/store"
import { useSelector } from "react-redux"
import { getChatbot } from "@/services/chatbot"
import { useAuth } from "@/context/auth-context"
import { SidebarInset, SidebarTrigger } from "@/components/ui/sidebar"
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from "@/components/ui/breadcrumb"
import { DarkModeToggle } from "@/components/darkmodetoogle"

export default function ChatbotPreviewPage() {
  const params = useParams()
  const router = useRouter()
  const [chatbot, setChatbot] = useState<Chatbot | null>(null)
  const [device, setDevice] = useState<"mobile" | "tablet" | "desktop">("desktop")
  const [orientation, setOrientation] = useState<"portrait" | "landscape">("portrait")
  const [darkMode, setDarkMode] = useState(false)
  const [fullscreen, setFullscreen] = useState(false)
  const [theme, setTheme] = useState<"light" | "dark" | "system">("light")
  const { user } = useAuth()


  useEffect(() => {
    if (!user || !params.id) {
      console.log("Error: ", "Invalid user")
      return
    }
    const chatbot_uuid = params.id as string;
    const fetchChatbot = async (serviceid: number, chatbot_uuid: string) => {
      const chatbot:Chatbot = await getChatbot(serviceid, chatbot_uuid);
      setChatbot(chatbot);
    };

    fetchChatbot(user.services[0].id, chatbot_uuid);

  }, [user, params.id])

  const getDeviceStyles = () => {
    switch (device) {
      case "mobile":
        return orientation === "portrait" ? { width: "375px", height: "667px" } : { width: "667px", height: "375px" }
      case "tablet":
        return orientation === "portrait" ? { width: "768px", height: "1024px" } : { width: "1024px", height: "768px" }
      case "desktop":
        return { width: "100%", height: "800px", maxWidth: "1280px" }
    }
  }

  const getDeviceFrame = () => {
    switch (device) {
      case "mobile":
        return "rounded-[36px] border-[16px] border-gray-800"
      case "tablet":
        return "rounded-[24px] border-[16px] border-gray-800"
      case "desktop":
        return "rounded-lg border border-gray-300 shadow-sm"
    }
  }

  if (!chatbot) {
    return <div className="p-8">Loading...</div>
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

      <div className="flex-1 flex h-[calc(100vh-4rem)]">
        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">

    <div className={`container mx-auto py-6 px-4 ${darkMode ? "dark" : ""}`}>
      <div className="flex items-center justify-between mb-6">
        <div className="flex items-center gap-2">
          {/* <Button variant="outline" size="icon" onClick={() => router.back()}>
            <ArrowLeft className="h-4 w-4" />
          </Button> */}
          <div>
            <h1 className="text-2xl font-bold tracking-tight">{chatbot.name} - Preview</h1>
            <p className="text-muted-foreground">Preview how your chatbot appears on different devices</p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-[300px_1fr] gap-6">
        {/* Controls sidebar */}
        <div className="space-y-6">
        <Card>
            <CardContent className="p-6">
              <h2 className="text-lg font-semibold mb-4">Chatbot Information</h2>
              <div className="space-y-4">
                <div>
                  <Label className="text-sm text-muted-foreground">Name</Label>
                  <p className="font-medium">{chatbot.name}</p>
                    <p className="font-medium">
                    {chatbot.description.length > 100
                      ? `${chatbot.description.substring(0, 100)}...`
                      : chatbot.description}
                    </p>
                </div>
                <div>
                  <Label className="text-sm text-muted-foreground">Primary Color</Label>
                  <div className="flex items-center gap-2 mt-1">
                    <div className="w-6 h-6 rounded-full border" style={{ backgroundColor: chatbot.primary_color }} />
                    <span>{chatbot.primary_color}</span>
                  </div>
                </div>
                <div className="pt-2">
                  <Button
                    variant="outline"
                    className="w-full flex items-center justify-center gap-2"
                    onClick={() => window.open(`/preview/${chatbot.id}`, "_blank")}
                  >
                    <ExternalLink className="h-4 w-4" />
                    Open in New Tab
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
          <Card>
            <CardContent className="p-6">
              <h2 className="text-lg font-semibold mb-4">Preview Settings</h2>

              <div className="space-y-6">
                <div className="space-y-2">
                  <h3 className="text-sm font-medium">Device</h3>
                  <Tabs
                    defaultValue={device}
                    onValueChange={(value) => setDevice(value as "mobile" | "tablet" | "desktop")}
                    className="w-full"
                  >
                    <TabsList className="grid grid-cols-3 w-full">
                      <TabsTrigger value="mobile" className="flex items-center gap-1">
                        <Smartphone className="h-4 w-4" />
                        <span className="hidden sm:inline">Mobile</span>
                      </TabsTrigger>
                      <TabsTrigger value="tablet" className="flex items-center gap-1">
                        <Tablet className="h-4 w-4" />
                        <span className="hidden sm:inline">Tablet</span>
                      </TabsTrigger>
                      <TabsTrigger value="desktop" className="flex items-center gap-1">
                        <Laptop className="h-4 w-4" />
                        <span className="hidden sm:inline">Desktop</span>
                      </TabsTrigger>
                    </TabsList>
                  </Tabs>
                </div>

                {device !== "desktop" && (
                  <div className="flex items-center justify-between">
                    <Label htmlFor="orientation" className="text-sm font-medium">
                      Orientation
                    </Label>
                    <div className="flex items-center space-x-2">
                      <Label htmlFor="orientation" className="text-sm text-muted-foreground">
                        Portrait
                      </Label>
                      <Switch
                        id="orientation"
                        checked={orientation === "landscape"}
                        onCheckedChange={(checked) => setOrientation(checked ? "landscape" : "portrait")}
                      />
                      <Label htmlFor="orientation" className="text-sm text-muted-foreground">
                        Landscape
                      </Label>
                    </div>
                  </div>
                )}

                <Separator />

                <div className="space-y-4">
                  <div className="flex items-center justify-between">
                    <Label htmlFor="dark-mode" className="text-sm font-medium">
                      Dark Mode
                    </Label>
                    <Switch id="dark-mode" checked={darkMode} onCheckedChange={setDarkMode} />
                  </div>

                  <div className="space-y-2">
                    <Label htmlFor="theme" className="text-sm font-medium">
                      Theme
                    </Label>
                    <Select value={theme} onValueChange={(value) => setTheme(value as "light" | "dark" | "system")}>
                      <SelectTrigger id="theme">
                        <SelectValue placeholder="Select theme" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="light">Light</SelectItem>
                        <SelectItem value="dark">Dark</SelectItem>
                        <SelectItem value="system">System</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>
                </div>

                <Separator />

                <div className="pt-2">
                  <Button
                    variant="outline"
                    className="w-full flex items-center justify-center gap-2"
                    onClick={() => setFullscreen(!fullscreen)}
                  >
                    {fullscreen ? (
                      <>
                        <Minimize2 className="h-4 w-4" />
                        Exit Fullscreen
                      </>
                    ) : (
                      <>
                        <Maximize2 className="h-4 w-4" />
                        Fullscreen Preview
                      </>
                    )}
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Preview area */}
        <div className={fullscreen ? "fixed inset-0 bg-background z-50 p-6 flex items-center justify-center" : ""}>
          {fullscreen && (
            <Button
              variant="outline"
              size="icon"
              className="absolute top-4 right-4"
              onClick={() => setFullscreen(false)}
            >
              <Minimize2 className="h-4 w-4" />
            </Button>
          )}

          <div className="w-full h-full flex items-center justify-center overflow-auto p-4">
            <div className={`bg-white dark:bg-gray-900 overflow-hidden ${getDeviceFrame()}`} style={getDeviceStyles()}>
              <div className="w-full h-full bg-white dark:bg-gray-900 overflow-hidden relative">
                {/* Website mockup */}
                <div className="w-full h-12 bg-gray-100 dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 flex items-center px-4">
                  <div className="w-full max-w-md mx-auto flex items-center">
                    <div className="w-3 h-3 rounded-full bg-red-500 mr-2"></div>
                    <div className="w-3 h-3 rounded-full bg-yellow-500 mr-2"></div>
                    <div className="w-3 h-3 rounded-full bg-green-500 mr-2"></div>
                    <div className="flex-1 bg-white dark:bg-gray-700 h-6 rounded-md mx-2"></div>
                  </div>
                </div>

                <div className="p-4 h-[calc(100%-48px)] overflow-auto">
                  <div className="max-w-4xl mx-auto">
                    <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded-md w-3/4 mb-4"></div>
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-md w-full mb-2"></div>
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-md w-full mb-2"></div>
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-md w-2/3 mb-6"></div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                      <div className="h-40 bg-gray-200 dark:bg-gray-700 rounded-md"></div>
                      <div className="h-40 bg-gray-200 dark:bg-gray-700 rounded-md"></div>
                    </div>

                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-md w-full mb-2"></div>
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-md w-full mb-2"></div>
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-md w-4/5 mb-6"></div>

                    <div className="h-60 bg-gray-200 dark:bg-gray-700 rounded-md w-full mb-6"></div>

                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-md w-full mb-2"></div>
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-md w-full mb-2"></div>
                    <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded-md w-3/4 mb-2"></div>
                  </div>
                </div>

                {/* Chatbot widget */}
                <div
                  className="absolute bottom-6 right-6 w-16 h-16 rounded-full flex items-center justify-center shadow-lg cursor-pointer"
                  style={{ backgroundColor: chatbot.primary_color }}
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="24"
                    height="24"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    className="text-white"
                  >
                    <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                  </svg>
                </div>

                {/* Chatbot window */}
                <div className="absolute bottom-24 right-6 w-80 h-96 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700 overflow-hidden">
                  <div
                    className="h-14 flex items-center justify-between px-4"
                    style={{ backgroundColor: chatbot.primary_color }}
                  >
                    <div className="text-white font-medium">{chatbot.name}</div>
                    <div className="flex items-center gap-2">
                      <div className="w-6 h-6 rounded-full bg-white/20 flex items-center justify-center cursor-pointer">
                        <svg
                          xmlns="http://www.w3.org/2000/svg"
                          width="14"
                          height="14"
                          viewBox="0 0 24 24"
                          fill="none"
                          stroke="currentColor"
                          strokeWidth="2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          className="text-white"
                        >
                          <line x1="18" y1="6" x2="6" y2="18"></line>
                          <line x1="6" y1="6" x2="18" y2="18"></line>
                        </svg>
                      </div>
                    </div>
                  </div>

                  <div className="h-[calc(100%-112px)] p-4 overflow-auto bg-gray-50 dark:bg-gray-900">
                    <div className="space-y-4">
                      <div className="flex">
                        <div className="bg-gray-200 dark:bg-gray-700 rounded-lg rounded-tl-none p-3 max-w-[80%]">
                          <p className="text-sm">Hello! How can I help you today?</p>
                        </div>
                      </div>

                      <div className="flex justify-end">
                        <div
                          className="rounded-lg rounded-tr-none p-3 max-w-[80%] text-white"
                          style={{ backgroundColor: chatbot.primary_color }}
                        >
                          <p className="text-sm">I have a question about your services.</p>
                        </div>
                      </div>

                      <div className="flex">
                        <div className="bg-gray-200 dark:bg-gray-700 rounded-lg rounded-tl-none p-3 max-w-[80%]">
                          <p className="text-sm">
                            Of course! I'd be happy to help with any questions about our services. What would you like
                            to know?
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div className="h-14 border-t border-gray-200 dark:border-gray-700 flex items-center px-4 bg-white dark:bg-gray-800">
                    <input
                      type="text"
                      placeholder="Type your message..."
                      className="w-full bg-transparent border-none outline-none text-sm dark:text-white"
                    />
                    <button
                      className="ml-2 w-8 h-8 rounded-full flex items-center justify-center"
                      style={{ backgroundColor: chatbot.primary_color }}
                    >
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        viewBox="0 0 24 24"
                        fill="none"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        className="text-white"
                      >
                        <line x1="22" y1="2" x2="11" y2="13"></line>
                        <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                      </svg>
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

            </div>
      </div>
    </SidebarInset>
  )
}


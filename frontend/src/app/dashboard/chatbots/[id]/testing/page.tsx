"use client";

import { useState } from "react";
import { Bot, Code, Copy, MessageSquare, RefreshCw, Send } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Progress } from "@/components/ui/progress";
import { Separator } from "@/components/ui/separator";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { DarkModeToggle } from "@/components/darkmodetoogle";
// import { toast } from "@/components/ui/use-toast"

export default function TestingPage() {
  const [message, setMessage] = useState("");
  const [conversation, setConversation] = useState<
    {
      role: "user" | "bot";
      content: string;
      intent?: string;
      confidence?: number;
      entities?: { name: string; value: string }[];
      webhook?: { name: string; status: string; response?: string };
    }[]
  >([
    {
      role: "bot",
      content: "Hello! I'm your testing assistant. How can I help you today?",
    },
  ]);

  const handleSendMessage = () => {
    if (!message.trim()) return;

    // Add user message
    setConversation([...conversation, { role: "user", content: message }]);

    // Simulate bot response
    setTimeout(() => {
      let botResponse: (typeof conversation)[0] = {
        role: "bot",
        content: "I'm not sure how to respond to that.",
      };

      // Simple pattern matching for demo purposes
      if (
        message.toLowerCase().includes("order") &&
        message.toLowerCase().includes("status")
      ) {
        botResponse = {
          role: "bot",
          content:
            "Your order AB1234 is currently being processed and will be shipped within 2 business days.",
          intent: "Order Status",
          confidence: 0.92,
          entities: [{ name: "OrderID", value: "AB1234" }],
          webhook: {
            name: "Order API",
            status: "Success",
            response:
              '{"status": "processing", "estimated_shipping": "2 business days"}',
          },
        };
      } else if (
        message.toLowerCase().includes("hello") ||
        message.toLowerCase().includes("hi")
      ) {
        botResponse = {
          role: "bot",
          content: "Hello there! How can I assist you today?",
          intent: "Greeting",
          confidence: 0.95,
        };
      } else if (
        message.toLowerCase().includes("product") ||
        message.toLowerCase().includes("laptop")
      ) {
        botResponse = {
          role: "bot",
          content:
            "Our latest laptop model is the XPS 15 with 16GB RAM and 512GB SSD. Would you like more information?",
          intent: "Product Inquiry",
          confidence: 0.88,
          entities: [{ name: "Product", value: "Laptop" }],
          webhook: {
            name: "Product Catalog",
            status: "Success",
            response:
              '{"product": "XPS 15", "specs": {"ram": "16GB", "storage": "512GB SSD"}}',
          },
        };
      }

      setConversation((prev) => [...prev, botResponse]);

      // Show toast for intent recognition
      if (botResponse.intent) {
        // toast({
        //   title: "Intent Recognized",
        //   description: `Detected "${botResponse.intent}" with ${(botResponse.confidence! * 100).toFixed(1)}% confidence.`,
        // })
      }
    }, 1000);

    setMessage("");
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // toast({
    //   title: "Copied to clipboard",
    //   description: "The content has been copied to your clipboard.",
    // })
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
            <div>
              <h1 className="text-3xl font-bold tracking-tight">Testing</h1>
              <p className="text-muted-foreground">
                Test your conversational AI in real-time.
              </p>
            </div>

            <div className="grid gap-6 md:grid-cols-3">
              <Card className="md:col-span-2">
                <CardHeader>
                  <CardTitle>Conversation</CardTitle>
                  <CardDescription>
                    Test your bot by sending messages and see how it responds.
                  </CardDescription>
                </CardHeader>
                <CardContent className="p-0">
                  <div className="h-[500px] overflow-y-auto p-4">
                    {conversation.map((msg, index) => (
                      <div
                        key={index}
                        className={`mb-4 flex ${
                          msg.role === "user" ? "justify-end" : "justify-start"
                        }`}
                      >
                        <div
                          className={`max-w-[80%] rounded-lg p-3 ${
                            msg.role === "user"
                              ? "bg-primary text-primary-foreground"
                              : "bg-muted"
                          }`}
                        >
                          <div className="flex items-center gap-2">
                            {msg.role === "bot" && <Bot className="h-4 w-4" />}
                            {msg.role === "user" && (
                              <MessageSquare className="h-4 w-4" />
                            )}
                            <span>{msg.content}</span>
                          </div>

                          {msg.intent && (
                            <div className="mt-2 space-y-1 border-t pt-2 text-xs">
                              <div className="flex items-center justify-between">
                                <span>Intent: {msg.intent}</span>
                                <span>
                                  Confidence:{" "}
                                  {(msg.confidence! * 100).toFixed(1)}%
                                </span>
                              </div>
                              <Progress
                                value={msg.confidence! * 100}
                                className="h-1"
                              />
                            </div>
                          )}

                          {msg.entities && msg.entities.length > 0 && (
                            <div className="mt-2 border-t pt-2 text-xs">
                              <div className="mb-1">Entities:</div>
                              <div className="flex flex-wrap gap-1">
                                {msg.entities.map((entity, i) => (
                                  <div
                                    key={i}
                                    className="rounded-full bg-primary/10 px-2 py-0.5"
                                  >
                                    {entity.name}:{" "}
                                    <span className="font-medium">
                                      {entity.value}
                                    </span>
                                  </div>
                                ))}
                              </div>
                            </div>
                          )}

                          {msg.webhook && (
                            <div className="mt-2 border-t pt-2 text-xs">
                              <div className="mb-1">
                                Webhook: {msg.webhook.name}
                              </div>
                              <div
                                className={`rounded-full px-2 py-0.5 ${
                                  msg.webhook.status === "Success"
                                    ? "bg-green-50 text-green-700 dark:bg-green-900/20 dark:text-green-400"
                                    : "bg-red-50 text-red-700 dark:bg-red-900/20 dark:text-red-400"
                                }`}
                              >
                                Status: {msg.webhook.status}
                              </div>
                              {msg.webhook.response && (
                                <div className="mt-1 flex items-center justify-between rounded bg-black/10 p-1 font-mono dark:bg-white/10">
                                  <div className="truncate">
                                    {msg.webhook.response}
                                  </div>
                                  <Button
                                    variant="ghost"
                                    size="sm"
                                    className="h-5 w-5 p-0"
                                    onClick={() =>
                                      copyToClipboard(msg.webhook!.response!)
                                    }
                                  >
                                    <Copy className="h-3 w-3" />
                                    <span className="sr-only">Copy</span>
                                  </Button>
                                </div>
                              )}
                            </div>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                </CardContent>
                <CardFooter className="border-t p-3">
                  <div className="flex w-full items-center gap-2">
                    <Input
                      placeholder="Type a message..."
                      value={message}
                      onChange={(e) => setMessage(e.target.value)}
                      onKeyDown={(e) =>
                        e.key === "Enter" && handleSendMessage()
                      }
                    />
                    <Button onClick={handleSendMessage}>
                      <Send className="h-4 w-4" />
                      <span className="sr-only">Send</span>
                    </Button>
                  </div>
                </CardFooter>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle>Testing Tools</CardTitle>
                  <CardDescription>
                    Tools to help you test your bot.
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <Tabs defaultValue="suggestions">
                    <TabsList className="grid w-full grid-cols-2">
                      <TabsTrigger value="suggestions">Suggestions</TabsTrigger>
                      <TabsTrigger value="debug">Debug</TabsTrigger>
                    </TabsList>

                    <TabsContent value="suggestions" className="space-y-4 pt-4">
                      <div className="space-y-2">
                        <h3 className="text-sm font-medium">
                          Try these phrases
                        </h3>
                        <div className="space-y-2">
                          <Button
                            variant="outline"
                            size="sm"
                            className="w-full justify-start"
                            onClick={() => {
                              setMessage(
                                "What's the status of my order AB1234?"
                              );
                              setTimeout(() => handleSendMessage(), 100);
                            }}
                          >
                            What's the status of my order AB1234?
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            className="w-full justify-start"
                            onClick={() => {
                              setMessage("Tell me about your latest laptop");
                              setTimeout(() => handleSendMessage(), 100);
                            }}
                          >
                            Tell me about your latest laptop
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            className="w-full justify-start"
                            onClick={() => {
                              setMessage("Hello, how are you today?");
                              setTimeout(() => handleSendMessage(), 100);
                            }}
                          >
                            Hello, how are you today?
                          </Button>
                        </div>
                      </div>

                      <Separator />

                      <div className="space-y-2">
                        <h3 className="text-sm font-medium">Test Scenarios</h3>
                        <div className="space-y-2">
                          <Button
                            variant="outline"
                            size="sm"
                            className="w-full justify-start"
                          >
                            Run Order Flow Test
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            className="w-full justify-start"
                          >
                            Run Product Inquiry Test
                          </Button>
                          <Button
                            variant="outline"
                            size="sm"
                            className="w-full justify-start"
                          >
                            Run Support Request Test
                          </Button>
                        </div>
                      </div>
                    </TabsContent>

                    <TabsContent value="debug" className="space-y-4 pt-4">
                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <h3 className="text-sm font-medium">Debug Mode</h3>
                          <Button variant="outline" size="sm">
                            <RefreshCw className="mr-2 h-3 w-3" />
                            Refresh
                          </Button>
                        </div>
                        <div className="rounded-md border p-3">
                          <div className="space-y-1 text-xs">
                            <div className="flex items-center justify-between">
                              <span>Intent Recognition</span>
                              <span className="font-medium text-green-600 dark:text-green-400">
                                Working
                              </span>
                            </div>
                            <div className="flex items-center justify-between">
                              <span>Entity Extraction</span>
                              <span className="font-medium text-green-600 dark:text-green-400">
                                Working
                              </span>
                            </div>
                            <div className="flex items-center justify-between">
                              <span>Webhook Integration</span>
                              <span className="font-medium text-green-600 dark:text-green-400">
                                Working
                              </span>
                            </div>
                            <div className="flex items-center justify-between">
                              <span>Response Generation</span>
                              <span className="font-medium text-green-600 dark:text-green-400">
                                Working
                              </span>
                            </div>
                          </div>
                        </div>
                      </div>

                      <Separator />

                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <h3 className="text-sm font-medium">API Request</h3>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-6 w-6 p-0"
                            onClick={() =>
                              copyToClipboard(`curl -X POST https://api.example.com/conversation \\
  -H "Content-Type: application/json" \\
  -d '{"message": "What's the status of my order?", "session": "user-123"}'`)
                            }
                          >
                            <Copy className="h-3 w-3" />
                            <span className="sr-only">Copy</span>
                          </Button>
                        </div>
                        <div className="rounded-md bg-muted p-2 font-mono text-xs">
                          <pre className="whitespace-pre-wrap">
                            {`curl -X POST https://api.example.com/conversation \\
  -H "Content-Type: application/json" \\
  -d '{"message": "What's the status of my order?", "session": "user-123"}'`}
                          </pre>
                        </div>
                      </div>

                      <div className="space-y-2">
                        <div className="flex items-center justify-between">
                          <h3 className="text-sm font-medium">API Response</h3>
                          <Button
                            variant="ghost"
                            size="sm"
                            className="h-6 w-6 p-0"
                            onClick={() =>
                              copyToClipboard(`{
  "response": "Your order AB1234 is currently being processed and will be shipped within 2 business days.",
  "intent": "Order Status",
  "confidence": 0.92,
  "entities": [
    { "name": "OrderID", "value": "AB1234" }
  ],
  "webhook": {
    "name": "Order API",
    "status": "Success"
  }
}`)
                            }
                          >
                            <Copy className="h-3 w-3" />
                            <span className="sr-only">Copy</span>
                          </Button>
                        </div>
                        <div className="rounded-md bg-muted p-2 font-mono text-xs">
                          <pre className="whitespace-pre-wrap">
                            {`{
  "response": "Your order AB1234 is currently being processed and will be shipped within 2 business days.",
  "intent": "Order Status",
  "confidence": 0.92,
  "entities": [
    { "name": "OrderID", "value": "AB1234" }
  ],
  "webhook": {
    "name": "Order API",
    "status": "Success"
  }
}`}
                          </pre>
                        </div>
                      </div>
                    </TabsContent>
                  </Tabs>
                </CardContent>
                <CardFooter>
                  <Button variant="outline" className="w-full">
                    <Code className="mr-2 h-4 w-4" />
                    View API Documentation
                  </Button>
                </CardFooter>
              </Card>
            </div>
          </div>
        </div>
      </div>
    </SidebarInset>
  );
}

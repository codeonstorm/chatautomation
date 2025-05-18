"use client"

import { useState } from "react"
import { Bot, MessageSquare, RefreshCw, Send } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Progress } from "@/components/ui/progress"
import { Separator } from "@/components/ui/separator"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
// import { toast } from "@/components/ui/use-toast"

export default function IntentTrainingPage() {
  const [message, setMessage] = useState("")
  const [conversation, setConversation] = useState<
    {
      role: "user" | "bot"
      content: string
      intent?: string
      confidence?: number
    }[]
  >([
    {
      role: "bot",
      content: "Hello! I'm your training assistant. Try sending some messages to test intent recognition.",
    },
  ])

  const [trainingProgress, setTrainingProgress] = useState(78)

  const handleSendMessage = () => {
    if (!message.trim()) return

    // Add user message
    setConversation([...conversation, { role: "user", content: message }])

    // Simulate intent recognition
    setTimeout(() => {
      const intents = [
        { name: "Greeting", confidence: 0.92 },
        { name: "Order Status", confidence: 0.85 },
        { name: "Product Inquiry", confidence: 0.78 },
        { name: "Support Request", confidence: 0.65 },
      ]

      // Randomly select an intent based on the message
      const randomIndex = Math.floor(Math.random() * intents.length)
      const recognizedIntent = intents[randomIndex]

      // Add bot response
      setConversation((prev) => [
        ...prev,
        {
          role: "bot",
          content: `I recognized that as a "${recognizedIntent.name}" intent.`,
          intent: recognizedIntent.name,
          confidence: recognizedIntent.confidence,
        },
      ])

      // Show toast for intent recognition
      // toast({
      //   title: "Intent Recognized",
      //   description: `Detected "${recognizedIntent.name}" with ${(recognizedIntent.confidence * 100).toFixed(1)}% confidence.`,
      // })
    }, 1000)

    setMessage("")
  }

  const startTraining = () => {
    // toast({
    //   title: "Training Started",
    //   description: "Your model is now training with the latest data.",
    // })

    // Simulate training progress
    setTrainingProgress(0)
    const interval = setInterval(() => {
      setTrainingProgress((prev) => {
        if (prev >= 100) {
          clearInterval(interval)
          // toast({
          //   title: "Training Complete",
          //   description: "Your model has been successfully trained.",
          // })
          return 100
        }
        return prev + 10
      })
    }, 800)
  }

  return (
    <div className="space-y-6 py-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Intent Training</h1>
        <p className="text-muted-foreground">Train and test your intent recognition model.</p>
      </div>

      <Tabs defaultValue="test">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="test">Test Recognition</TabsTrigger>
          <TabsTrigger value="train">Train Model</TabsTrigger>
        </TabsList>

        <TabsContent value="test" className="space-y-4 pt-4">
          <div className="grid gap-6 md:grid-cols-2">
            <Card className="md:col-span-1">
              <CardHeader>
                <CardTitle>Test Your Bot</CardTitle>
                <CardDescription>Send messages to test intent recognition.</CardDescription>
              </CardHeader>
              <CardContent className="p-0">
                <div className="h-[400px] overflow-y-auto p-4">
                  {conversation.map((msg, index) => (
                    <div key={index} className={`mb-4 flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}>
                      <div
                        className={`max-w-[80%] rounded-lg p-3 ${
                          msg.role === "user" ? "bg-primary text-primary-foreground" : "bg-muted"
                        }`}
                      >
                        <div className="flex items-center gap-2">
                          {msg.role === "bot" && <Bot className="h-4 w-4" />}
                          {msg.role === "user" && <MessageSquare className="h-4 w-4" />}
                          <span>{msg.content}</span>
                        </div>
                        {msg.intent && (
                          <div className="mt-2 text-xs">
                            <div className="flex items-center justify-between">
                              <span>Intent: {msg.intent}</span>
                              <span>Confidence: {(msg.confidence! * 100).toFixed(1)}%</span>
                            </div>
                            <Progress value={msg.confidence! * 100} className="mt-1 h-1" />
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
                    onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
                  />
                  <Button onClick={handleSendMessage}>
                    <Send className="h-4 w-4" />
                    <span className="sr-only">Send</span>
                  </Button>
                </div>
              </CardFooter>
            </Card>

            <Card className="md:col-span-1">
              <CardHeader>
                <CardTitle>Intent Recognition</CardTitle>
                <CardDescription>View detailed intent recognition results.</CardDescription>
              </CardHeader>
              <CardContent>
                <div className="space-y-4">
                  <div>
                    <h3 className="mb-2 text-sm font-medium">Top Intents</h3>
                    <div className="space-y-2">
                      <div className="space-y-1">
                        <div className="flex items-center justify-between">
                          <span className="text-sm">Greeting</span>
                          <span className="text-sm">92%</span>
                        </div>
                        <Progress value={92} className="h-2" />
                      </div>
                      <div className="space-y-1">
                        <div className="flex items-center justify-between">
                          <span className="text-sm">Order Status</span>
                          <span className="text-sm">85%</span>
                        </div>
                        <Progress value={85} className="h-2" />
                      </div>
                      <div className="space-y-1">
                        <div className="flex items-center justify-between">
                          <span className="text-sm">Product Inquiry</span>
                          <span className="text-sm">78%</span>
                        </div>
                        <Progress value={78} className="h-2" />
                      </div>
                    </div>
                  </div>

                  <Separator />

                  <div>
                    <h3 className="mb-2 text-sm font-medium">Detected Entities</h3>
                    <div className="rounded-md border p-3">
                      <div className="text-sm">No entities detected in the last message.</div>
                    </div>
                  </div>

                  <Separator />

                  <div>
                    <h3 className="mb-2 text-sm font-medium">Suggested Improvements</h3>
                    <div className="space-y-2">
                      <div className="rounded-md bg-muted p-3 text-sm">
                        Add more training phrases for "Product Inquiry" intent.
                      </div>
                      <div className="rounded-md bg-muted p-3 text-sm">
                        Consider creating a "Pricing" intent to handle pricing questions.
                      </div>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </div>
        </TabsContent>

        <TabsContent value="train" className="space-y-4 pt-4">
          <Card>
            <CardHeader>
              <CardTitle>Train Your Model</CardTitle>
              <CardDescription>Train your intent recognition model with the latest data.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="rounded-md border p-4">
                <div className="mb-4 flex items-center justify-between">
                  <div>
                    <h3 className="text-sm font-medium">Model Status</h3>
                    <p className="text-sm text-muted-foreground">Your model was last trained 2 days ago.</p>
                  </div>
                  <div className="rounded-md bg-green-50 px-2 py-1 text-xs font-medium text-green-700 dark:bg-green-900/50 dark:text-green-400">
                    Ready
                  </div>
                </div>

                <div className="space-y-2">
                  <div className="flex items-center justify-between text-sm">
                    <span>Training Data</span>
                    <span className="font-medium">156 samples</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span>Intents</span>
                    <span className="font-medium">12</span>
                  </div>
                  <div className="flex items-center justify-between text-sm">
                    <span>Entities</span>
                    <span className="font-medium">8</span>
                  </div>
                </div>
              </div>

              <div className="rounded-md border p-4">
                <h3 className="mb-2 text-sm font-medium">Training Progress</h3>
                <div className="space-y-2">
                  <Progress value={trainingProgress} className="h-2" />
                  <div className="flex items-center justify-between text-xs text-muted-foreground">
                    <span>{trainingProgress === 100 ? "Complete" : "Training..."}</span>
                    <span>{trainingProgress}%</span>
                  </div>
                </div>
              </div>
            </CardContent>
            <CardFooter className="flex justify-between">
              <Button variant="outline">View Training History</Button>
              <Button onClick={startTraining} disabled={trainingProgress > 0 && trainingProgress < 100}>
                <RefreshCw className="mr-2 h-4 w-4" />
                {trainingProgress === 100 ? "Retrain Model" : trainingProgress > 0 ? "Training..." : "Start Training"}
              </Button>
            </CardFooter>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Training Analytics</CardTitle>
              <CardDescription>View analytics about your training data and model performance.</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="grid gap-4 md:grid-cols-2">
                <div className="rounded-md border p-4">
                  <h3 className="mb-2 text-sm font-medium">Intent Distribution</h3>
                  <div className="space-y-2">
                    <div className="space-y-1">
                      <div className="flex items-center justify-between text-sm">
                        <span>Greeting</span>
                        <span>15 samples</span>
                      </div>
                      <div className="h-2 rounded-full bg-muted">
                        <div className="h-full w-[25%] rounded-full bg-primary"></div>
                      </div>
                    </div>
                    <div className="space-y-1">
                      <div className="flex items-center justify-between text-sm">
                        <span>Order Status</span>
                        <span>24 samples</span>
                      </div>
                      <div className="h-2 rounded-full bg-muted">
                        <div className="h-full w-[40%] rounded-full bg-primary"></div>
                      </div>
                    </div>
                    <div className="space-y-1">
                      <div className="flex items-center justify-between text-sm">
                        <span>Product Inquiry</span>
                        <span>32 samples</span>
                      </div>
                      <div className="h-2 rounded-full bg-muted">
                        <div className="h-full w-[55%] rounded-full bg-primary"></div>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="rounded-md border p-4">
                  <h3 className="mb-2 text-sm font-medium">Model Performance</h3>
                  <div className="space-y-2">
                    <div className="flex items-center justify-between text-sm">
                      <span>Accuracy</span>
                      <span className="font-medium">92%</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span>Precision</span>
                      <span className="font-medium">89%</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span>Recall</span>
                      <span className="font-medium">87%</span>
                    </div>
                    <div className="flex items-center justify-between text-sm">
                      <span>F1 Score</span>
                      <span className="font-medium">88%</span>
                    </div>
                  </div>
                </div>
              </div>
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  )
}

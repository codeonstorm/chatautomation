"use client"

import type React from "react"

import { useState } from "react"
import { Bot, Plus, Save, Trash2 } from "lucide-react"
import { useRouter } from "next/navigation"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
// import { toast } from "@/components/ui/use-toast"

export default function CreateIntentPage() {
  const router = useRouter()
  const [trainingPhrases, setTrainingPhrases] = useState<string[]>(["Hello there", "Hi, how are you?", "Good morning"])
  const [newPhrase, setNewPhrase] = useState("")
  const [responses, setResponses] = useState<string[]>([
    "Hello! How can I help you today?",
    "Hi there! What can I do for you?",
  ])
  const [newResponse, setNewResponse] = useState("")

  const addTrainingPhrase = () => {
    if (newPhrase.trim()) {
      setTrainingPhrases([...trainingPhrases, newPhrase.trim()])
      setNewPhrase("")
      // toast({
      //   title: "Training phrase added",
      //   description: "Your training phrase has been added successfully.",
      // })
    }
  }

  const removeTrainingPhrase = (index: number) => {
    setTrainingPhrases(trainingPhrases.filter((_, i) => i !== index))
  }

  const addResponse = () => {
    if (newResponse.trim()) {
      setResponses([...responses, newResponse.trim()])
      setNewResponse("")
      // toast({
      //   title: "Response added",
      //   description: "Your response has been added successfully.",
      // })
    }
  }

  const removeResponse = (index: number) => {
    setResponses(responses.filter((_, i) => i !== index))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // toast({
    //   title: "Intent created",
    //   description: "Your intent has been created successfully.",
    // })
    router.push("/dashboard/intents")
  }

  return (
    <div className="space-y-6 py-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Create Intent</h1>
        <p className="text-muted-foreground">Create a new intent for your conversational AI.</p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="grid gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Intent Details</CardTitle>
              <CardDescription>Basic information about your intent.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-2">
                <Label htmlFor="name">Intent Name</Label>
                <Input id="name" placeholder="e.g., Greeting, Order Status" required />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  placeholder="Describe what this intent is for..."
                  className="min-h-[100px]"
                />
              </div>
            </CardContent>
          </Card>

          <Tabs defaultValue="training">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="training">Training Phrases</TabsTrigger>
              <TabsTrigger value="responses">Responses</TabsTrigger>
              <TabsTrigger value="parameters">Parameters</TabsTrigger>
            </TabsList>

            <TabsContent value="training" className="space-y-4 pt-4">
              <Card>
                <CardHeader>
                  <CardTitle>Training Phrases</CardTitle>
                  <CardDescription>Add phrases that users might say to trigger this intent.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex gap-2">
                    <Input
                      placeholder="Add a training phrase..."
                      value={newPhrase}
                      onChange={(e) => setNewPhrase(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && addTrainingPhrase()}
                    />
                    <Button type="button" onClick={addTrainingPhrase}>
                      <Plus className="h-4 w-4" />
                      <span className="sr-only">Add</span>
                    </Button>
                  </div>

                  <div className="space-y-2">
                    {trainingPhrases.map((phrase, index) => (
                      <div key={index} className="flex items-center justify-between rounded-md border p-3">
                        <div className="flex items-center gap-2">
                          <span>{phrase}</span>
                        </div>
                        <Button variant="ghost" size="sm" onClick={() => removeTrainingPhrase(index)}>
                          <Trash2 className="h-4 w-4" />
                          <span className="sr-only">Remove</span>
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
                <CardFooter>
                  <div className="text-sm text-muted-foreground">
                    Add at least 5-10 training phrases for better intent recognition.
                  </div>
                </CardFooter>
              </Card>
            </TabsContent>

            <TabsContent value="responses" className="space-y-4 pt-4">
              <Card>
                <CardHeader>
                  <CardTitle>Responses</CardTitle>
                  <CardDescription>Add responses that your bot will use when this intent is triggered.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="flex gap-2">
                    <Input
                      placeholder="Add a response..."
                      value={newResponse}
                      onChange={(e) => setNewResponse(e.target.value)}
                      onKeyDown={(e) => e.key === "Enter" && addResponse()}
                    />
                    <Button type="button" onClick={addResponse}>
                      <Plus className="h-4 w-4" />
                      <span className="sr-only">Add</span>
                    </Button>
                  </div>

                  <div className="space-y-2">
                    {responses.map((response, index) => (
                      <div key={index} className="flex items-center justify-between rounded-md border p-3">
                        <div className="flex items-center gap-2">
                          <Bot className="h-4 w-4 text-muted-foreground" />
                          <span>{response}</span>
                        </div>
                        <Button variant="ghost" size="sm" onClick={() => removeResponse(index)}>
                          <Trash2 className="h-4 w-4" />
                          <span className="sr-only">Remove</span>
                        </Button>
                      </div>
                    ))}
                  </div>
                </CardContent>
                <CardFooter>
                  <div className="text-sm text-muted-foreground">
                    Add multiple responses for variety in your bot's replies.
                  </div>
                </CardFooter>
              </Card>
            </TabsContent>

            <TabsContent value="parameters" className="space-y-4 pt-4">
              <Card>
                <CardHeader>
                  <CardTitle>Parameters</CardTitle>
                  <CardDescription>Define parameters that can be extracted from user input.</CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex h-40 items-center justify-center rounded-md border border-dashed">
                    <div className="flex flex-col items-center gap-1 text-center">
                      <Plus className="h-4 w-4 text-muted-foreground" />
                      <p className="text-sm font-medium">Add Parameter</p>
                      <p className="text-xs text-muted-foreground">
                        Parameters help extract specific data from user input
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          <div className="flex justify-end gap-2">
            <Button variant="outline" type="button" onClick={() => router.push("/dashboard/intents")}>
              Cancel
            </Button>
            <Button type="submit">
              <Save className="mr-2 h-4 w-4" />
              Save Intent
            </Button>
          </div>
        </div>
      </form>
    </div>
  )
}

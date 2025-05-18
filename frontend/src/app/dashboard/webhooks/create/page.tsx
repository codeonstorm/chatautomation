"use client"

import React from "react"

import { useState } from "react"
import { Check, ChevronDown, MessageSquare, Plus, Save, Trash2 } from "lucide-react"
import { useRouter } from "next/navigation"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Command, CommandEmpty, CommandGroup, CommandInput, CommandItem, CommandList } from "@/components/ui/command"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Textarea } from "@/components/ui/textarea"
import { useAppDispatch } from "@/redux/store/hooks"
import { Webhook } from "@/redux/store/features/webhook/webhook"
import { useSelector } from "react-redux"
import { RootState } from "@/redux/store/store"
// import { toast } from "@/components/ui/use-toast"

// Sample intents for mapping
const intents = [
  { value: "greeting", label: "Greeting" },
  { value: "order_status", label: "Order Status" },
  { value: "product_inquiry", label: "Product Inquiry" },
  { value: "support_request", label: "Support Request" },
  { value: "feedback", label: "Feedback" },
]

export default function CreateWebhookPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = React.use(params)
  const router = useRouter()
  const [selectedIntents, setSelectedIntents] = useState<string[]>([])
  const [open, setOpen] = useState(false)
  const [headers, setHeaders] = useState<{ key: string; value: string }[]>([
    { key: "Content-Type", value: "application/json" },
    { key: "Authorization", value: "Bearer YOUR_API_KEY" },
  ])
  const [newHeader, setNewHeader] = useState({ key: "", value: "" })
  const dispatch = useAppDispatch()
  const webhook: Webhook  = useSelector((state: RootState) => state.webhook[id] || [])

  const addHeader = () => {
    if (newHeader.key.trim() && newHeader.value.trim()) {
      setHeaders([...headers, { ...newHeader }])
      setNewHeader({ key: "", value: "" })
      // toast({
      //   title: "Header added",
      //   description: "Your header has been added successfully.",
      // })
    }
  }

  const removeHeader = (index: number) => {
    setHeaders(headers.filter((_, i) => i !== index))
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    // toast({
    //   title: "Webhook created",
    //   description: "Your webhook has been created successfully.",
    // })
    router.push("/dashboard/webhooks")
  }

  return (
    <div className="space-y-6 py-6">
      <div>
        <h1 className="text-3xl font-bold tracking-tight">Create Webhook</h1>
        <p className="text-muted-foreground">Create a new webhook for your conversational AI.</p>
      </div>

      <form onSubmit={handleSubmit}>
        <div className="grid gap-6">
          <Card>
            <CardHeader>
              <CardTitle>Webhook Details</CardTitle>
              <CardDescription>Basic information about your webhook.</CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="grid gap-2">
                <Label htmlFor="name">Webhook Name</Label>
                <Input id="name" placeholder="e.g., Order API, Product Catalog" required />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="url">Webhook URL</Label>
                <Input id="url" placeholder="https://api.example.com/webhook" required />
              </div>
              <div className="grid gap-2">
                <Label htmlFor="description">Description</Label>
                <Textarea
                  id="description"
                  placeholder="Describe what this webhook is for..."
                  className="min-h-[100px]"
                />
              </div>
              <div className="flex items-center space-x-2">
                <Switch id="active" defaultChecked />
                <Label htmlFor="active">Active</Label>
              </div>
            </CardContent>
          </Card>

          <Tabs defaultValue="intents">
            <TabsList className="grid w-full grid-cols-3">
              <TabsTrigger value="intents">Intent Mapping</TabsTrigger>
              <TabsTrigger value="headers">Headers</TabsTrigger>
              <TabsTrigger value="testing">Testing</TabsTrigger>
            </TabsList>

            <TabsContent value="intents" className="space-y-4 pt-4">
              <Card>
                <CardHeader>
                  <CardTitle>Intent Mapping</CardTitle>
                  <CardDescription>Map intents to this webhook.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-2">
                    <Label>Select Intents</Label>
                    <Popover open={open} onOpenChange={setOpen}>
                      <PopoverTrigger asChild>
                        <Button variant="outline" role="combobox" aria-expanded={open} className="justify-between">
                          {selectedIntents.length > 0
                            ? `${selectedIntents.length} intent${selectedIntents.length > 1 ? "s" : ""} selected`
                            : "Select intents..."}
                          <ChevronDown className="ml-2 h-4 w-4 shrink-0 opacity-50" />
                        </Button>
                      </PopoverTrigger>
                      <PopoverContent className="w-[300px] p-0">
                        <Command>
                          <CommandInput placeholder="Search intents..." />
                          <CommandList>
                            <CommandEmpty>No intent found.</CommandEmpty>
                            <CommandGroup>
                              {intents.map((intent) => (
                                <CommandItem
                                  key={intent.value}
                                  value={intent.value}
                                  onSelect={() => {
                                    setSelectedIntents(
                                      selectedIntents.includes(intent.value)
                                        ? selectedIntents.filter((i) => i !== intent.value)
                                        : [...selectedIntents, intent.value],
                                    )
                                  }}
                                >
                                  <Check
                                    className={`mr-2 h-4 w-4 ${
                                      selectedIntents.includes(intent.value) ? "opacity-100" : "opacity-0"
                                    }`}
                                  />
                                  <div className="flex items-center gap-2">
                                    <MessageSquare className="h-4 w-4 text-muted-foreground" />
                                    {intent.label}
                                  </div>
                                </CommandItem>
                              ))}
                            </CommandGroup>
                          </CommandList>
                        </Command>
                      </PopoverContent>
                    </Popover>
                  </div>

                  <div className="space-y-2">
                    <Label>Selected Intents</Label>
                    <div className="rounded-md border p-4">
                      {selectedIntents.length > 0 ? (
                        <div className="flex flex-wrap gap-2">
                          {selectedIntents.map((intentValue) => {
                            const intent = intents.find((i) => i.value === intentValue)
                            return (
                              <div
                                key={intentValue}
                                className="flex items-center gap-1 rounded-full border px-3 py-1 text-sm"
                              >
                                <MessageSquare className="h-3 w-3 text-muted-foreground" />
                                <span>{intent?.label}</span>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  className="h-5 w-5 p-0"
                                  onClick={() => {
                                    setSelectedIntents(selectedIntents.filter((i) => i !== intentValue))
                                  }}
                                >
                                  <Trash2 className="h-3 w-3" />
                                  <span className="sr-only">Remove</span>
                                </Button>
                              </div>
                            )
                          })}
                        </div>
                      ) : (
                        <div className="text-center text-sm text-muted-foreground">No intents selected</div>
                      )}
                    </div>
                  </div>
                </CardContent>
                <CardFooter>
                  <div className="text-sm text-muted-foreground">
                    This webhook will be triggered when any of the selected intents are matched.
                  </div>
                </CardFooter>
              </Card>
            </TabsContent>

            <TabsContent value="headers" className="space-y-4 pt-4">
              <Card>
                <CardHeader>
                  <CardTitle>HTTP Headers</CardTitle>
                  <CardDescription>Configure HTTP headers for your webhook requests.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-4">
                    <div className="grid grid-cols-5 gap-2">
                      <div className="col-span-2">
                        <Label htmlFor="header-key">Header Name</Label>
                        <Input
                          id="header-key"
                          placeholder="e.g., Content-Type"
                          value={newHeader.key}
                          onChange={(e) => setNewHeader({ ...newHeader, key: e.target.value })}
                        />
                      </div>
                      <div className="col-span-2">
                        <Label htmlFor="header-value">Header Value</Label>
                        <Input
                          id="header-value"
                          placeholder="e.g., application/json"
                          value={newHeader.value}
                          onChange={(e) => setNewHeader({ ...newHeader, value: e.target.value })}
                        />
                      </div>
                      <div className="flex items-end">
                        <Button
                          type="button"
                          onClick={addHeader}
                          disabled={!newHeader.key.trim() || !newHeader.value.trim()}
                          className="w-full"
                        >
                          <Plus className="h-4 w-4" />
                          <span className="sr-only">Add</span>
                        </Button>
                      </div>
                    </div>

                    <div className="space-y-2">
                      {headers.map((header, index) => (
                        <div key={index} className="flex items-center justify-between rounded-md border p-3">
                          <div className="grid grid-cols-2 gap-4 text-sm">
                            <div className="font-medium">{header.key}</div>
                            <div className="font-mono">{header.value}</div>
                          </div>
                          <Button variant="ghost" size="sm" onClick={() => removeHeader(index)}>
                            <Trash2 className="h-4 w-4" />
                            <span className="sr-only">Remove</span>
                          </Button>
                        </div>
                      ))}
                    </div>
                  </div>
                </CardContent>
              </Card>
            </TabsContent>

            <TabsContent value="testing" className="space-y-4 pt-4">
              <Card>
                <CardHeader>
                  <CardTitle>Webhook Testing</CardTitle>
                  <CardDescription>Test your webhook configuration.</CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  <div className="grid gap-2">
                    <Label htmlFor="method">HTTP Method</Label>
                    <Select defaultValue="post">
                      <SelectTrigger id="method">
                        <SelectValue placeholder="Select method" />
                      </SelectTrigger>
                      <SelectContent>
                        <SelectItem value="get">GET</SelectItem>
                        <SelectItem value="post">POST</SelectItem>
                        <SelectItem value="put">PUT</SelectItem>
                        <SelectItem value="patch">PATCH</SelectItem>
                        <SelectItem value="delete">DELETE</SelectItem>
                      </SelectContent>
                    </Select>
                  </div>

                  <div className="grid gap-2">
                    <Label htmlFor="test-payload">Test Payload</Label>
                    <Textarea
                      id="test-payload"
                      className="min-h-[200px] font-mono text-sm"
                      defaultValue={`{
  "intent": "order_status",
  "parameters": {
    "order_id": "AB1234"
  },
  "session": "user-123"
}`}
                    />
                  </div>

                  <Button type="button" variant="outline" className="w-full">
                    Test Webhook
                  </Button>
                </CardContent>
              </Card>
            </TabsContent>
          </Tabs>

          <div className="flex justify-end gap-2">
            <Button variant="outline" type="button" onClick={() => router.push("/dashboard/webhooks")}>
              Cancel
            </Button>
            <Button type="submit">
              <Save className="mr-2 h-4 w-4" />
              Save Webhook
            </Button>
          </div>
        </div>
      </form>
    </div>
  )
}

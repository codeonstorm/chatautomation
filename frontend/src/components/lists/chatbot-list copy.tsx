"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { PlusCircle, Pencil, Trash2, BookOpen, Eye } from "lucide-react"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog"
import { Form, FormControl, FormDescription, FormField, FormItem, FormLabel, FormMessage } from "@/components/ui/form"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Input } from "@/components/ui/input"
import { Textarea } from "@/components/ui/textarea"
import { Switch } from "@/components/ui/switch"
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import * as z from "zod"
// import { useToast } from "@/components/ui/use-toast"
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

import { useRouter } from "next/navigation"
import { useSelector } from 'react-redux';
import { RootState } from "@/redux/store/store";
import Link from "next/link"
import { Chatbot } from "@/types/chatbot";
import { Domain } from "@/types/domain";
import { createChatbot, updateChatbot } from "@/services/chatbot"
import { useAppDispatch } from "@/redux/store/hooks"
import { addChatbot } from "@/redux/store/features/chatbot/chatbot"

// Form schema for chatbot creation/editing
const chatbotFormSchema = z.object({
  name: z.string().min(1, "Name is required"),
  behavior: z.string().min(1, "Behavior is required"),
  system_prompt: z.string().min(1, "System prompt is required"),
  temperature: z.coerce.number().min(0).max(1),
  primary_color: z.string().regex(/^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/, "Invalid color format"),
  secondary_color: z.string().regex(/^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/, "Invalid color format"),
  domain_id: z.coerce.number().int().positive(),
  // is_active: z.boolean().default(true),
})

type ChatbotFormValues = z.infer<typeof chatbotFormSchema>

// Mock chatbots data
// const initialChatbots = [
//   { id: 1, name: "Support Bot", status: "Active", interactions: 523 },
//   { id: 2, name: "Sales Assistant", status: "Inactive", interactions: 102 },
//   { id: 3, name: "FAQ Bot", status: "Active", interactions: 789 },
// ]

const initialChatbots: Chatbot[] = [
  {
    name: "Support Bot",
    description: "hg jhghgj",
    behavior: "hgcg gfj hgvhg hgchjg hgv",
    system_prompt: "",
    temperature: 0.8,
    primary_color: "#7546",
    secondary_color: "#7656",
    uuid: "vhcgfhj",
    service_id: 1,
    created_at: "",
    last_trained: ""
  }
]

export function ChatbotList() {
  const [isLoading, setIsLoading] = useState(false)
  const [isDialogOpen, setIsDialogOpen] = useState(false)
  const [editingChatbot, setEditingChatbot] = useState<number | null>(null)
  // const { toast } = useToast()
  const router = useRouter()
  const dispatch = useAppDispatch()

  const domains:Domain[] = useSelector((state: RootState) => state.domains);


  const form = useForm<ChatbotFormValues>({
    resolver: zodResolver(chatbotFormSchema),
    defaultValues: {
      name: "",
      behavior: "",
      system_prompt: "",
      temperature: 0.7,
      primary_color: "#4a56e2",
      secondary_color: "#ffffff",
      domain_id: 1,
      // is_active: true,
    },
  })

  const onSubmit = async (values: ChatbotFormValues) => {
    setIsLoading(true)
    try {
      if (editingChatbot) {
        // Update existing chatbot
       try {
        // await createChatbot(chatbot);
        dispatch(updateChatbot(chatbot))
       } catch (error) {
        
       }
      } else {
        // Create new chatbot
        try {
          const chatbot = await createChatbot(chatbot)
          dispatch(addChatbot(chatbot))
        } catch (error) {
          
        }
      }

      // Reset form and close dialog
      form.reset()
      setIsDialogOpen(false)
      setEditingChatbot(null)
    } catch (error) {
      console.error("Error:", error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleEdit = (uuid: string) => {
    // Find the chatbot to edit
    const chatbot = chatbots.find((bot) => bot.uuid === id)
    if (!chatbot) return

    // In a real app, you would fetch the full chatbot details from the API
    // For this example, we'll just set some mock values
    form.reset({
      name: chatbot.name,
      behavior: "Helpful assistant",
      system_prompt: "You are a helpful assistant for our company.",
      temperature: 0.7,
      primary_color: "#4a56e2",
      secondary_color: "#ffffff",
      domain_id: 1,
    })

    setEditingChatbot(id)
    setIsDialogOpen(true)
  }

  const handleDelete = async (id: number) => {
    setIsLoading(true)
    try {
      const response = await fetch(`https://ex.com/api/v1/chatbots/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("accessToken")}`,
        },
      })

      if (!response.ok) {
        throw new Error("Failed to delete chatbot")
      }

      // Remove the chatbot from the local state
      // setChatbots(chatbots.filter((bot) => bot.id !== id))

      // toast({
      //   title: "Chatbot deleted",
      //   description: "The chatbot has been deleted successfully.",
      // })
    } catch (error) {
      console.error("Error:", error)
      // toast({
      //   variant: "destructive",
      //   title: "Error",
      //   description: error instanceof Error ? error.message : "An error occurred",
      // })
    } finally {
      // setIsLoading(false)
    }
  }

  const openNewChatbotDialog = () => {
    form.reset({
      name: "",
      behavior: "",
      system_prompt: "",
      temperature: 0.7,
      primary_color: "#4a56e2",
      secondary_color: "#ffffff",
      domain_id: 1,
    })
    setEditingChatbot(null)
    setIsDialogOpen(true)
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Your Chatbots</h2>
        <Button onClick={openNewChatbotDialog}>
          <PlusCircle className="mr-2 h-4 w-4" /> Add New Chatbot
        </Button>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Created On</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {chatbots.map((bot) => (
            <TableRow key={bot.uuid}>
              <TableCell><Link href={`/dashboard/chatbots/${bot.uuid}`}>{bot.name}</Link></TableCell>
              <TableCell>
                <span
                  className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${                   
                    'Active' === "Active" ? "bg-green-100 text-green-800" : "bg-yellow-100 text-yellow-800"}`}>
                  Active
                </span>
              </TableCell>
              <TableCell>{bot.created_at}</TableCell>
              <TableCell>
                <div className="flex space-x-2">
                  <Button variant="outline" size="sm" onClick={() => handleEdit(bot.id)}>
                    <Pencil className="h-4 w-4 mr-1" /> Edit
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="text-primary hover:text-primary-foreground hover:bg-primary"
                    onClick={() => router.push(`/dashboard/chatbots/train/${bot.id}`)}>
                    <BookOpen className="h-4 w-4 mr-1" /> Train
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="text-blue-500 hover:text-blue-700"
                    onClick={() => router.push(`/dashboard/chatbots/preview/${bot.id}`)}>
                    <Eye className="h-4 w-4 mr-1" /> Preview
                  </Button>
                  <AlertDialog>
                    <AlertDialogTrigger asChild>
                      <Button variant="outline" size="sm" className="text-red-500 hover:text-red-700">
                        <Trash2 className="h-4 w-4 mr-1" /> Delete
                      </Button>
                    </AlertDialogTrigger>
                    <AlertDialogContent>
                      <AlertDialogHeader>
                        <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                        <AlertDialogDescription>
                          This action cannot be undone. This will permanently delete the chatbot and all its data.
                        </AlertDialogDescription>
                      </AlertDialogHeader>
                      <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction onClick={() => handleDelete(bot.id)} className="bg-red-500 hover:bg-red-700">
                          Delete
                        </AlertDialogAction>
                      </AlertDialogFooter>
                    </AlertDialogContent>
                  </AlertDialog>
                </div>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      {/* Chatbot Create/Edit Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[600px] overflow-y-scroll max-h-[80vh]">
          <DialogHeader>
            <DialogTitle>{editingChatbot ? "Edit Chatbot" : "Create New Chatbot"}</DialogTitle>
            <DialogDescription>
              {editingChatbot ? "Update your chatbot settings below." : "Fill in the details to create a new chatbot."}
            </DialogDescription>
          </DialogHeader>
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Name</FormLabel>
                    <FormControl>
                      <Input placeholder="Support Bot" {...field} />
                    </FormControl>
                    <FormDescription>The name of your chatbot.</FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="behavior"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Behavior</FormLabel>
                    <FormControl>
                      <Input placeholder="Helpful, friendly assistant" {...field} />
                    </FormControl>
                    <FormDescription>Describe how your chatbot should behave.</FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="system_prompt"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>System Prompt</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="You are a helpful assistant for our company..."
                        className="min-h-[100px]"
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>The system prompt that defines your chatbot's behavior.</FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="temperature"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Temperature</FormLabel>
                      <FormControl>
                        <Input type="number" step="0.1" min="0" max="1" {...field} />
                      </FormControl>
                      <FormDescription>Controls randomness (0-1).</FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="domain_id"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Domain</FormLabel>
                      <Select
                        onValueChange={(value) => field.onChange(Number.parseInt(value))}
                        defaultValue={field.value.toString()}
                      >
                        <FormControl>
                          <SelectTrigger>
                            <SelectValue placeholder="Select a domain" />
                          </SelectTrigger>
                        </FormControl>
                        <SelectContent>
                          {domains.map((domain) => (
                            <SelectItem key={domain.uuid} value={domain.uuid.toString()}>
                              {domain.domain}
                            </SelectItem>
                          ))}
                        </SelectContent>
                      </Select>
                      <FormDescription>The domain for this chatbot.</FormDescription>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              <div className="grid grid-cols-2 gap-4">
                <FormField
                  control={form.control}
                  name="primary_color"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Primary Color</FormLabel>
                      <FormControl>
                        <div className="flex gap-2">
                          <Input type="color" className="w-10 h-10 p-1" {...field} />
                          <Input {...field} />
                        </div>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
                <FormField
                  control={form.control}
                  name="secondary_color"
                  render={({ field }) => (
                    <FormItem>
                      <FormLabel>Secondary Color</FormLabel>
                      <FormControl>
                        <div className="flex gap-2">
                          <Input type="color" className="w-10 h-10 p-1" {...field} />
                          <Input {...field} />
                        </div>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              {/* <FormField
                control={form.control}
                name="is_active"
                render={({ field }) => (
                  <FormItem className="flex flex-row items-center justify-between rounded-lg border p-4">
                    <div className="space-y-0.5">
                      <FormLabel className="text-base">Active Status</FormLabel>
                      <FormDescription>Whether this chatbot is active and available for use.</FormDescription>
                    </div>
                    <FormControl>
                      <Switch checked={field.value} onCheckedChange={field.onChange} />
                    </FormControl>
                  </FormItem>
                )}
              /> */}
              <DialogFooter>
                <Button type="button" variant="outline" onClick={() => setIsDialogOpen(false)}>
                  Cancel
                </Button>
                <Button type="submit" disabled={isLoading}>
                  {isLoading ? "Saving..." : editingChatbot ? "Update Chatbot" : "Create Chatbot"}
                </Button>
              </DialogFooter>
            </form>
          </Form>
        </DialogContent>
      </Dialog>
    </div>
  )
}


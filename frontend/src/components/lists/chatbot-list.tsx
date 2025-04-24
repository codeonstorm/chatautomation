"use client";

import { useEffect, useRef, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { PlusCircle, Pencil, Trash2, BookOpen, Eye } from "lucide-react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { useForm } from "react-hook-form";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
// import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import { Switch } from "@/components/ui/switch";
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

import { useRouter } from "next/navigation";
import { useSelector } from "react-redux";
import { RootState } from "@/redux/store/store";
import Link from "next/link";
import { Chatbot } from "@/types/chatbot";
import { Domain } from "@/types/domain";
import { createChatbot, getChatbots, updateChatbot, deleteChatbot } from "@/services/chatbot";
import { useAppDispatch } from "@/redux/store/hooks";
import {
  addChatbots,
  editChatbot,
  removeChatbot,
} from "@/redux/store/features/chatbot/chatbot";
import { useAuth } from "@/context/auth-context";

export function ChatbotList() {
  // const [isAuthenticated, setIsLoading] = useState(false);
  const [isLoading, setIsLoading] = useState(false)
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingChatbot, setEditingChatbot] = useState<string | null>(null);
  const { isAuthenticated } = useAuth();

  const router = useRouter();
  const dispatch = useAppDispatch();

  const chatbots: Chatbot[] = useSelector((state: RootState) => state.chatbots);

  const form = useForm<Chatbot>({
    defaultValues: {
      name: "",
      behavior: "",
      description: "",
      system_prompt: "",
      temperature: 0.7,
      primary_color: "#4a56e2",
      secondary_color: "#ffffff",
    },
  });

  const fetchedRef = useRef(false);
  useEffect(() => {
    if (chatbots.length || fetchedRef.current) return;
    fetchedRef.current = true;
    const chatbot = async () => {
      const chatbots: Chatbot[] = await getChatbots();
      dispatch(addChatbots(chatbots));
    };
    chatbot();
  }, []);

  const onSubmit = async (chatbot: Chatbot) => {
    try {
      if(editingChatbot && chatbot) {
        chatbot.uuid = editingChatbot;
        chatbot.status = 'enabled';
        const response: Chatbot = await updateChatbot(chatbot);
        dispatch(editChatbot(response));
        form.reset();
        console.log('edit', editingChatbot , chatbot);

      } else {
        // const response: Chatbot = await createChatbot(chatbot);
        // dispatch(addChatbots([response]));
        // form.reset();
        console.log('new', editingChatbot , chatbot);

      }
      setIsDialogOpen(false);
      setEditingChatbot(null);
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleEdit = (uuid: string) => {

    const chatbot = chatbots.find((bot) => bot.uuid === uuid);
    if (!chatbot) return;
    form.reset({
      name: chatbot.name,
      behavior: chatbot.behavior,
      description: chatbot.description,
      system_prompt: chatbot.system_prompt,
      temperature: chatbot.temperature || 0.7,
      primary_color: chatbot.primary_color,
      secondary_color: chatbot.secondary_color,
    });

    setEditingChatbot(uuid);
    setIsDialogOpen(true);
  };

  const handleDelete = async (uuid: string) => {
    setIsLoading(true);
    try {
      const chatbots: Chatbot = await deleteChatbot(uuid);
      dispatch(removeChatbot(uuid));
    } catch (error) {
      console.error("Error:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const openNewChatbotDialog = () => {
    form.reset({
      name: "",
      behavior: "",
      description: "",
      system_prompt: "",
      temperature: 0.7,
      primary_color: "#4a56e2",
      secondary_color: "#ffffff",
    });
    setEditingChatbot(null);
    setIsDialogOpen(true);
  };

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
              <TableCell>
                <Link href={`http://127.0.0.1:8000/chat/${bot.uuid}`} target="_bank">{bot.name}</Link>
              </TableCell>
              <TableCell>
                <span className="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-green-100 text-green-800">
                  Active
                </span>
              </TableCell>
              <TableCell>{bot.created_at?.replace("T", " ").replaceAll("-", " ")}</TableCell>
              <TableCell>
                <div className="flex space-x-2">
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() => handleEdit(bot.uuid)}
                  >
                    <Pencil className="h-4 w-4 mr-1" /> Edit
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    onClick={() =>
                      router.push(`/dashboard/chatbots/train/${bot.uuid}`)
                    }
                  >
                    <BookOpen className="h-4 w-4 mr-1" /> Train
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="text-blue-500 hover:text-blue-700"
                    onClick={() =>
                      router.push(`/dashboard/chatbots/preview/${bot.uuid}`)
                    }
                  >
                    <Eye className="h-4 w-4 mr-1" /> Preview
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
                        <AlertDialogTitle>Are you sure?</AlertDialogTitle>
                        <AlertDialogDescription>
                          This action cannot be undone. This will permanently
                          delete the chatbot and all its data.
                        </AlertDialogDescription>
                      </AlertDialogHeader>
                      <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction
                          onClick={() => handleDelete(bot.uuid)}
                          className="bg-red-500 hover:bg-red-700"
                        >
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

      {/* Chatbot Form Dialog */}
      <Dialog open={isDialogOpen} onOpenChange={setIsDialogOpen}>
        <DialogContent className="sm:max-w-[600px] overflow-y-scroll max-h-[80vh]">
          <DialogHeader>
            <DialogTitle>
              {editingChatbot ? "Edit Chatbot" : "Create New Chatbot"}
            </DialogTitle>
            <DialogDescription>
              {editingChatbot
                ? "Update your chatbot settings below."
                : "Fill in the details to create a new chatbot."}
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
                      <Input placeholder="Support Bot" required {...field} />
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
                      <Input
                        placeholder="Helpful, friendly assistant"
                        required
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Describe how your chatbot should behave.
                    </FormDescription>
                    <FormMessage />
                  </FormItem>
                )}
              />
              <FormField
                control={form.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Description</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Add chatbot descriotion"
                        className="min-h-[100px]"
                        required
                        {...field}
                      />
                    </FormControl>
                    {/* <FormDescription>Defines your chatbot's role.</FormDescription> */}
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
                        required
                        {...field}
                      />
                    </FormControl>
                    <FormDescription>
                      Defines your chatbot's role.
                    </FormDescription>
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
                        <Input
                          type="number"
                          step="0.1"
                          min="0"
                          max="1"
                          required
                          {...field}
                        />
                      </FormControl>
                      <FormDescription>
                        Controls randomness (0-1).
                      </FormDescription>
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
                          <Input
                            type="color"
                            className="w-10 h-10 p-1"
                            {...field}
                          />
                          <Input required {...field} />
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
                          <Input
                            type="color"
                            className="w-10 h-10 p-1"
                            {...field}
                          />
                          <Input required {...field} />
                        </div>
                      </FormControl>
                      <FormMessage />
                    </FormItem>
                  )}
                />
              </div>
              <DialogFooter>
                <Button
                  type="button"
                  variant="outline"
                  onClick={() => setIsDialogOpen(false)}
                >
                  Cancel
                </Button>
                <Button type="submit" disabled={isLoading}>
                  {isLoading
                    ? "Saving..."
                    : editingChatbot
                    ? "Update Chatbot"
                    : "Create Chatbot"}
                </Button>
              </DialogFooter>
            </form>
          </Form>
        </DialogContent>
      </Dialog>
    </div>
  );
}

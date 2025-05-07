"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Pencil, PlusCircle, Trash2 } from "lucide-react";
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
} from "../ui/alert-dialog";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "../ui/dialog";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "../ui/form";
import { Input } from "@/components/ui/input";
import { Textarea } from "../ui/textarea";

// zod form
import { useForm } from "react-hook-form";
import { z } from "zod";
import { zodResolver } from "@hookform/resolvers/zod";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";
import { useAuth } from "@/context/auth-context";

export const StatusEnum = z.enum(["enabled", "disabled", "deleted"]);
export const IntentEnum = z.enum(["weather check", "Appointment", "check Inventory"]);

const formSchema = z.object({
  intent: IntentEnum.default("weather check"),
  name: z.string().min(1, "Name is required"),
  description: z.string().min(1, "Description is required"),
  type: z.string().default("api"),
  endpoint_url: z.string(),
  require_parameters: z.string().optional(),
  response_schema: z.string().optional(),
  auth_type: z.string().nullable().optional(),
  auth_details: z.string().nullable().optional(),
  status: StatusEnum.default("enabled"),
});

const functions = [
  {
    id: 1,
    name: "Get Weather",
    intent: "weather check",
    status: "Active",
    description: "Fetches current weather for a given location",
  },
  {
    id: 2,
    name: "Book Appointment",
    intent: "Appointment",
    status: "Active",
    description: "Schedules an appointment in the system",
  },
  {
    id: 3,
    name: "Check Inventory",
    intent: "check Inventory",
    status: "Active",
    description: "Checks product availability in inventory",
  },
];

export function FunctionList() {
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [editingFunction, setEditingFunction] = useState<string | null>(null);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      type: "api",
      status: "enabled",
    },
  });

  function onSubmit(values: z.infer<typeof formSchema>) {
    console.log(values);
  }

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Custom Functions</h2>
        <Button
          onClick={() => {
            setEditingFunction(null);
            form.reset();
            setIsDialogOpen(true);
          }}
        >
          <PlusCircle className="mr-2 h-4 w-4" /> Add New Function
        </Button>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Name</TableHead>
            <TableHead>Intent</TableHead>
            <TableHead>Status</TableHead>
            <TableHead>Description</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {functions.map((func) => (
            <TableRow key={func.id}>
              <TableCell>{func.name}</TableCell>
              <TableCell>{func.intent}</TableCell>
              <TableCell>
                <span className="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium bg-green-100 text-green-800">
                  {func.status}
                </span>
              </TableCell>
              <TableCell>{func.description}</TableCell>
              <TableCell className="flex space-x-2">
                <Button
                  variant="outline"
                  size="sm"
                  // onClick={() => handleEdit(func.id)}
                >
                  <Pencil className="h-4 w-4 mr-1" /> Edit
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
                        delete the function and all its data.
                      </AlertDialogDescription>
                    </AlertDialogHeader>
                    <AlertDialogFooter>
                      <AlertDialogCancel>Cancel</AlertDialogCancel>
                      <AlertDialogAction
                        // onClick={() => handleDelete(func.id)}
                        className="bg-red-500 hover:bg-red-700"
                      >
                        Delete
                      </AlertDialogAction>
                    </AlertDialogFooter>
                  </AlertDialogContent>
                </AlertDialog>
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
              {editingFunction ? "Edit Function" : "Create New Function"}
            </DialogTitle>
            <DialogDescription>
              {editingFunction
                ? "Update your function settings below."
                : "Fill in the details to create a new function."}
            </DialogDescription>
          </DialogHeader>

          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              {/* Name */}
              <FormField
                control={form.control}
                name="name"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Name</FormLabel>
                    <FormControl>
                      <Input placeholder="Name" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Intent */}
                            {/* Status */}
                            <FormField
                control={form.control}
                name="intent"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Intent</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select status" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="weather">weather </SelectItem>
                        <SelectItem value="disabled">Disabled</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

                   {/* Description */}
              <FormField
                control={form.control}
                name="description"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Description</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="Enter a detailed description"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

           
              <FormField
                control={form.control}
                name="type"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Type</FormLabel>
                    <FormControl>
                      <Input placeholder="Type" {...field} />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

            
              <FormField
                control={form.control}
                name="endpoint_url"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Endpoint URL</FormLabel>
                    <FormControl>
                      <Input placeholder="Type" {...field}
                        value={field.value || ""}
                        onChange={(e) => field.onChange(e.target.value)}
                          />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <FormField
                control={form.control}
                name="require_parameters"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Description</FormLabel>
                    <FormControl>
                      <Textarea
                        placeholder="require_parameters"
                        {...field}
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />
              

       

              <FormField
                control={form.control}
                name="response_schema"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Response Schema</FormLabel>
                    <FormControl>
                      <Textarea placeholder="Response JSON schema" {...field} 
                      />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Auth Type */}
              <FormField
                control={form.control}
                name="auth_type"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Auth Type</FormLabel>
                    <FormControl>
                      <Input placeholder="OAuth, API Key, etc." {...field}
                        value={field.value || ""}
                        onChange={(e) => field.onChange(e.target.value)}
                          />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Auth Details */}
              <FormField
                control={form.control}
                name="auth_details"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Auth Details</FormLabel>
                    <FormControl>
                      <Input placeholder="Authentication details" {...field} 
                        value={field.value || ""}
                        onChange={(e) => field.onChange(e.target.value)}
                        />
                    </FormControl>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Status */}
              <FormField
                control={form.control}
                name="status"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Status</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      defaultValue={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Select status" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value="enabled">Enabled</SelectItem>
                        <SelectItem value="disabled">Disabled</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Submit Button */}
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
                    : editingFunction
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

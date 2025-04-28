import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { Pencil, PlusCircle, Trash2 } from "lucide-react"
import { AlertDialog, AlertDialogAction, AlertDialogCancel, AlertDialogContent, AlertDialogDescription, AlertDialogFooter, AlertDialogHeader, AlertDialogTitle, AlertDialogTrigger } from "../ui/alert-dialog"

const functions = [
  { id: 1, name: "Get Weather", intent: "weather check", status: "Active", description: "Fetches current weather for a given location" },
  { id: 2, name: "Book Appointment", intent: "Appointment", status: "Active", description: "Schedules an appointment in the system" },
  { id: 3, name: "Check Inventory", intent: "check Inventory", status: "Active", description: "Checks product availability in inventory" },
]

export function FunctionList() {
  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-2xl font-bold">Custom Functions</h2>
        <Button>
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
              <TableCell>
              {/* <div className="flex space-x-2"> */}
                <Button
                  variant="outline"
                  size="sm"
                  // onClick={() => bot.uuid && handleEdit(bot.uuid)}
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
                          delete the chatbot and all its data.
                        </AlertDialogDescription>
                      </AlertDialogHeader>
                      <AlertDialogFooter>
                        <AlertDialogCancel>Cancel</AlertDialogCancel>
                        <AlertDialogAction
                          // onClick={() => bot.uuid && handleDelete(bot.uuid)}
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
    </div>
  )
}


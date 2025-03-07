import { Button } from "@/components/ui/button"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { PlusCircle } from "lucide-react"

const functions = [
  { id: 1, name: "Get Weather", description: "Fetches current weather for a given location" },
  { id: 2, name: "Book Appointment", description: "Schedules an appointment in the system" },
  { id: 3, name: "Check Inventory", description: "Checks product availability in inventory" },
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
            <TableHead>Description</TableHead>
            <TableHead>Actions</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {functions.map((func) => (
            <TableRow key={func.id}>
              <TableCell>{func.name}</TableCell>
              <TableCell>{func.description}</TableCell>
              <TableCell>
                <Button variant="outline" size="sm">
                  Edit
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}


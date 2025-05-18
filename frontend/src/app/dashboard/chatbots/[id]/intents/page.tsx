import { MessageSquare, Plus } from "lucide-react"
import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

// Sample data for intents
const intents = [
  {
    id: "1",
    name: "Greeting",
    description: "Handles user greetings",
    trainingPhrases: 15,
    lastUpdated: "2 days ago",
  },
  {
    id: "2",
    name: "Order Status",
    description: "Checks status of an order",
    trainingPhrases: 24,
    lastUpdated: "5 hours ago",
  },
  {
    id: "3",
    name: "Product Inquiry",
    description: "Handles questions about products",
    trainingPhrases: 32,
    lastUpdated: "1 day ago",
  },
  {
    id: "4",
    name: "Support Request",
    description: "Handles customer support requests",
    trainingPhrases: 18,
    lastUpdated: "3 days ago",
  },
  {
    id: "5",
    name: "Feedback",
    description: "Collects user feedback",
    trainingPhrases: 12,
    lastUpdated: "1 week ago",
  },
]

export default function IntentsPage() {
  return (
    <div className="space-y-6 py-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Intents</h1>
          <p className="text-muted-foreground">Manage and train your conversation intents.</p>
        </div>
        <Button asChild>
          <Link href="/dashboard/intents/create">
            <Plus className="mr-2 h-4 w-4" />
            Create Intent
          </Link>
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All Intents</CardTitle>
          <CardDescription>View and manage all your conversation intents.</CardDescription>
          <div className="flex items-center gap-2">
            <Input placeholder="Search intents..." className="max-w-sm" />
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Description</TableHead>
                <TableHead>Training Phrases</TableHead>
                <TableHead>Last Updated</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {intents.map((intent) => (
                <TableRow key={intent.id}>
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-2">
                      <MessageSquare className="h-4 w-4 text-muted-foreground" />
                      {intent.name}
                    </div>
                  </TableCell>
                  <TableCell>{intent.description}</TableCell>
                  <TableCell>{intent.trainingPhrases}</TableCell>
                  <TableCell>{intent.lastUpdated}</TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button asChild variant="ghost" size="sm">
                        <Link href={`/dashboard/intents/${intent.id}`}>Edit</Link>
                      </Button>
                      <Button asChild variant="ghost" size="sm">
                        <Link href={`/dashboard/intents/${intent.id}/train`}>Train</Link>
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}

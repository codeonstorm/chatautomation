import { Plus, Webhook } from "lucide-react"
import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

// Sample data for webhooks
const webhooks = [
  {
    id: "1",
    name: "Order API",
    url: "https://api.example.com/orders",
    intents: ["Order Status", "Place Order"],
    lastUpdated: "1 day ago",
    status: "Active",
  },
  {
    id: "2",
    name: "Product Catalog",
    url: "https://api.example.com/products",
    intents: ["Product Inquiry"],
    lastUpdated: "3 days ago",
    status: "Active",
  },
  {
    id: "3",
    name: "Customer Support",
    url: "https://api.example.com/support",
    intents: ["Support Request"],
    lastUpdated: "1 week ago",
    status: "Inactive",
  },
  {
    id: "4",
    name: "Feedback Collection",
    url: "https://api.example.com/feedback",
    intents: ["Feedback"],
    lastUpdated: "2 weeks ago",
    status: "Active",
  },
]

export default function WebhooksPage() {
  return (
    <div className="space-y-6 py-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Webhooks</h1>
          <p className="text-muted-foreground">Manage webhooks for your conversational AI.</p>
        </div>
        <Button asChild>
          <Link href="/dashboard/webhooks/create">
            <Plus className="mr-2 h-4 w-4" />
            Create Webhook
          </Link>
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All Webhooks</CardTitle>
          <CardDescription>View and manage all your webhooks.</CardDescription>
          <div className="flex items-center gap-2">
            <Input placeholder="Search webhooks..." className="max-w-sm" />
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>URL</TableHead>
                <TableHead>Mapped Intents</TableHead>
                <TableHead>Status</TableHead>
                <TableHead>Last Updated</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {webhooks.map((webhook) => (
                <TableRow key={webhook.id}>
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-2">
                      <Webhook className="h-4 w-4 text-muted-foreground" />
                      {webhook.name}
                    </div>
                  </TableCell>
                  <TableCell className="font-mono text-xs">{webhook.url}</TableCell>
                  <TableCell>
                    <div className="flex flex-wrap gap-1">
                      {webhook.intents.map((intent) => (
                        <span
                          key={intent}
                          className="inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold"
                        >
                          {intent}
                        </span>
                      ))}
                    </div>
                  </TableCell>
                  <TableCell>
                    <span
                      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold ${
                        webhook.status === "Active"
                          ? "bg-green-50 text-green-700 dark:bg-green-900/20 dark:text-green-400"
                          : "bg-yellow-50 text-yellow-700 dark:bg-yellow-900/20 dark:text-yellow-400"
                      }`}
                    >
                      {webhook.status}
                    </span>
                  </TableCell>
                  <TableCell>{webhook.lastUpdated}</TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button asChild variant="ghost" size="sm">
                        <Link href={`/dashboard/webhooks/${webhook.id}`}>Edit</Link>
                      </Button>
                      <Button asChild variant="ghost" size="sm">
                        <Link href={`/dashboard/webhooks/${webhook.id}/test`}>Test</Link>
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

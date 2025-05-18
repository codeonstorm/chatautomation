import { FileJson, Plus } from "lucide-react"
import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"

// Sample data for entities
const entities = [
  {
    id: "1",
    name: "Product",
    type: "List",
    values: 24,
    lastUpdated: "3 days ago",
  },
  {
    id: "2",
    name: "OrderID",
    type: "Pattern",
    values: 1,
    lastUpdated: "1 week ago",
  },
  {
    id: "3",
    name: "Date",
    type: "System",
    values: "Built-in",
    lastUpdated: "N/A",
  },
  {
    id: "4",
    name: "Location",
    type: "List",
    values: 15,
    lastUpdated: "2 days ago",
  },
  {
    id: "5",
    name: "Price",
    type: "Pattern",
    values: 1,
    lastUpdated: "5 days ago",
  },
]

export default function EntitiesPage() {
  return (
    <div className="space-y-6 py-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight">Entities</h1>
          <p className="text-muted-foreground">Manage entities for your conversational AI.</p>
        </div>
        <Button asChild>
          <Link href="/dashboard/entities/create">
            <Plus className="mr-2 h-4 w-4" />
            Create Entity
          </Link>
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All Entities</CardTitle>
          <CardDescription>View and manage all your entities.</CardDescription>
          <div className="flex items-center gap-2">
            <Input placeholder="Search entities..." className="max-w-sm" />
          </div>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Name</TableHead>
                <TableHead>Type</TableHead>
                <TableHead>Values</TableHead>
                <TableHead>Last Updated</TableHead>
                <TableHead className="text-right">Actions</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {entities.map((entity) => (
                <TableRow key={entity.id}>
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-2">
                      <FileJson className="h-4 w-4 text-muted-foreground" />
                      {entity.name}
                    </div>
                  </TableCell>
                  <TableCell>{entity.type}</TableCell>
                  <TableCell>{entity.values}</TableCell>
                  <TableCell>{entity.lastUpdated}</TableCell>
                  <TableCell className="text-right">
                    <div className="flex justify-end gap-2">
                      <Button asChild variant="ghost" size="sm">
                        <Link href={`/dashboard/entities/${entity.id}`}>Edit</Link>
                      </Button>
                      <Button asChild variant="ghost" size="sm">
                        <Link href={`/dashboard/entities/${entity.id}/values`}>Values</Link>
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

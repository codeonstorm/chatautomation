"use client";

import { FileJson, Plus } from "lucide-react"
import Link from "next/link"

import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Input } from "@/components/ui/input"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table"
import { SidebarInset, SidebarTrigger } from "@/components/ui/sidebar"
import { Separator } from "@radix-ui/react-separator"
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink, BreadcrumbList, BreadcrumbPage, BreadcrumbSeparator } from "@/components/ui/breadcrumb"
import { DarkModeToggle } from "@/components/darkmodetoogle"
import { useParams } from "next/navigation"

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
  const params = useParams()
  const id = params.id as string; 

  return (
    <SidebarInset>
      <header className="flex h-16 shrink-0 items-center justify-between gap-2 px-4 transition-[width,height] ease-linear group-has-[[data-collapsible=icon]]/sidebar-wrapper:h-12">
        {" "}
        <div className="flex items-center gap-2 px-4">
          <SidebarTrigger className="-ml-1" />
          <Separator orientation="vertical" className="mr-2 h-4" />
          <Breadcrumb>
            <BreadcrumbList>
              <BreadcrumbItem className="hidden md:block">
                <BreadcrumbLink href="/dashboard">Dashboard</BreadcrumbLink>
              </BreadcrumbItem>
              <BreadcrumbSeparator className="hidden md:block" />
              <BreadcrumbItem>
                <BreadcrumbPage>Chatbot Traning</BreadcrumbPage>
              </BreadcrumbItem>
            </BreadcrumbList>
          </Breadcrumb>
        </div>
        <DarkModeToggle />
      </header>

      <div className="flex-1 flex h-[calc(100vh-4rem)]">
        <div className="flex flex-1 flex-col gap-4 p-4 pt-0">
      <div className="space-y-6 py-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Entities</h1>
            <p className="text-muted-foreground">Manage entities for your conversational AI.</p>
          </div>
          <Button asChild>
            <Link href={`/dashboard/chatbots/${id}/entities/create`}>
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
                      </div>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>
      </div>
      </div>
      </div>
    </SidebarInset>
  )
}

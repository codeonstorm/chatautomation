"use client";

import { FileJson, Plus, Trash2 } from "lucide-react"
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
import { use, useEffect, useState } from "react";
import { useAuth } from "@/context/auth-context";
import { deleteEntity, getEntities } from "@/services/entities_service";
import { Entity } from "@/types/entity";

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

export default function EntitiesPage() {
  const { user } = useAuth();
  const params = useParams();
  const id = params.id as string;
  const [entities, setEntities] = useState<Entity[]>([])

  useEffect(() => {
    const fetchEntities = async () => {
      if (!user || !user.services || user.services.length === 0) {
        return;
      }
      try {
        const entitieslist:Entity[] = await getEntities(user?.services[0].id, id);
        setEntities(entitieslist);
      } catch (error) {
        // console.error("Error fetching entities:", error);
      }
    };

    fetchEntities();
    console.log(entities)
  }, [user, id]);

  const handleDelete = async (entityId: string) => {
    if (!user || !user.services || user.services.length === 0) return;
    try {
      await deleteEntity(user?.services[0].id, id, entityId)
      setEntities((prev) => prev.filter((entity) => entityId != entityId));
    } catch (error) {
      // Optionally handle error
    }
  };

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
                  {/* <TableHead>Last Updated</TableHead> */}
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
                    <TableCell>{entity.entity_type}</TableCell>
                    <TableCell>{entity.value && Object.keys(entity.value).length}</TableCell>
                    {/* <TableCell>{entity.lastUpdated}</TableCell> */}
                    <TableCell className="text-right">
                      <div className="flex justify-end gap-2">
                        <Button asChild variant="ghost" size="sm">
                          <Link href={`/dashboard/chatbots/${id}/entities/edit/${entity.id}`}>Edit</Link>
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
                          onClick={() => handleDelete(String(entity.id))}
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
          </CardContent>
        </Card>
      </div>
      </div>
      </div>
    </SidebarInset>
  )
}

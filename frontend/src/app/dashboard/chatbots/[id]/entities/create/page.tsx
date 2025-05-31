"use client";

import type React from "react";

import { useEffect, useState } from "react";
import { Plus, Save, Trash2 } from "lucide-react";
import { useParams, useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Separator } from "@/components/ui/separator";
import { Textarea } from "@/components/ui/textarea";
import { DarkModeToggle } from "@/components/darkmodetoogle";
import { SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { createEntity, getEntity } from "@/services/entities_service";
import { useAuth } from "@/context/auth-context";
// import { toast } from "@/components/ui/use-toast"

export default function CreateEntityPage() {
  const router = useRouter();
  const { user } = useAuth();
  const params = useParams()
  const [entityType, setEntityType] = useState("list");
  const [entityValues, setEntityValues] = useState<
    { value: string; synonyms: string[] }[]
  >([
    { value: "Laptop", synonyms: ["Notebook", "Computer"] },
    { value: "Smartphone", synonyms: ["Phone", "Mobile", "Cell phone"] },
  ]);
  const [newValue, setNewValue] = useState("");
  const [newSynonym, setNewSynonym] = useState("");
  const [selectedValueIndex, setSelectedValueIndex] = useState<number | null>(
    null
  );
  const [entityName, setEntityName] = useState("");
  const [entityDescription, setEntityDescription] = useState("");
  const [patternValue, setPatternValue] = useState("");
  const chatbot_uuid = params.id as string;
  const serviceid = user?.services[0].id; 

  //  useEffect(() => {
  //    if (!user) return;
 
  //    const fetchEntity = async () => {
  //      try {
  //       await getEntity(user.services[0].id, params.id as string);
  //      } catch (err) {
  //        console.log("No webhook found or failed to load", err);
  //      }
  //    };
 
  //    fetchEntity();
  //  }, [user, params.id]);

  const addEntityValue = () => {
    if (newValue.trim()) {
      setEntityValues([
        ...entityValues,
        { value: newValue.trim(), synonyms: [] },
      ]);
      setNewValue("");
    }
  };

  const removeEntityValue = (index: number) => {
    setEntityValues(entityValues.filter((_, i) => i !== index));
    if (selectedValueIndex === index) {
      setSelectedValueIndex(null);
    }
  };

  const addSynonym = () => {
    if (selectedValueIndex !== null && newSynonym.trim()) {
      const updatedValues = [...entityValues];
      updatedValues[selectedValueIndex].synonyms.push(newSynonym.trim());
      setEntityValues(updatedValues);
      setNewSynonym("");
    }
  };

  const removeSynonym = (valueIndex: number, synonymIndex: number) => {
    const updatedValues = [...entityValues];
    updatedValues[valueIndex].synonyms = updatedValues[
      valueIndex
    ].synonyms.filter((_, i) => i !== synonymIndex);
    setEntityValues(updatedValues);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if(!serviceid) return
    var data = {}

    var filteredEntity: Record<string, string[]> = {};
    entityValues.forEach(item => {
      filteredEntity[item.value] = item.synonyms;
    });

    if (entityType == 'list') {
      data = {
        name: entityName,
        description: entityDescription,
        entity_type: entityType,
        value: filteredEntity,
      }

    } else if (entityType == 'pattern') {
      data = {
        name: entityName,
        description: entityDescription,
        entity_type: entityType,
        value: {'regex': [patternValue]},
      }
    } else {
      alert('this feature not available. come in future')
      return
    }

    try {
      await createEntity(serviceid, chatbot_uuid, data)
      router.push(`/dashboard/chatbots/${chatbot_uuid}/entities`);
    } catch (error) {
      console.error("Error creating entity:", error);
    }
    // toast({
    //   title: "Entity created",
    //   description: "Your entity has been created successfully.",
    // })
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
            <div>
              <h1 className="text-3xl font-bold tracking-tight">
                Create Entity
              </h1>
              <p className="text-muted-foreground">
                Create a new entity for your conversational AI.
              </p>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="grid gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Entity Details</CardTitle>
                    <CardDescription>
                      Basic information about your entity.
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid gap-2">
                      <Label htmlFor="name">Entity Name</Label>
                      <Input
                        id="name"
                        placeholder="e.g., Product, Location, Date"
                        required
                        value={entityName}
                        onChange={(e) => setEntityName(e.target.value)}
                      />
                    </div>
                    <div className="grid gap-2">
                      <Label htmlFor="description">Description</Label>
                      <Textarea
                        id="description"
                        placeholder="Describe what this entity is for..."
                        className="min-h-[100px]"
                        value={entityDescription}
                        onChange={(e) => setEntityDescription(e.target.value)}
                      />
                    </div>
                  </CardContent>
                </Card>

                <Card>
                  <CardHeader>
                    <CardTitle>Entity Type</CardTitle>
                    <CardDescription>
                      Select the type of entity you want to create.
                    </CardDescription>
                  </CardHeader>
                  <CardContent>
                    <RadioGroup
                      defaultValue="list"
                      value={entityType}
                      onValueChange={setEntityType}
                      className="space-y-4"
                    >
                      <div className="flex items-start space-x-2 rounded-md border p-4">
                        <RadioGroupItem
                          value="list"
                          id="list"
                          className="mt-1"
                        />
                        <div className="space-y-1">
                          <Label htmlFor="list" className="font-medium">
                            List
                          </Label>
                          <p className="text-sm text-muted-foreground">
                            Define a list of values and synonyms. Best for
                            entities with a fixed set of values.
                          </p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-2 rounded-md border p-4">
                        <RadioGroupItem
                          value="pattern"
                          id="pattern"
                          className="mt-1"
                        />
                        <div className="space-y-1">
                          <Label htmlFor="pattern" className="font-medium">
                            Pattern
                          </Label>
                          <p className="text-sm text-muted-foreground">
                            Define a regular expression pattern. Best for
                            entities with a specific format.
                          </p>
                        </div>
                      </div>
                      <div className="flex items-start space-x-2 rounded-md border p-4">
                        <RadioGroupItem
                          value="system"
                          id="system"
                          className="mt-1"
                        />
                        <div className="space-y-1">
                          <Label htmlFor="system" className="font-medium">
                            System
                          </Label>
                          <p className="text-sm text-muted-foreground">
                            Use a built-in system entity like date, time,
                            number, etc.
                          </p>
                        </div>
                      </div>
                    </RadioGroup>
                  </CardContent>
                </Card>

                {entityType === "list" && (
                  <Card>
                    <CardHeader>
                      <CardTitle>Entity Values</CardTitle>
                      <CardDescription>
                        Add values and synonyms for your entity.
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="flex gap-2">
                        <Input
                          placeholder="Add a value..."
                          value={newValue}
                          onChange={(e) => setNewValue(e.target.value)}
                          onKeyDown={(e) =>
                            e.key === "Enter" && addEntityValue()
                          }
                        />
                        <Button type="button" onClick={addEntityValue}>
                          <Plus className="h-4 w-4" />
                          <span className="sr-only">Add</span>
                        </Button>
                      </div>

                      <div className="grid gap-4 md:grid-cols-2">
                        <div className="space-y-2">
                          <h3 className="text-sm font-medium">Values</h3>
                          <div className="space-y-2">
                            {entityValues.map((value, index) => (
                              <div
                                key={index}
                                className={`flex items-center justify-between rounded-md border p-3 ${
                                  selectedValueIndex === index
                                    ? "border-primary"
                                    : ""
                                }`}
                                onClick={() => setSelectedValueIndex(index)}
                              >
                                <div className="flex items-center gap-2">
                                  <span>{value.value}</span>
                                  <span className="text-xs text-muted-foreground">
                                    ({value.synonyms.length} synonyms)
                                  </span>
                                </div>
                                <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    removeEntityValue(index);
                                  }}
                                >
                                  <Trash2 className="h-4 w-4" />
                                  <span className="sr-only">Remove</span>
                                </Button>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div className="space-y-2">
                          <h3 className="text-sm font-medium">Synonyms</h3>
                          {selectedValueIndex !== null ? (
                            <div className="space-y-2">
                              <div className="flex gap-2">
                                <Input
                                  placeholder="Add a synonym..."
                                  value={newSynonym}
                                  onChange={(e) =>
                                    setNewSynonym(e.target.value)
                                  }
                                  onKeyDown={(e) =>
                                    e.key === "Enter" && addSynonym()
                                  }
                                />
                                <Button type="button" onClick={addSynonym}>
                                  <Plus className="h-4 w-4" />
                                  <span className="sr-only">Add</span>
                                </Button>
                              </div>

                              <div className="space-y-2">
                                {entityValues[selectedValueIndex].synonyms.map(
                                  (synonym, synIndex) => (
                                    <div
                                      key={synIndex}
                                      className="flex items-center justify-between rounded-md border p-3"
                                    >
                                      <span>{synonym}</span>
                                      <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() =>
                                          removeSynonym(
                                            selectedValueIndex,
                                            synIndex
                                          )
                                        }
                                      >
                                        <Trash2 className="h-4 w-4" />
                                        <span className="sr-only">Remove</span>
                                      </Button>
                                    </div>
                                  )
                                )}

                                {entityValues[selectedValueIndex].synonyms
                                  .length === 0 && (
                                  <div className="rounded-md border border-dashed p-3 text-center text-sm text-muted-foreground">
                                    No synonyms added yet
                                  </div>
                                )}
                              </div>
                            </div>
                          ) : (
                            <div className="rounded-md border border-dashed p-3 text-center text-sm text-muted-foreground">
                              Select a value to add synonyms
                            </div>
                          )}
                        </div>
                      </div>
                    </CardContent>
                    <CardFooter>
                      <div className="text-sm text-muted-foreground">
                        Synonyms help your bot recognize different ways users
                        might refer to the same entity.
                      </div>
                    </CardFooter>
                  </Card>
                )}

                {entityType === "pattern" && (
                  <Card>
                    <CardHeader>
                      <CardTitle>Pattern Definition</CardTitle>
                      <CardDescription>
                        Define a regular expression pattern for your entity.
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="grid gap-2">
                        <Label htmlFor="pattern">
                          Regular Expression Pattern
                        </Label>
                        <Input
                          id="pattern"
                          placeholder="e.g., [A-Z]{2}[0-9]{4}"  
                          onChange={(e) =>
                            setPatternValue(e.target.value)}
                        />
                      </div>
                      <div className="rounded-md bg-muted p-4">
                        <h3 className="mb-2 text-sm font-medium">
                          Pattern Examples
                        </h3>
                        <div className="space-y-2 text-sm">
                          <div className="flex items-center justify-between">
                            <code>
                              [A-Z]{2}[0-9]{4}
                            </code>
                            <span>Order IDs (e.g., AB1234)</span>
                          </div>
                          <Separator />
                          <div className="flex items-center justify-between">
                            <code>
                              [0-9]{3}-[0-9]{3}-[0-9]{4}
                            </code>
                            <span>Phone numbers (e.g., 123-456-7890)</span>
                          </div>
                          <Separator />
                          <div className="flex items-center justify-between">
                            <code>
                              [a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2}
                            </code>
                            <span>Email addresses</span>
                          </div>
                        </div>
                      </div>
                    </CardContent>
                  </Card>
                )}

                {entityType === "system" && (
                  <Card>
                    <CardHeader>
                      <CardTitle>System Entity</CardTitle>
                      <CardDescription>
                        Select a built-in system entity.
                      </CardDescription>
                    </CardHeader>
                    <CardContent>
                      <RadioGroup defaultValue="date" className="space-y-4">
                        <div className="flex items-start space-x-2 rounded-md border p-4">
                          <RadioGroupItem
                            value="date"
                            id="date"
                            className="mt-1"
                          />
                          <div className="space-y-1">
                            <Label htmlFor="date" className="font-medium">
                              Date
                            </Label>
                            <p className="text-sm text-muted-foreground">
                              Recognizes dates in various formats (e.g.,
                              "tomorrow", "May 5th", "2023-06-15").
                            </p>
                          </div>
                        </div>
                        <div className="flex items-start space-x-2 rounded-md border p-4">
                          <RadioGroupItem
                            value="time"
                            id="time"
                            className="mt-1"
                          />
                          <div className="space-y-1">
                            <Label htmlFor="time" className="font-medium">
                              Time
                            </Label>
                            <p className="text-sm text-muted-foreground">
                              Recognizes times in various formats (e.g., "3pm",
                              "15:30", "in 10 minutes").
                            </p>
                          </div>
                        </div>
                        <div className="flex items-start space-x-2 rounded-md border p-4">
                          <RadioGroupItem
                            value="number"
                            id="number"
                            className="mt-1"
                          />
                          <div className="space-y-1">
                            <Label htmlFor="number" className="font-medium">
                              Number
                            </Label>
                            <p className="text-sm text-muted-foreground">
                              Recognizes numbers in various formats (e.g., "42",
                              "forty-two", "4.2").
                            </p>
                          </div>
                        </div>
                        <div className="flex items-start space-x-2 rounded-md border p-4">
                          <RadioGroupItem
                            value="currency"
                            id="currency"
                            className="mt-1"
                          />
                          <div className="space-y-1">
                            <Label htmlFor="currency" className="font-medium">
                              Currency
                            </Label>
                            <p className="text-sm text-muted-foreground">
                              Recognizes currency amounts (e.g., "$10", "10
                              dollars", "€50").
                            </p>
                          </div>
                        </div>
                      </RadioGroup>
                    </CardContent>
                  </Card>
                )}

                <div className="flex justify-end gap-2">
                  <Button
                    variant="outline"
                    type="button"
                    onClick={() => router.push("/dashboard/entities")}
                  >
                    Cancel
                  </Button>
                  <Button type="submit">
                    <Save className="mr-2 h-4 w-4" />
                    Save Entity
                  </Button>
                </div>
              </div>
            </form>
          </div>
        </div>
      </div>
    </SidebarInset>
  );
}

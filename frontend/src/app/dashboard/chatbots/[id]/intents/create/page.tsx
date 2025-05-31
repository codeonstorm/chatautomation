"use client";

import type React from "react";

import { useEffect, useState } from "react";
import { Bot, Plus, Save, Trash2 } from "lucide-react";
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
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Textarea } from "@/components/ui/textarea";
import { SidebarInset, SidebarTrigger } from "@/components/ui/sidebar";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Separator } from "@radix-ui/react-separator";
import { DarkModeToggle } from "@/components/darkmodetoogle";
import { Checkbox } from "@/components/ui/checkbox";
import {
  Select,
  SelectContent,
  SelectGroup,
  SelectItem,
  SelectLabel,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import { Switch } from "@/components/ui/switch";
// import { toast } from "@/components/ui/use-toast"
import { Intent } from "@/types/intent.js"
import { createEntity, getEntities } from "@/services/entities_service";
import { useAuth } from "@/context/auth-context";
import { createIntent } from "@/services/intents_service";
import { Entity } from "@/types/entity";

export default function CreateIntentPage() {
  const router = useRouter();
  const params = useParams()
  const { user } = useAuth();

  const [trainingPhrases, setTrainingPhrases] = useState<string[]>([]);
  // [
  //   "Hello there",
  //   "Hi, how are you?",
  //   "Good morning",
  // ]
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [newPhrase, setNewPhrase] = useState("");
  const [responses, setResponses] = useState<string[]>([]);
  const [newResponse, setNewResponse] = useState("");
  const [newValue, setNewValue] = useState("");
  const [newParamMessage, setNewParamMessage] = useState("");

  const [entityType, setEntityType] = useState("list");
  const [parameters, setParameter] = useState<
    { parameter: string; required: boolean; messages: string[] }[]
  >([]);
    // { parameter: "Laptop", required: true, messages: ["Notebook", "Computer"] },
    // { parameter: "Smartphone", required: true, messages: ["Phone", "Mobile", "Cell phone"] },
  const [selectedValueIndex, setSelectedValueIndex] = useState<number | null>(
    null
  );

  const [entities, setEntities] = useState<Entity[]>([])
  useEffect(() => {
    const fetchEntities = async () => {
      if (!user || !user.services || user.services.length === 0) {
        return;
      }
      try {
        const entitieslist:Entity[] = await getEntities(user?.services[0].id, params.id as string);
        setEntities(entitieslist);
      } catch (error) {
        // console.error("Error fetching entities:", error);
      }
    };
    fetchEntities();
  }, [user, params.id]);

  if (!user) {
    return
  }
  const serviceid = user.services[0].id; 
  const chatbot_uuid = params.id as string;

  const addTrainingPhrase = () => {
    if (newPhrase.trim()) {
      setTrainingPhrases([...trainingPhrases, newPhrase.trim()]);
      setNewPhrase("");
      // toast({
      //   title: "Training phrase added",
      //   description: "Your training phrase has been added successfully.",
      // })
    }
  };

  const removeTrainingPhrase = (index: number) => {
    setTrainingPhrases(trainingPhrases.filter((_, i) => i !== index));
  };

  const addResponse = () => {
    if (newResponse.trim()) {
      setResponses([...responses, newResponse.trim()]);
      setNewResponse("");
      // toast({
      //   title: "Response added",
      //   description: "Your response has been added successfully.",
      // })
    }
  };

  const removeResponse = (index: number) => {
    setResponses(responses.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const filteredParam = parameters.map(v => ({
      parameter: v.parameter,
      required: v.required,
      message: v.messages[0]
    }));

    var data = {
      name,
      description,
      "phrases": trainingPhrases,
      "default_intent_responses": responses,
      "action": {
        "name": "string",
        "webhook": true,
        "parameters": [
          ...filteredParam
        ]
      }

    }
   
    try {
      await createIntent(serviceid, chatbot_uuid, data)
      router.push(`/dashboard/chatbots/${chatbot_uuid}/intents`);
    } catch (error) {
      console.log(error)
    }

    console.log(data)
    // toast({
    //   title: "Intent created",
    //   description: "Your intent has been created successfully.",
    // })
    // router.push("/dashboard/intents");
  };

  // =========
    const addEntityValue = () => {
    if (newValue.trim()) {
      setParameter([
        ...parameters,
        { parameter: newValue.trim(), required: false, messages: [] },
      ]);
      setNewValue("");
    }
  };

  const addValidatioMessage = () => {
    if (selectedValueIndex !== null && newParamMessage.trim()) {
      const updatedValues = [...parameters];
      updatedValues[selectedValueIndex].messages.push(newParamMessage.trim());
      setParameter(updatedValues);
      setNewParamMessage("");
    }
  };

  const removeParamMessage = (valueIndex: number, synonymIndex: number) => {
    const updatedValues = [...parameters];
    updatedValues[valueIndex].messages = updatedValues[
      valueIndex
    ].messages.filter((_, i) => i !== synonymIndex);
    setParameter(updatedValues);
  };

  const removeEntityValue = (index: number) => {
    setParameter(parameters.filter((_, i) => i !== index));
    if (selectedValueIndex === index) {
      setSelectedValueIndex(null);
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
            <div>
              <h1 className="text-3xl font-bold tracking-tight">
                Create Intent
              </h1>
              <p className="text-muted-foreground">
                Create a new intent for your conversational AI.
              </p>
            </div>

            <form onSubmit={handleSubmit}>
              <div className="grid gap-6">
                <Card>
                  <CardHeader>
                    <CardTitle>Intent Details</CardTitle>
                    <CardDescription>
                      Basic information about your intent.
                    </CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid gap-2">
                      <Label htmlFor="name">Intent Name</Label>
                      <Input
                        id="name"
                        placeholder="e.g., Greeting, Order Status"
                        value={name}
                        required
                        onChange={(e) =>setName(e.target.value)}
                      />
                    </div>
                    <div className="grid gap-2">
                      <Label htmlFor="description">Description</Label>
                      <Textarea
                        id="description"
                        placeholder="Describe what this intent is for..."
                        className="min-h-[100px]"
                        value={description}
                        onChange={(e) =>setDescription(e.target.value)}
                      />
                    </div>
                  </CardContent>
                </Card>

                <Tabs defaultValue="training">
                  <TabsList className="grid w-full grid-cols-3">
                    <TabsTrigger value="training">Training Phrases</TabsTrigger>
                    <TabsTrigger value="responses">Responses</TabsTrigger>
                    <TabsTrigger value="parameters">Action & Parameters</TabsTrigger>
                  </TabsList>

                  <TabsContent value="training" className="space-y-4 pt-4">
                    <Card>
                      <CardHeader>
                        <CardTitle>Training Phrases</CardTitle>
                        <CardDescription>
                          Add phrases that users might say to trigger this
                          intent.
                        </CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="flex gap-2">
                          <Input
                            placeholder="Add a training phrase..."
                            value={newPhrase}
                            onChange={(e) => setNewPhrase(e.target.value)}
                            onKeyDown={(e) =>
                              e.key === "Enter" && addTrainingPhrase()
                            }
                          />
                          <Button type="button" onClick={addTrainingPhrase}>
                            <Plus className="h-4 w-4" />
                            <span className="sr-only">Add</span>
                          </Button>
                        </div>

                        <div className="space-y-2">
                          {trainingPhrases.map((phrase, index) => (
                            <div
                              key={index}
                              className="flex items-center justify-between rounded-md border p-3"
                            >
                              <div className="flex items-center gap-2">
                                <span>{phrase}</span>
                              </div>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => removeTrainingPhrase(index)}
                              >
                                <Trash2 className="h-4 w-4" />
                                <span className="sr-only">Remove</span>
                              </Button>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                      <CardFooter>
                        <div className="text-sm text-muted-foreground">
                          Add at least 5-10 training phrases for better intent
                          recognition.
                        </div>
                      </CardFooter>
                    </Card>
                  </TabsContent>

                  <TabsContent value="responses" className="space-y-4 pt-4">
                    <Card>
                      <CardHeader>
                        <CardTitle>Responses</CardTitle>
                        <CardDescription>
                          Add responses that your bot will use when this intent
                          is triggered.
                        </CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="flex gap-2">
                          <Input
                            placeholder="Add a response..."
                            value={newResponse}
                            onChange={(e) => setNewResponse(e.target.value)}
                            onKeyDown={(e) =>
                              e.key === "Enter" && addResponse()
                            }
                          />
                          <Button type="button" onClick={addResponse}>
                            <Plus className="h-4 w-4" />
                            <span className="sr-only">Add</span>
                          </Button>
                        </div>

                        <div className="space-y-2">
                          {responses.map((response, index) => (
                            <div
                              key={index}
                              className="flex items-center justify-between rounded-md border p-3"
                            >
                              <div className="flex items-center gap-2">
                                <Bot className="h-4 w-4 text-muted-foreground" />
                                <span>{response}</span>
                              </div>
                              <Button
                                variant="ghost"
                                size="sm"
                                onClick={() => removeResponse(index)}
                              >
                                <Trash2 className="h-4 w-4" />
                                <span className="sr-only">Remove</span>
                              </Button>
                            </div>
                          ))}
                        </div>
                      </CardContent>
                      <CardFooter>
                        <div className="text-sm text-muted-foreground">
                          Add multiple responses for variety in your bot's
                          replies.
                        </div>
                      </CardFooter>
                    </Card>
                  </TabsContent>

                  <TabsContent value="parameters" className="space-y-4 pt-4">
                  <Card>
                    <CardHeader>
                      <CardTitle>Add Action & Prameters</CardTitle>
                      <CardDescription>
                        Add action & parameters to compete task.
                      </CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                      <div className="flex flex-col gap-2">
                        <Label htmlFor="action-name">Action</Label>
                        <Input
                          id="action-name"
                          placeholder="Add Action name"
                        />
                      </div>

                      <div className="flex gap-2">
                        <Label htmlFor="sentiment-analysis" className="flex items-center gap-2">
                        <Switch
                          id="sentiment-analysis"
                          // checked={sentimentAnalysis}
                          // onCheckedChange={handleSentimentAnalysisChange}
                        />
                          Enable Webhook
                        </Label>

                      </div>

                      <div className="flex gap-2 pt-8">
                        {/* <Label htmlFor="entity-select">Select Entity for Parameter</Label> */}
                        <Select
                          value={newValue}
                          onValueChange={(value) => setNewValue(value)}
                        >
                          <SelectTrigger id="entity-select" className="w-[200px]">
                            <SelectValue placeholder="Select an entity..." />
                          </SelectTrigger>
                          <SelectContent>
                            <SelectGroup>
                              <SelectLabel>Entities</SelectLabel>
                              {
                                entities.map(v => (<SelectItem key={v.id} value={v.name}>{v.name}</SelectItem>))
                              }
                              </SelectGroup>
                          </SelectContent>
                        </Select>
                        <Button type="button" onClick={addEntityValue}>
                          <Plus className="h-4 w-4" />
                          <span className="sr-only">Add</span>
                        </Button>
                      </div>

                      <div className="grid gap-4 md:grid-cols-2">
                        <div className="space-y-2">
                          <h3 className="text-sm font-medium">Parameters</h3>
                          <div className="space-y-2">
                            {parameters.map((value, index) => (
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
                                  <span>{value.parameter}</span>
                                  <span className="text-xs text-muted-foreground">
                                    ({value.messages.length} Default replies)
                                  </span>
                                </div>
                                <div className="flex items-center gap-2">
                                  <div className="flex items-center gap-1">
                                  <Checkbox
                                    checked={value.required}
                                    onCheckedChange={(checked) => {
                                    const updated = [...parameters];
                                    updated[index].required = !!checked;
                                    setParameter(updated);
                                    }}
                                    id={`required-checkbox-${index}`}
                                  />
                                  <label
                                    htmlFor={`required-checkbox-${index}`}
                                    className="text-xs text-muted-foreground cursor-pointer"
                                    title="Check if this parameter is required for the action"
                                  >
                                    Required
                                  </label>
                                  </div>
                                  <Button
                                  variant="ghost"
                                  size="sm"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    removeEntityValue(index);
                                  }}
                                  title="Remove this parameter"
                                  >
                                  <Trash2 className="h-4 w-4" />
                                  <span className="sr-only">Remove</span>
                                  </Button>
                                </div>
                              </div>
                            ))}
                          </div>
                        </div>

                        <div className="space-y-2">
                          <h3 className="text-sm font-medium">Default replies (Check required option to add default reply)</h3>
                          {selectedValueIndex !== null ? (
                            <div className="space-y-2">
                              <div className="flex gap-2">
                                <Input
                                  placeholder="Add a reply..."
                                  value={newParamMessage}
                                  onChange={(e) =>
                                    setNewParamMessage(e.target.value)
                                  }
                                  onKeyDown={(e) =>
                                    e.key === "Enter" && addValidatioMessage()
                                  }
                                />
                                <Button type="button" onClick={addValidatioMessage}>
                                  <Plus className="h-4 w-4" />
                                  <span className="sr-only">Add</span>
                                </Button>
                              </div>

                              <div className="space-y-2">
                                {parameters[selectedValueIndex].required && parameters[selectedValueIndex].messages.slice(0, 1).map(
                                  (message, synIndex) => (
                                    <div
                                      key={synIndex}
                                      className="flex items-center justify-between rounded-md border p-3"
                                    >
                                      <span>{message}</span>
                                      <Button
                                        variant="ghost"
                                        size="sm"
                                        onClick={() =>
                                          removeParamMessage(
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

                                {parameters[selectedValueIndex].messages
                                  .length === 0 && (
                                  <div className="rounded-md border border-dashed p-3 text-center text-sm text-muted-foreground">
                                    No Default replies added yet
                                  </div>
                                )}
                              </div>
                            </div>
                          ) : (
                            <div className="rounded-md border border-dashed p-3 text-center text-sm text-muted-foreground">
                              Select a parameter to add Default replies
                            </div>
                          )}
                        </div>
                      </div>
                    </CardContent>
                    <CardFooter>
                      <div className="text-sm text-muted-foreground">
                        Paramter help your bot to collect data from user require to perfom action.
                      </div>
                    </CardFooter>
                  </Card>
                  </TabsContent>
                </Tabs>

                <div className="flex justify-end gap-2">
                  <Button
                    variant="outline"
                    type="button"
                    onClick={() => router.push("/dashboard/intents")}
                  >
                    Cancel
                  </Button>
                  <Button type="submit">
                    <Save className="mr-2 h-4 w-4" />
                    Save Intent
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

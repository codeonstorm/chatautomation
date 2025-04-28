"use client";

// import { useState } from "react"
// import { Button } from "@/components/ui/button"
// import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label";
// import { Textarea } from "@/components/ui/textarea"
// import { Copy } from "lucide-react"
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../ui/select";

// export function EmbedCode() {
//   const [chatbotId, setChatbotId] = useState("your-chatbot-id")
//   const embedCode = `<script src="https://your-chatbot-service.com/embed.js" data-chatbot-id="${chatbotId}"></script>`

//   const copyToClipboard = () => {
//     navigator.clipboard
//       .writeText(embedCode)
//       .then(() => {
//         alert("Embed code copied to clipboard!")
//       })
//       .catch((err) => {
//         console.error("Failed to copy: ", err)
//       })
//   }

//   return (
//     <div className="space-y-4">
//       <h2 className="text-2xl font-bold">Embed Your Chatbot</h2>
//       <div className="space-y-2">
//         <Label htmlFor="chatbot-id">Chatbot ID</Label>
//         <Select value={chatbotId} onValueChange={setChatbotId}>
//           <SelectTrigger className="w-full">
//         <SelectValue placeholder="Select a chatbot" />
//           </SelectTrigger>
//           <SelectContent>
//         <SelectItem value="chatbot-1">Chatbot 1</SelectItem>
//         <SelectItem value="chatbot-2">Chatbot 2</SelectItem>
//         <SelectItem value="chatbot-3">Chatbot 3</SelectItem>
//           </SelectContent>
//         </Select>
//       </div>
//       <div className="space-y-2">
//         <Label htmlFor="embed-code">Embed Code</Label>
//         <Textarea id="embed-code" value={embedCode} readOnly rows={3} />
//       </div>
//       <Button onClick={copyToClipboard}>
//         <Copy className="mr-2 h-4 w-4" /> Copy Embed Code
//       </Button>
//     </div>
//   )
// }

import { AppSidebar } from "../../components/app-sidebar";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Separator } from "@/components/ui/separator";
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { CodeBlock } from "@/components/code-block";
import { useState } from "react";

export function EmbedCode() {
  // Single JavaScript example
  const jsExample = {
    title: "Chatbot Embed Code",
    description: "How to embed your chatbot on a webpage",
    code: `// Fetch data from an API
async function fetchData(url) {
  try {
    const response = await fetch(url);
    
    if (!response.ok) {
      throw new Error(\`HTTP error! Status: \${response.status}\`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Fetch error:', error);
    throw error;
  }
}

// Usage
fetchData('https://api.example.com/data')
  .then(data => {
    console.log('Data received:', data);
  })
  .catch(error => {
    console.error('Failed to fetch data:', error);
  });`,
  };

  const [chatbotId, setChatbotId] = useState("your-chatbot-id");

  return (
    <div className="flex flex-1 flex-col gap-4 pt-0">
      <div className="pt-4 mb-2">
        <h1 className="text-2xl font-bold tracking-tight">
          {jsExample.title}
        </h1>
        <p>{jsExample.description}</p>
      </div>
      
      {/* <Card>
        <CardHeader>
          <CardTitle>{jsExample.title}</CardTitle>
          <CardDescription>{jsExample.description}</CardDescription>
        </CardHeader>
        <CardContent> */}
        <div className="space-y-2">
        <Label htmlFor="chatbot-id">Chatbot ID</Label>
        <Select value={chatbotId} onValueChange={setChatbotId}>
          <SelectTrigger className="w-full">
            <SelectValue placeholder="Select a chatbot" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="chatbot-1">Chatbot 1</SelectItem>
            <SelectItem value="chatbot-2">Chatbot 2</SelectItem>
            <SelectItem value="chatbot-3">Chatbot 3</SelectItem>
          </SelectContent>
        </Select>
      </div>
          <CodeBlock code={jsExample.code} language="javascript" />
        {/* </CardContent>
      </Card> */}
    </div>
  );
}

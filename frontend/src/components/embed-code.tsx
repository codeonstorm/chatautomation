"use client"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { Textarea } from "@/components/ui/textarea"
import { Copy } from "lucide-react"

export function EmbedCode() {
  const [chatbotId, setChatbotId] = useState("your-chatbot-id")
  const embedCode = `<script src="https://your-chatbot-service.com/embed.js" data-chatbot-id="${chatbotId}"></script>`

  const copyToClipboard = () => {
    navigator.clipboard
      .writeText(embedCode)
      .then(() => {
        alert("Embed code copied to clipboard!")
      })
      .catch((err) => {
        console.error("Failed to copy: ", err)
      })
  }

  return (
    <div className="space-y-4">
      <h2 className="text-2xl font-bold">Embed Your Chatbot</h2>
      <div className="space-y-2">
        <Label htmlFor="chatbot-id">Chatbot ID</Label>
        <Input
          id="chatbot-id"
          value={chatbotId}
          onChange={(e) => setChatbotId(e.target.value)}
          placeholder="Enter your chatbot ID"
        />
      </div>
      <div className="space-y-2">
        <Label htmlFor="embed-code">Embed Code</Label>
        <Textarea id="embed-code" value={embedCode} readOnly rows={3} />
      </div>
      <Button onClick={copyToClipboard}>
        <Copy className="mr-2 h-4 w-4" /> Copy Embed Code
      </Button>
    </div>
  )
}


"use client";

import { useState } from "react";
import { Check, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";

interface CodeBlockProps {
  code: string;
  language: string;
  showLineNumbers?: boolean;
  className?: string;
}

export function CodeBlock({
  code,
  language,
  showLineNumbers = true,
  className,
}: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const copyToClipboard = async () => {
    await navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // Escape special characters in code to prevent HTML injection
  const escapeHtml = (str: string) => {
    return str.replace(/[&<>"']/g, (char) => {
      const escapeMap: { [key: string]: string } = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#039;",
      };
      return escapeMap[char] || char;
    });
  };

  // Simple syntax highlighting for JavaScript
  const highlightCode = (code: string) => {
    return code;
    return escapeHtml(code)
      .replace(
        /(\/\/.*|\/\*[\s\S]*?\*\/)/g,
        '<span class="text-slate-500">$1</span>'
      ) // Comments
      .replace(
        /\b(const|let|var|function|return|if|else|for|while|class|import|export|from|async|await|try|catch|new)\b/g,
        '<span class="text-purple-500">$1</span>' // Keywords
      )
      .replace(
        /\b(true|false|null|undefined|NaN|Infinity)\b/g,
        '<span class="text-amber-500">$1</span>'
      ) // Constants
      .replace(
        /"([^"]*)"|'([^']*)'|`([^`]*)`/g,
        '<span class="text-green-500">$&</span>'
      ) // Strings
      .replace(/\b(\d+)\b/g, '<span class="text-blue-500">$1</span>'); // Numbers
  };

  const highlightedCode = highlightCode(code);
  const lines = code.split("\n");

  return (
    <div
      className={`relative rounded-md bg-slate-950 text-slate-50 ${className}`}
    >
      <div className="flex items-center justify-between px-4 py-2 border-b border-slate-800">
        <div className="text-xs font-medium text-slate-400 uppercase">
          {language}
        </div>
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8 text-slate-400 hover:text-slate-50 hover:bg-slate-800"
          onClick={copyToClipboard}
        >
          {copied ? (
            <Check className="h-4 w-4" />
          ) : (
            <Copy className="h-4 w-4" />
          )}
          <span className="sr-only">Copy code</span>
        </Button>
      </div>
      <div className="relative overflow-x-auto">
        <pre className="p-4 overflow-x-auto text-sm">
          {showLineNumbers ? (
            <div className="flex">
              <div className="select-none pr-4 text-right text-slate-600 border-r border-slate-800 mr-4">
                {lines.map((_, i) => (
                  <div key={i}>{i + 1}</div>
                ))}
              </div>
              <code
                dangerouslySetInnerHTML={{ __html: highlightedCode }}
                className="flex-1"
              />
            </div>
          ) : (
            <code dangerouslySetInnerHTML={{ __html: highlightedCode }} />
          )}
        </pre>
      </div>
    </div>
  );
}

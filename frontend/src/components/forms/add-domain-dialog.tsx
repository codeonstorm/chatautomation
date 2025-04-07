'use client'

import { Button } from "@/components/ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog"
import { Input } from "@/components/ui/input"
import { Label } from "@/components/ui/label"
import { PlusCircle } from "lucide-react"

import { useState } from "react"
import { addDomain } from "@/services/domain"
import { useAppDispatch } from "@/redux/store/hooks"
import { add } from "@/redux/store/features/domain/domain"
import { Domain } from "@/types/domain"
 
export function AddDomainDialog() {
  const [domainName, setDomainName] = useState("")
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [open, setOpen] = useState(false)
  const dispatch = useAppDispatch()

  const handleDomainChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setDomainName(e.target.value)
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()

    if (!domainName) {
      setError("Domain name is required.")
      return
    }

    setLoading(true)
    setError(null)
    
    try {
      const domain: Domain = await addDomain(domainName)
      dispatch(add(domain))

      setOpen(false)
    } catch (err) {
      setError("Failed to add domain. Please try again.")
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog>  
      <DialogTrigger asChild>
        <Button variant="ghost" className="w-full justify-between">
          Add Domain
          <PlusCircle className="h-4 w-4 mr-2" />
        </Button>
      </DialogTrigger>
      <DialogContent className="sm:max-w-[425px]">
      <form onSubmit={handleSubmit} className="grid gap-4 py-4">

        <DialogHeader>
          <DialogTitle>Add Domain</DialogTitle>
          <DialogDescription>Enter the domain name to add.</DialogDescription>
        </DialogHeader>
          <div className="grid gap-4 py-4">
            <div className="grid grid-cols-4 items-center gap-4">
              <Label htmlFor="domainName" className="text-right">Domain Name</Label>
              <Input
                id="domainName"
                className={`col-span-4 ${error ? "border-red-500" : ""}`}
                onChange={handleDomainChange}
                value={domainName}
                placeholder="example.com"
                aria-describedby={error ? "domain-error" : undefined}
              />
            </div>
            {error && (
              <div id="domain-error" className="text-red-500 text-sm mt-1">
                {error}
              </div>
            )}
          </div>
        <DialogFooter>
          <Button
            type="submit"
            disabled={loading}
            className="w-full"
          >
            {loading ? (
              <span>Loading...</span>
            ) : (
              "Save Domain"
            )}
          </Button>
        </DialogFooter>
        </form>

      </DialogContent>
    </Dialog>
  )
}

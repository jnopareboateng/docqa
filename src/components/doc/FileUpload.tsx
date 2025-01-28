'use client'

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Progress } from "@/components/ui/progress"
import { useToast } from "@/hooks/use-toast"
import { useDocument } from "@/lib/context/DocumentContext"

export function FileUpload() {
  const [isProcessing, setIsProcessing] = useState(false)
  const [uploadProgress, setUploadProgress] = useState(0)
  const { toast } = useToast()
  const { setCurrentDocument } = useDocument()

  async function onSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault()
    setIsProcessing(true)
    setUploadProgress(0)

    try {
      const formData = new FormData(event.currentTarget)
      const file = formData.get('file') as File

      if (!file) {
        throw new Error('No file selected')
      }

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => Math.min(prev + 10, 90))
      }, 500)

      const response = await fetch('http://localhost:8000/upload', {
        method: 'POST',
        body: formData,
      })

      clearInterval(progressInterval)
      setUploadProgress(100)

      if (!response.ok) {
        throw new Error('Upload failed')
      }
      
      const data = await response.json()
      
      // Update document context
      setCurrentDocument({
        id: data.id,
        name: data.filename,
        url: `http://localhost:8000/documents/${data.id}`,
        type: data.type,
      })

      toast({
        title: "Success",
        description: "Document uploaded and processed successfully",
      })

      // Reset form
      event.currentTarget.reset()
    } catch (error) {
      toast({
        title: "Error",
        description: error instanceof Error ? error.message : 'Failed to upload document',
        variant: "destructive",
      })
    } finally {
      setIsProcessing(false)
      setTimeout(() => setUploadProgress(0), 1000) // Reset progress after a delay
    }
  }

  return (
    <Card className="p-4">
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="flex flex-col gap-2">
          <input 
            type="file"
            name="file"
            accept=".pdf,.doc,.docx,.txt"
            className="block w-full text-sm text-slate-500
              file:mr-4 file:py-2 file:px-4
              file:rounded-full file:border-0
              file:text-sm file:font-semibold
              file:bg-primary file:text-primary-foreground
              hover:file:bg-primary/90"
            disabled={isProcessing}
          />
          {uploadProgress > 0 && (
            <Progress value={uploadProgress} className="w-full" />
          )}
        </div>
        
        <Button 
          type="submit" 
          disabled={isProcessing}
          className="w-full"
        >
          {isProcessing ? 'Processing...' : 'Upload Document'}
        </Button>
      </form>
    </Card>
  )
}
import Image from "next/image";
import { FileUpload } from "@/components/doc/FileUpload"
import { ChatInterface } from "@/components/chat/ChatInterface"

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <header className="border-b">
        <div className="container mx-auto px-4 py-4">
          <h1 className="text-2xl font-bold">Document QA System</h1>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Document Section */}
          <div className="space-y-6">
            <div>
              <h2 className="text-xl font-semibold mb-4">Upload Document</h2>
              <FileUpload />
            </div>
            
            <div className="mt-8">
              <h2 className="text-xl font-semibold mb-4">Document Preview</h2>
              <div className="border rounded-lg p-4 bg-muted/50 min-h-[400px] flex items-center justify-center">
                <p className="text-muted-foreground">
                  Upload a document to preview its contents
                </p>
              </div>
            </div>
          </div>

          {/* Chat Section */}
          <div>
            <h2 className="text-xl font-semibold mb-4">Ask Questions</h2>
            <div className="border rounded-lg min-h-[600px] bg-card">
              <ChatInterface />
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

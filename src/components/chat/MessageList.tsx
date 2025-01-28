'use client'

import { Card } from '@/components/ui/card'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface MessageListProps {
  messages: Message[]
}

export function MessageList({ messages }: MessageListProps) {
  if (messages.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        No messages yet. Start by asking a question about your document.
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {messages.map((message, index) => (
        <Card
          key={index}
          className={`p-4 ${
            message.role === 'user'
              ? 'bg-primary text-primary-foreground ml-12'
              : 'bg-muted mr-12'
          }`}
        >
          <div className="flex items-start gap-2">
            <div className="min-w-[24px]">
              {message.role === 'user' ? '👤' : '🤖'}
            </div>
            <div className="prose prose-sm max-w-none">
              {message.content}
            </div>
          </div>
        </Card>
      ))}
    </div>
  )
}
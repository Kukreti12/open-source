'use client'

import { useState, useEffect, useRef } from 'react'
import ChatWindow from '@/components/ChatWindow'
import InputBox from '@/components/InputBox'
import Header from '@/components/Header'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: 'assistant',
      content: 'Hello! I\'m your AI assistant. How can I help you today?',
    },
  ])
  const [loading, setLoading] = useState(false)
  const [apiUrl, setApiUrl] = useState('')
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    setApiUrl('/api')
  }, [])

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async (text: string) => {
    if (!text.trim()) return

    // Add user message
    const userMessage: Message = { role: 'user', content: text }
    setMessages((prev) => [...prev, userMessage])
    setLoading(true)

    try {
      const response = await fetch(`${apiUrl}/ask`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text }),
      })

      if (response.ok) {
        const data = await response.json()
        const assistantMessage: Message = {
          role: 'assistant',
          content: data.answer || 'Sorry, I couldn\'t generate a response.',
        }
        setMessages((prev) => [...prev, assistantMessage])
      } else {
        const assistantMessage: Message = {
          role: 'assistant',
          content: `Error: ${response.status} - Failed to get response from server.`,
        }
        setMessages((prev) => [...prev, assistantMessage])
      }
    } catch (error) {
      const errorMessage: Message = {
        role: 'assistant',
        content: `❌ Error: Cannot connect to API at ${apiUrl}. Is the FastAPI server running?`,
      }
      setMessages((prev) => [...prev, errorMessage])
    } finally {
      setLoading(false)
    }
  }

  const handleClearChat = () => {
    setMessages([
      {
        role: 'assistant',
        content: 'Hello! I\'m your AI assistant. How can I help you today?',
      },
    ])
  }

  return (
    <main className="flex flex-col h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <Header onClear={handleClearChat} />
      <div className="flex-1 overflow-hidden">
        <ChatWindow messages={messages} loading={loading} messagesEndRef={messagesEndRef} />
      </div>
      <InputBox onSend={sendMessage} disabled={loading} />
    </main>
  )
}

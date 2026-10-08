'use client'

interface HeaderProps {
  onClear: () => void
}

export default function Header({ onClear }: HeaderProps) {
  return (
    <header className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-lg">
      <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold flex items-center gap-2">
            🤖 AI Chatbot
          </h1>
          <p className="text-blue-100 text-sm">Powered by Ollama & FastAPI</p>
        </div>
        <button
          onClick={onClear}
          className="px-4 py-2 bg-white text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transition-colors duration-200"
        >
          Clear Chat
        </button>
      </div>
    </header>
  )
}

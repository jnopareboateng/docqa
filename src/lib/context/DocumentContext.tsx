'use client'

import { createContext, useContext, useState, ReactNode } from 'react'

interface DocumentState {
  currentDocument: {
    id: string
    name: string
    url: string
    type: string
  } | null
  setCurrentDocument: (doc: DocumentState['currentDocument']) => void
  clearDocument: () => void
}

const DocumentContext = createContext<DocumentState | undefined>(undefined)

export function DocumentProvider({ children }: { children: ReactNode }) {
  const [currentDocument, setCurrentDocument] = useState<DocumentState['currentDocument']>(null)

  const clearDocument = () => setCurrentDocument(null)

  return (
    <DocumentContext.Provider
      value={{
        currentDocument,
        setCurrentDocument,
        clearDocument,
      }}
    >
      {children}
    </DocumentContext.Provider>
  )
}

export function useDocument() {
  const context = useContext(DocumentContext)
  if (context === undefined) {
    throw new Error('useDocument must be used within a DocumentProvider')
  }
  return context
}

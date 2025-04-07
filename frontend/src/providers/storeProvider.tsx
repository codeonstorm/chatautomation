
'use client';

import { AppStore, makeStore } from "@/redux/store/store";
import React from "react";
import { useRef } from 'react'
import { Provider } from 'react-redux'
// import { incrementByAmount } from '@/redux/store/features/domain/domain'

// import { makeStore, AppStore } from "@/lib/redux/store/store"

export default function StoreProvider({
  // count,
  children,
}: {
  // count: number
  children: React.ReactNode
}) {
  const storeRef = useRef<AppStore>(undefined)
  if (!storeRef.current) {
    // Create the store instance the first time this renders
    storeRef.current = makeStore()
    // Initialize the store with the initial count value
    // storeRef.current.dispatch(incrementByAmount(count))

  }

  return <Provider store={storeRef.current}>{children}</Provider>
}
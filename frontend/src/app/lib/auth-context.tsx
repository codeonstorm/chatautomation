"use client"

import type React from "react"

import { createContext, useContext, useEffect, useState } from "react"
import { useRouter } from "next/navigation"
import type { User } from "@/types/user"
import { login, refreshToken, getCurrentUser } from "@/app/lib/auth-service"

interface AuthContextType {
  user: User | null
  isLoading: boolean
  isAuthenticated: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => void
  refreshAuth: () => Promise<boolean>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  const isAuthenticated = !!user

  useEffect(() => {
    const checkAuth = async () => {
      try {
        // Check if we have tokens in localStorage
        const accessToken = localStorage.getItem("accessToken")
        const refreshTokenValue = localStorage.getItem("refreshToken")

        if (!accessToken || !refreshTokenValue) {
          setIsLoading(false)
          return
        }

        // Try to get current user with the access token
        try {
          const userData = await getCurrentUser()
          setUser(userData)
        } catch (error) {
          // If access token is expired, try to refresh
          if (refreshTokenValue) {
            const success = await refreshAuth()
            if (!success) {
              logout()
            }
          } else {
            logout()
          }
        }
      } catch (error) {
        console.error("Auth initialization error:", error)
      } finally {
        setIsLoading(false)
      }
    }

    checkAuth()
  }, [])

  const loginUser = async (email: string, password: string) => {
    setIsLoading(true)
    try {
      const { access_token, refresh_token } = await login(email, password)

      localStorage.setItem("accessToken", access_token)
      localStorage.setItem("refreshToken", refresh_token)

      const userData = await getCurrentUser()
      setUser(userData)

      router.push("/dashboard")
    } catch (error) {
      console.error("Login error:", error)
      throw error
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    localStorage.removeItem("accessToken")
    localStorage.removeItem("refreshToken")
    setUser(null)
    router.push("/login")
  }

  const refreshAuth = async (): Promise<boolean> => {
    try {
      const refreshTokenValue = localStorage.getItem("refreshToken")
      if (!refreshTokenValue) return false

      const { access_token, refresh_token } = await refreshToken(refreshTokenValue)

      localStorage.setItem("accessToken", access_token)
      localStorage.setItem("refreshToken", refresh_token)

      const userData = await getCurrentUser()
      setUser(userData)

      return true
    } catch (error) {
      console.error("Token refresh error:", error)
      return false
    }
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated,
        login: loginUser,
        logout,
        refreshAuth,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider")
  }
  return context
}


import { NextResponse } from "next/server"
import type { NextRequest } from "next/server"

export function middleware(request: NextRequest) {
  const accessToken = request.cookies.get("accessToken")?.value
  const isAuthPage = request.nextUrl.pathname === "/login" || request.nextUrl.pathname === "/register"

  // If trying to access auth page while logged in, redirect to dashboard
  if (isAuthPage && accessToken) {
    return NextResponse.redirect(new URL("/dashboard", request.url))
  }

  // If trying to access protected page without being logged in, redirect to login
  if (!isAuthPage && !accessToken && request.nextUrl.pathname.startsWith("/dashboard")) {
    return NextResponse.redirect(new URL("/login", request.url))
  }

  return NextResponse.next()
}

export const config = {
  matcher: ["/dashboard/:path*", "/login", "/register"],
}


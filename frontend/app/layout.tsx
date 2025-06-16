import type React from "react"
import type { Metadata } from "next"
import { Inter } from "next/font/google"
import { Press_Start_2P } from "next/font/google"
import "./globals.css"
import Header from "@/components/header"
import { AuthProvider } from "@/lib/auth"
import Navbar from "@/components/Navbar"
import { ThemeProvider } from "@/components/theme-provider"

const inter = Inter({ subsets: ["latin"] })

const pressStart2P = Press_Start_2P({
  weight: '400',
  subsets: ['latin'],
  variable: '--font-press-start-2p',
  display: 'swap',
})

export const metadata: Metadata = {
  title: "Retro Gallery",
  description: "A retro-style photo gallery",
    generator: 'v0.dev'
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="en" className={`${inter.className} ${pressStart2P.variable}`}>
      <body className="bg-gray-50 dark:bg-black text-gray-900 dark:text-gray-100">
        <ThemeProvider
          attribute="class"
          defaultTheme="system"
          enableSystem
          disableTransitionOnChange
        >
          <AuthProvider>
            <Navbar />
            <main className="container mx-auto px-4 py-6">{children}</main>
          </AuthProvider>
        </ThemeProvider>
      </body>
    </html>
  )
}

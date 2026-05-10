import type { Metadata } from 'next'
import { Inter } from 'next/font/google'
import './globals.css'

const inter = Inter({ subsets: ['latin', 'arabic'] })

export const metadata: Metadata = {
  title: 'Ragaban Clinics — Patient Portal',
  description: 'Book appointments, view records, make payments. Jeddah\'s premier medical group.',
}

export default function RootLayout({
  children,
  params: { locale }
}: {
  children: React.ReactNode
  params: { locale: string }
}) {
  const dir = locale === 'ar' ? 'rtl' : 'ltr'
  
  return (
    <html lang={locale} dir={dir}>
      <body className={inter.className}>{children}</body>
    </html>
  )
}

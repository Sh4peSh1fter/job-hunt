import type { Metadata } from "next";
import Link from "next/link"; // Import Link for navigation
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Job Hunt - Your Personal Job Search Assistant",
  description: "A local web application to help manage and optimize your job search.",
};

// Simple Header component for now
function AppHeader() {
  return (
    <header className="px-4 lg:px-6 h-14 flex items-center">
      <Link href="/" className="flex items-center justify-center" prefetch={false}>
        <span className="font-semibold">Job Hunt</span>
      </Link>
      <nav className="ml-auto flex gap-4 sm:gap-6">
        <Link
          href="/dashboard"
          className="text-sm font-medium hover:underline underline-offset-4"
          prefetch={false}
        >
          Dashboard
        </Link>
        <Link
          href="/components"
          className="text-sm font-medium hover:underline underline-offset-4"
          prefetch={false}
        >
          Components
        </Link>
        <Link
          href="/tools"
          className="text-sm font-medium hover:underline underline-offset-4"
          prefetch={false}
        >
          Tools
        </Link>
        <Link
          href="/"
          className="text-sm font-medium hover:underline underline-offset-4"
          prefetch={false}
        >
          Guide
        </Link>
      </nav>
    </header>
  );
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased flex flex-col min-h-screen`}
      >
        <AppHeader />
        <main className="flex-grow container mx-auto px-6 py-8">
        {children}
        </main>
        {/* Optional Footer can be added here later */}
        {/* <footer className="bg-gray-100 text-center p-4 mt-auto">
          <p className="text-sm text-gray-600">&copy; {new Date().getFullYear()} Job Hunt. All rights reserved.</p>
        </footer> */}
      </body>
    </html>
  );
}

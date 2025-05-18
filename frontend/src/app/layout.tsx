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
    <header className="bg-gray-100 shadow-md">
      <nav className="container mx-auto px-6 py-3 flex justify-between items-center">
        <Link href="/" className="text-xl font-semibold text-gray-700 hover:text-gray-900">
          Job Hunt
        </Link>
        <div className="space-x-4">
          <Link href="/" className="text-gray-700 hover:text-gray-900">
            Guide
          </Link>
          <Link href="/tools" className="text-gray-700 hover:text-gray-900">
            Tools
          </Link>
        </div>
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

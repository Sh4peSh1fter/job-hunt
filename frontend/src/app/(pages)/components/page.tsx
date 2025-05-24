import Link from 'next/link';
import { Card, CardHeader, CardTitle, CardDescription } from "@/components/ui/card";

const componentLinks = [
  { href: "/components/companies", title: "Companies", description: "Manage company information." },
  { href: "/components/job-applications", title: "Job Applications", description: "Track your job applications." },
  { href: "/components/application-events", title: "Application Events", description: "Log events for each application." },
  { href: "/components/job-sources", title: "Job Sources", description: "Keep a list of your job sources." },
];

export default function ComponentsPage() {
  return (
    <div className="container mx-auto py-10">
      <h1 className="text-3xl font-bold mb-8">Data Components</h1>
      <p className="mb-8 text-muted-foreground">
        Select a data component below to view and manage its records.
      </p>
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {componentLinks.map((link) => (
          <Link href={link.href} key={link.title} passHref className="no-underline">
            <Card className="hover:shadow-lg transition-shadow duration-200 cursor-pointer h-full flex flex-col">
              <CardHeader className="flex-grow">
                <CardTitle>{link.title}</CardTitle>
                <CardDescription>{link.description}</CardDescription>
              </CardHeader>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
} 
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import Link from "next/link";

interface ToolInfo {
  slug: string;
  title: string;
  description: string;
}

// Placeholder data for tools - we will expand this later
const availableTools: ToolInfo[] = [
  {
    slug: "keyword-analyzer",
    title: "Keyword Frequency Analyzer",
    description: "Extract and count key terms from job descriptions to tailor your resume.",
  },
  {
    slug: "company-research",
    title: "Company Research Assistant",
    description: "Gather information about potential employers (Details TBD).",
  },
  {
    slug: "resume-tailor",
    title: "Resume Tailoring Utility (Planned)",
    description: "Match your resume content to specific job descriptions.",
  },
];

export default function ToolsOverviewPage() {
  return (
    <div>
      <h1 className="text-3xl font-bold tracking-tight text-gray-900 dark:text-gray-100 sm:text-4xl mb-8">
        Available Tools
      </h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {availableTools.map((tool) => (
          <Link href={`/tools/${tool.slug}`} key={tool.slug} legacyBehavior passHref>
            <Card className="h-full flex flex-col hover:shadow-lg transition-shadow duration-200 cursor-pointer">
              <CardHeader>
                <CardTitle>{tool.title}</CardTitle>
                {tool.slug.includes("planned") || tool.slug.includes("research") ? (
                  <span className="text-xs bg-yellow-200 text-yellow-800 px-2 py-0.5 rounded-full inline-block mt-1">
                    {tool.slug.includes("planned") ? "Planned" : "Alpha"}
                  </span>
                ) : null}
              </CardHeader>
              <CardContent className="flex-grow">
                <CardDescription>{tool.description}</CardDescription>
              </CardContent>
            </Card>
          </Link>
        ))}
      </div>
    </div>
  );
} 
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

export default function JobSourcesDataPage() {
  return (
    <div className="container mx-auto py-10">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Job Sources</h1>
        <Button>Add New Job Source</Button>
      </div>
      <Card>
        <CardHeader>
          <CardTitle>Job Source Records</CardTitle>
          <CardDescription>A table displaying all job source records will appear here.</CardDescription>
        </CardHeader>
        <CardContent>
          {/* Placeholder for table */}
          <p className="text-muted-foreground">Job source data table is loading...</p>
        </CardContent>
      </Card>
    </div>
  );
} 
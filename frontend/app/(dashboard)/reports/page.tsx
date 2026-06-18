"use client";

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { FileText, Download, Calendar } from "lucide-react";

export default function ReportsPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Reports & History</h1>
        <p className="text-muted-foreground">
          View and download validation reports and processing history
        </p>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        <Card className="hover:shadow-lg transition-shadow cursor-pointer">
          <CardHeader>
            <FileText className="h-8 w-8 text-blue-500 mb-2" />
            <CardTitle>Validation Report</CardTitle>
            <CardDescription>Customer data validation - 2024-01-15</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-2 text-sm mb-4">
              <div className="flex justify-between">
                <span className="text-muted-foreground">Total Records:</span>
                <span className="font-medium">10,000</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Valid:</span>
                <span className="font-medium text-green-600">9,240</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Invalid:</span>
                <span className="font-medium text-red-600">760</span>
              </div>
              <div className="flex justify-between">
                <span className="text-muted-foreground">Success Rate:</span>
                <span className="font-medium">92.4%</span>
              </div>
            </div>
            <Button variant="outline" size="sm" className="w-full">
              <Download className="h-4 w-4 mr-2" />
              Download PDF
            </Button>
          </CardContent>
        </Card>

        {/* Add more report cards as needed */}
      </div>
    </div>
  );
}
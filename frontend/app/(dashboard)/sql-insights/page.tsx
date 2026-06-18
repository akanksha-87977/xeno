"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { analyticsAPI } from "@/lib/api";
import { Download, Code } from "lucide-react";

export default function SqlInsightsPage() {
  const [insights, setInsights] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedInsight, setSelectedInsight] = useState<any>(null);

  useEffect(() => {
    loadInsights();
  }, []);

  const loadInsights = async () => {
    try {
      const data = await analyticsAPI.getSqlInsights();
      setInsights(data);
      if (data.length > 0) {
        setSelectedInsight(data[0]);
      }
    } catch (error) {
      console.error("Failed to load insights:", error);
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = (insight: any) => {
    const csv = convertToCSV(insight.result);
    const blob = new Blob([csv], { type: "text/csv" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${insight.title.replace(/\s+/g, "_")}.csv`;
    a.click();
  };

  const convertToCSV = (data: any[]) => {
    if (!data || data.length === 0) return "";
    
    const headers = Object.keys(data[0]);
    const rows = data.map((row) =>
      headers.map((header) => JSON.stringify(row[header] || "")).join(",")
    );
    
    return [headers.join(","), ...rows].join("\n");
  };

  if (loading) {
    return <div className="text-center py-12">Loading SQL insights...</div>;
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">SQL Analytics & Insights</h1>
        <p className="text-muted-foreground">
          Pre-built SQL queries for customer data analysis
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar with insight list */}
        <div className="lg:col-span-1 space-y-2">
          <h3 className="font-semibold mb-3">Available Queries</h3>
          {insights.map((insight, idx) => (
            <Button
              key={idx}
              variant={selectedInsight?.title === insight.title ? "default" : "outline"}
              className="w-full justify-start"
              onClick={() => setSelectedInsight(insight)}
            >
              {insight.title}
            </Button>
          ))}
        </div>

        {/* Main content area */}
        <div className="lg:col-span-3 space-y-6">
          {selectedInsight && (
            <>
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center justify-between">
                    {selectedInsight.title}
                    <Button size="sm" onClick={() => downloadCSV(selectedInsight)}>
                      <Download className="h-4 w-4 mr-2" />
                      Export CSV
                    </Button>
                  </CardTitle>
                  <CardDescription>
                    Results: {selectedInsight.count} record(s)
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {/* SQL Query */}
                  <div>
                    <div className="flex items-center gap-2 mb-2">
                      <Code className="h-4 w-4" />
                      <span className="font-semibold text-sm">SQL Query:</span>
                    </div>
                    <pre className="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto text-sm">
                      {selectedInsight.query}
                    </pre>
                  </div>

                  {/* Results Table */}
                  <div>
                    <h4 className="font-semibold mb-2">Results:</h4>
                    {selectedInsight.result.length > 0 ? (
                      <div className="border rounded-lg overflow-x-auto">
                        <table className="w-full text-sm">
                          <thead className="bg-gray-100">
                            <tr>
                              {Object.keys(selectedInsight.result[0]).map((key) => (
                                <th key={key} className="px-4 py-2 text-left font-medium">
                                  {key}
                                </th>
                              ))}
                            </tr>
                          </thead>
                          <tbody>
                            {selectedInsight.result.slice(0, 50).map((row: any, idx: number) => (
                              <tr key={idx} className="border-t hover:bg-gray-50">
                                {Object.values(row).map((value: any, i: number) => (
                                  <td key={i} className="px-4 py-2">
                                    {String(value)}
                                  </td>
                                ))}
                              </tr>
                            ))}
                          </tbody>
                        </table>
                      </div>
                    ) : (
                      <p className="text-muted-foreground text-center py-8">No results found</p>
                    )}
                    {selectedInsight.result.length > 50 && (
                      <p className="text-sm text-muted-foreground mt-2">
                        Showing first 50 of {selectedInsight.result.length} results
                      </p>
                    )}
                  </div>
                </CardContent>
              </Card>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
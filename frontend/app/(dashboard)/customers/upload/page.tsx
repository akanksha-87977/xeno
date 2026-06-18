"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { FileUploader } from "@/components/upload/FileUploader";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { uploadAPI, customerAPI } from "@/lib/api";
import { CheckCircle, AlertCircle, Loader2 } from "lucide-react";

export default function CustomerUploadPage() {
  const router = useRouter();
  const [uploadedFile, setUploadedFile] = useState<any>(null);
  const [validating, setValidating] = useState(false);
  const [validationResult, setValidationResult] = useState<any>(null);

  const handleUpload = async (file: File) => {
    try {
      const result = await uploadAPI.uploadFile(file, "customer");
      setUploadedFile(result);
      return result;
    } catch (error: any) {
      throw new Error(error.response?.data?.detail || "Upload failed");
    }
  };

  const handleValidate = async () => {
    if (!uploadedFile) return;

    setValidating(true);
    try {
      const result = await customerAPI.validate(uploadedFile.file_id);
      setValidationResult(result);
    } catch (error: any) {
      alert(error.response?.data?.detail || "Validation failed");
    } finally {
      setValidating(false);
    }
  };

  const handleClean = async () => {
    if (!uploadedFile) return;

    try {
      const result = await customerAPI.clean(uploadedFile.file_id);
      alert("Data cleaned successfully!");
    } catch (error: any) {
      alert(error.response?.data?.detail || "Cleaning failed");
    }
  };

  const handleImport = async () => {
    if (!uploadedFile) return;

    try {
      const result = await customerAPI.import(uploadedFile.file_id);
      alert(`Successfully imported ${result.imported_count} customers!`);
      router.push("/customers/analytics");
    } catch (error: any) {
      alert(error.response?.data?.detail || "Import failed");
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <div>
        <h1 className="text-3xl font-bold mb-2">Upload Customer Data</h1>
        <p className="text-muted-foreground">
          Upload a CSV or Excel file containing customer information for validation and processing
        </p>
      </div>

      {/* Upload Section */}
      <Card>
        <CardHeader>
          <CardTitle>Step 1: Upload File</CardTitle>
          <CardDescription>
            Upload your customer data file (CSV, XLSX, or XLS)
          </CardDescription>
        </CardHeader>
        <CardContent>
          <FileUploader onUpload={handleUpload} fileType="customer" />
        </CardContent>
      </Card>

      {/* Preview Section */}
      {uploadedFile && (
        <Card>
          <CardHeader>
            <CardTitle>Step 2: Preview & Validate</CardTitle>
            <CardDescription>
              Review your uploaded data and run validation
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4">
              <div className="flex items-center gap-2 mb-3">
                <CheckCircle className="h-5 w-5 text-blue-600" />
                <span className="font-semibold">File Uploaded Successfully</span>
              </div>
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-muted-foreground">Filename:</span>{" "}
                  <span className="font-medium">{uploadedFile.filename}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Rows:</span>{" "}
                  <span className="font-medium">{uploadedFile.row_count}</span>
                </div>
                <div>
                  <span className="text-muted-foreground">Columns:</span>{" "}
                  <span className="font-medium">
                    {uploadedFile.preview?.column_count}
                  </span>
                </div>
              </div>
            </div>

            {/* Preview Table */}
            <div className="border rounded-lg overflow-hidden">
              <table className="w-full text-sm">
                <thead className="bg-gray-100">
                  <tr>
                    {uploadedFile.preview?.columns.map((col: string) => (
                      <th key={col} className="px-4 py-2 text-left font-medium">
                        {col}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {uploadedFile.preview?.preview.map((row: any, idx: number) => (
                    <tr key={idx} className="border-t">
                      {uploadedFile.preview?.columns.map((col: string) => (
                        <td key={col} className="px-4 py-2">
                          {row[col]}
                        </td>
                      ))}
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            <Button onClick={handleValidate} disabled={validating} className="w-full">
              {validating ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Validating...
                </>
              ) : (
                "Validate Data"
              )}
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Validation Results */}
      {validationResult && (
        <Card>
          <CardHeader>
            <CardTitle>Step 3: Validation Results</CardTitle>
            <CardDescription>Review validation findings and take action</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Summary */}
            <div className="grid grid-cols-4 gap-4">
              <div className="text-center p-4 bg-blue-50 rounded-lg">
                <div className="text-2xl font-bold text-blue-600">
                  {validationResult.summary.total_records}
                </div>
                <div className="text-sm text-muted-foreground">Total Records</div>
              </div>
              <div className="text-center p-4 bg-green-50 rounded-lg">
                <div className="text-2xl font-bold text-green-600">
                  {validationResult.summary.valid_records}
                </div>
                <div className="text-sm text-muted-foreground">Valid</div>
              </div>
              <div className="text-center p-4 bg-red-50 rounded-lg">
                <div className="text-2xl font-bold text-red-600">
                  {validationResult.summary.invalid_records}
                </div>
                <div className="text-sm text-muted-foreground">Invalid</div>
              </div>
              <div className="text-center p-4 bg-purple-50 rounded-lg">
                <div className="text-2xl font-bold text-purple-600">
                  {validationResult.summary.success_rate}%
                </div>
                <div className="text-sm text-muted-foreground">Success Rate</div>
              </div>
            </div>

            {/* AI Insights */}
            {validationResult.ai_insights && (
              <div className="bg-gradient-to-r from-purple-50 to-blue-50 border border-purple-200 rounded-lg p-6">
                <h4 className="font-semibold mb-3 flex items-center gap-2">
                  <span className="text-2xl">🤖</span> AI Insights
                </h4>
                <pre className="whitespace-pre-wrap text-sm font-mono bg-white p-4 rounded">
                  {validationResult.ai_insights}
                </pre>
              </div>
            )}

            {/* Errors Preview */}
            {validationResult.errors && validationResult.errors.length > 0 && (
              <div>
                <h4 className="font-semibold mb-3">
                  First {Math.min(10, validationResult.errors.length)} Errors:
                </h4>
                <div className="border rounded-lg overflow-hidden">
                  <table className="w-full text-sm">
                    <thead className="bg-gray-100">
                      <tr>
                        <th className="px-4 py-2 text-left">Row</th>
                        <th className="px-4 py-2 text-left">Column</th>
                        <th className="px-4 py-2 text-left">Error Type</th>
                        <th className="px-4 py-2 text-left">Description</th>
                      </tr>
                    </thead>
                    <tbody>
                      {validationResult.errors.slice(0, 10).map((error: any, idx: number) => (
                        <tr key={idx} className="border-t">
                          <td className="px-4 py-2">{error.row_number}</td>
                          <td className="px-4 py-2">{error.column_name}</td>
                          <td className="px-4 py-2">
                            <span className="px-2 py-1 bg-red-100 text-red-800 rounded text-xs">
                              {error.error_type}
                            </span>
                          </td>
                          <td className="px-4 py-2">{error.error_description}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}

            {/* Actions */}
            <div className="flex gap-4">
              <Button onClick={handleClean} variant="outline" className="flex-1">
                Clean Data
              </Button>
              <Button onClick={handleImport} className="flex-1">
                Import to Database
              </Button>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}
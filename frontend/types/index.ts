export interface User {
  id: number;
  email: string;
  username: string;
  full_name?: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

export interface Customer {
  id: number;
  customer_id: string;
  full_name: string;
  first_name?: string;
  email: string;
  email_domain?: string;
  is_gmail: boolean;
  phone_number?: string;
  city?: string;
  signup_date?: string;
  signup_month?: string;
  signup_day?: string;
  created_at: string;
}

export interface ValidationError {
  row_number: number;
  column_name: string;
  error_type: string;
  error_description: string;
  suggested_fix?: string;
  current_value?: string;
}

export interface ValidationReport {
  report_id: string;
  file_name: string;
  file_type: string;
  total_records: number;
  valid_records: number;
  invalid_records: number;
  success_rate: number;
  errors: ValidationError[];
  created_at: string;
}

export interface UploadedFile {
  file_id: string;
  file_name: string;
  file_type: string;
  file_path: string;
  row_count: number;
  uploaded_at: string;
}

export interface AnalyticsData {
  overview: {
    total_customers: number;
    total_cities: number;
    gmail_customers: number;
    non_gmail_customers: number;
    new_customers_30_days: number;
  };
  customers_by_city: Array<{ city: string; count: number }>;
  monthly_signups: Array<{ month: string; count: number }>;
  day_distribution: Array<{ day: string; count: number }>;
  gmail_distribution: {
    gmail: number;
    non_gmail: number;
  };
}
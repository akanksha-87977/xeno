from typing import List, Dict
from collections import Counter
from ..schemas.validation import ValidationError

class AIInsightsService:
    
    @staticmethod
    def generate_insights(
        total_records: int,
        valid_records: int,
        invalid_records: int,
        errors: List[ValidationError],
        error_distribution: Dict[str, int]
    ) -> str:
        """Generate AI-powered insights from validation results"""
        
        if total_records == 0:
            return "No data to analyze."
        
        success_rate = (valid_records / total_records) * 100
        error_rate = (invalid_records / total_records) * 100
        
        insights = []
        
        # Overall assessment
        if success_rate >= 95:
            insights.append(f"✅ Excellent data quality! {success_rate:.1f}% of records are valid.")
        elif success_rate >= 80:
            insights.append(f"⚠️ Good data quality with {success_rate:.1f}% valid records, but there's room for improvement.")
        else:
            insights.append(f"❌ Poor data quality detected. Only {success_rate:.1f}% of records are valid.")
        
        # Error analysis
        if error_distribution:
            top_errors = sorted(error_distribution.items(), key=lambda x: x[1], reverse=True)[:3]
            
            insights.append(f"\n📊 Top Issues Found:")
            for error_type, count in top_errors:
                percentage = (count / len(errors)) * 100
                insights.append(f"  • {error_type.replace('_', ' ').title()}: {count} occurrences ({percentage:.1f}%)")
        
        # Column-specific issues
        column_errors = Counter([error.column_name for error in errors])
        if column_errors:
            top_columns = column_errors.most_common(3)
            insights.append(f"\n🎯 Most Problematic Columns:")
            for column, count in top_columns:
                insights.append(f"  • {column}: {count} errors")
        
        # Recommendations
        insights.append(f"\n💡 Recommendations:")
        
        if 'MISSING_VALUE' in error_distribution:
            insights.append(f"  • Fill missing values in required fields")
        
        if 'DUPLICATE' in error_distribution:
            insights.append(f"  • Remove or merge duplicate records")
        
        if 'INVALID_FORMAT' in error_distribution or 'INVALID_EMAIL' in error_distribution:
            insights.append(f"  • Standardize data formats (email, phone, date)")
        
        if 'NEGATIVE_VALUE' in error_distribution or 'NEGATIVE_PRICE' in error_distribution:
            insights.append(f"  • Review and correct negative values")
        
        if 'INVALID_DATE' in error_distribution:
            insights.append(f"  • Use consistent date format (YYYY-MM-DD)")
        
        # Summary statistics
        insights.append(f"\n📈 Summary:")
        insights.append(f"  • Total Records: {total_records:,}")
        insights.append(f"  • Valid Records: {valid_records:,} ({success_rate:.1f}%)")
        insights.append(f"  • Invalid Records: {invalid_records:,} ({error_rate:.1f}%)")
        insights.append(f"  • Total Errors: {len(errors):,}")
        
        return "\n".join(insights)
    
    @staticmethod
    def detect_anomalies(df, column: str) -> List[str]:
        """Detect anomalies in specific column"""
        anomalies = []
        
        if df[column].dtype in ['int64', 'float64']:
            # Numerical anomalies
            mean = df[column].mean()
            std = df[column].std()
            outliers = df[(df[column] < mean - 3*std) | (df[column] > mean + 3*std)]
            
            if len(outliers) > 0:
                anomalies.append(f"Found {len(outliers)} statistical outliers in {column}")
        
        return anomalies
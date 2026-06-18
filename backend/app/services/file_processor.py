import pandas as pd
import os
import uuid
from typing import List, Dict
from datetime import datetime
from ..core.config import settings
import zipfile

class FileProcessorService:
    
    @staticmethod
    def read_file(file_path: str) -> pd.DataFrame:
        """Read CSV or Excel file"""
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.csv':
            return pd.read_csv(file_path)
        elif file_ext in ['.xlsx', '.xls']:
            return pd.read_excel(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_ext}")
    
    @staticmethod
    def save_file(df: pd.DataFrame, filename: str, format: str = 'csv') -> str:
        """Save dataframe to file"""
        file_id = str(uuid.uuid4())
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == 'csv':
            file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}_{timestamp}_{filename}.csv")
            df.to_csv(file_path, index=False)
        elif format == 'excel':
            file_path = os.path.join(settings.UPLOAD_DIR, f"{file_id}_{timestamp}_{filename}.xlsx")
            df.to_excel(file_path, index=False)
        else:
            raise ValueError(f"Unsupported format: {format}")
        
        return file_path
    
    @staticmethod
    def split_large_file(df: pd.DataFrame, filename: str, chunk_size: int = None) -> List[str]:
        """Split large dataframe into multiple files"""
        if chunk_size is None:
            chunk_size = settings.MAX_ROWS_PER_FILE
        
        file_paths = []
        num_chunks = len(df) // chunk_size + (1 if len(df) % chunk_size > 0 else 0)
        
        for i in range(num_chunks):
            start_idx = i * chunk_size
            end_idx = min((i + 1) * chunk_size, len(df))
            chunk_df = df.iloc[start_idx:end_idx]
            
            chunk_filename = f"{filename}_chunk_{i+1}"
            file_path = FileProcessorService.save_file(chunk_df, chunk_filename, format='csv')
            file_paths.append(file_path)
        
        return file_paths
    
    @staticmethod
    def create_zip(file_paths: List[str], zip_name: str) -> str:
        """Create ZIP file from multiple files"""
        zip_path = os.path.join(settings.UPLOAD_DIR, f"{zip_name}.zip")
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path in file_paths:
                zipf.write(file_path, os.path.basename(file_path))
        
        return zip_path
    
    @staticmethod
    def get_file_info(file_path: str) -> Dict:
        """Get file information"""
        file_size = os.path.getsize(file_path)
        file_name = os.path.basename(file_path)
        file_ext = os.path.splitext(file_path)[1]
        
        return {
            "file_name": file_name,
            "file_size": file_size,
            "file_extension": file_ext,
            "file_path": file_path
        }
    
    @staticmethod
    def preview_data(df: pd.DataFrame, rows: int = 10) -> Dict:
        """Get preview of dataframe"""
        return {
            "columns": list(df.columns),
            "row_count": len(df),
            "column_count": len(df.columns),
            "preview": df.head(rows).to_dict(orient='records'),
            "data_types": {col: str(dtype) for col, dtype in df.dtypes.items()}
        }
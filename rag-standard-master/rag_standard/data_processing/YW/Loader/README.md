# Document Loader

A comprehensive document processing system that supports multiple file formats and provides flexible chunking options for RAG (Retrieval-Augmented Generation) applications.

## Features

- **Multi-format Support**: Handles various document formats:
  - PDF files (including Upstage API integration)
  - PowerPoint (PPT, PPTX)
  - Excel (XLSX, XLS, XLSM)
  - Word (DOCX)
  - HWP (HWP, HWPX)
  - Text files (TXT)

- **Flexible Chunking Options**:
  - Page-based chunking
  - Token-based chunking with configurable parameters
  - Customizable overlap settings

- **Metadata Generation**:
  - File information (name, extension, size)
  - Creation and modification timestamps
  - Token counts for both LLM and retrieval content
  - Chunk ordering and identification

## Project Structure

```
Loader/
├── document_load_final.py    # Main loader implementation
├── load_upstageapi_pdf.py    # PDF processing with Upstage API
├── load_ppt.py              # PowerPoint file loader
├── load_pdf.py              # PDF file loader
├── load_hwpx.py             # HWPX file loader
├── load_hwp.py              # HWP file loader
├── load_excel.py            # Excel file loader
├── load_docx.py             # Word file loader
├── load_txt.py              # Text file loader
├── Parsing/                 # Chunking utilities
│   ├── chunk_by_page.py
│   └── chunk_by_token.py
└── logs/                    # Log files directory
```

## Configuration

The system uses configuration parameters from multiple sources:

1. From `configs/main_config.yaml`:
```yaml
# --- Metadata Settings ---
data_processing_settings:
  version_name: "string"        # Version identifier
  root_path: "string"          # Root directory path
  file_path: "string"          # Input files directory path
  page_tf: "boolean"           # Enable page-based chunking
  token_tf: "boolean"          # Enable token-based chunking
  api_tf: "boolean"            # Enable Upstage API

# --- Upstage API Settings ---
upstage_api_settings:
  url: "string"                # Upstage API endpoint
  model: "string"              # Upstage model name
  api_key: "string"            # Upstage API key
  max_tokens: number           # Maximum tokens per chunk
  overlap_tokens: number       # Token overlap between chunks
  token_limit: number          # Maximum token limit
```

2. From `.env` file:
```env
# === UPSTAGE API 정보 ===
UPSTAGE_API_KEY=<YOUR_UPSTAGE_API_KEY>
```

## Usage

1. Configure the settings in the two files:
   - `configs/main_config.yaml`
   - `.env` (refer to the template)
2. Use the `LoadData` class from `document_load_final.py`:

```python
from document_load_final import LoadData
import sys
sys.path.append('/data/aisvc_data/RAG/Rag_Standard_v2')
from rag_standard.data_processing import get_config_file

config = get_config_file()

pname = config['data_processing_settings']['version_name']
root_path = config['data_processing_settings']['root_path']
file_path = config['data_processing_settings']['file_path']
page_tf = config['data_processing_settings']['page_tf']
token_tf = config['data_processing_settings']['token_tf']
api_tf = config['data_processing_settings']['api_tf']

loader = LoadData()
loader.load_all(
  pname,
  root_path,
  file_path,
  page=page_tf,
  token=token_tf,
  api=api_tf
)
```

## Output Structure

The system generates three types of outputs:

1. **Interim Results**: Intermediate results from documents stored in `{root_path}/{pname}/Interim/`
2. **Split Results**: Processed chunks with metadata in JSON format stored in `{root_path}/{pname}/Split/`
3. **Document Loader Results**: Loader-processed metadata stored in `{root_path}/{pname}/Loader/`

The output structure is organized as follows:
```
version_name/
├── Interim/           # Intermediate results
├── Split/
│   ├── API_PAGE/     # API-processed page chunks
│   ├── API_TOKEN/    # API-processed token chunks
│   ├── DOCU_PAGE/    # Document Loader processed page chunks
│   └── DOCU_TOKEN/   # Document Loader processed token chunks
└── Loader/
    └── Document/     # Document-loader-processed metadata
    └── UpstageAPI/   # UpstageAPI-processed metadata
```

## Dependencies

- requests: For API calls and token counting
- Various document processing libraries (specific to each file type)
- Upstage API (optional, for PDF processing)
- logging: For detailed logging functionality
- json: For configuration and metadata handling
- os: For file system operations
- re: For text cleaning and pattern matching

## Logging

The system maintains detailed logs in the `logs` directory using a rotating file handler:
- Log files are limited to 5MB each
- Up to 10 backup log files are maintained
- Log format: `%(asctime)s - %(name)s - %(levelname)s - %(message)s`
- Logs are written to both file and console
- Log files are stored in `./logs/`

## Notes

- The system automatically handles file encoding and special characters
- CID references in PDFs are automatically cleaned
- Token counting is performed via an API endpoint
- File paths are automatically created if they don't exist
- The system supports both single file and directory processing
- Excludes `.ipynb_checkpoints` directories from processing 
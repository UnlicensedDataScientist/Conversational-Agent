# Conversational-Agent

# Prerequisites

- Python 3.10+
- UV (`pip install uv`)

## Installation

1. **Clone Repository**:

```bash
   git clone https://github.com/UnlicensedDataScientist/Conversational-Agent.git
   cd Conversational-Agent
```

2. **Create Virtual Environment**:

   ```
   uv venv venv
   ```

3. **Activate Environment**:

   ```
   # Linux/MacOS
   source venv/bin/activate

   # Windows
   .\venv\Scripts\activate
   ```

4. **Install Dependencies**:

   ```
   uv pip install .
   ```

5. **Download the English language model**

   ```
   uv pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.1/en_core_web_sm-3.7.1.tar.gz
   ```

## Usage

- **Start the FastAPI server:**

  ```
  chainlit run --port <port> main.py
  ```

  or

  ```
  chainlit run main.py
  ```

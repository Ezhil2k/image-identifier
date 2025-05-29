# image-identifier

image-identifier is a modular AI-based image search engine designed for semantic image retrieval and visual similarity matching. It features a FastAPI backend and Next.js frontend for an intuitive user interface.

## Features

- Search images using natural language queries
- Find visually similar images
- Face detection and grouping
- Modern web interface with real-time search
- Efficient vector indexing and fast search
- Modular design for easy integration into larger applications

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Ezhil2k/image-identifier.git
cd image-identifier
```

### 2. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup

```bash
cd frontend
npm install
```

## Usage

### 1. Start the Backend Server

```bash
cd backend
source venv/bin/activate    # On Windows: venv\Scripts\activate
uvicorn main:app --reload
```

The backend will be available at http://localhost:8000

### 2. Start the Frontend Development Server

```bash
cd frontend
npm run dev
```

The frontend will be available at http://localhost:3001

### 3. Using the Application

1. Add your images to the `backend/images/` directory
2. Access the web interface at http://localhost:3001
3. Use the search bar to find images using natural language
4. Navigate to the Faces tab to view face groupings

## Notes

- Ensure both backend and frontend servers are running simultaneously
- The backend will automatically process new images added to the images directory
- Update backend dependencies after installing new packages:
  ```bash
  pip freeze > requirements.txt
  ```
- Update frontend dependencies after installing new packages:
  ```bash
  npm install <package-name>
  ```

## Notes

- Ensure the virtual environment is activated before running any scripts.
- Update the `requirements.txt` file after installing any new dependencies:

```bash
pip freeze > requirements.txt
```
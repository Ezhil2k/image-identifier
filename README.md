

# image-identifier

image-identifier is a modular AI-based image search engine designed for semantic image retrieval and visual similarity matching. It is intended as the core engine for a personal photo management system.

## Features

- Search images using natural language queries
- Find visually similar images
- Efficient vector indexing and fast search
- Modular design for easy integration into larger applications

## Setup and Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/image-identifier.git
cd image-identifier
```

### 2. Create and Activate a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Usage

1. Add your images to the `images/` directory.
2. Run `clip_test.py` to:
   - Embed the images
   - Build the FAISS index
   - Search using text or image queries

```bash
python clip_test.py
```

## Notes

- Ensure the virtual environment is activated before running any scripts.
- Update the `requirements.txt` file after installing any new dependencies:

```bash
pip freeze > requirements.txt
```



# Data_Cleaner_APIs

## Overview
This project is designed to handle various types of data processing, including numeric and textual data, using a web server built with Flask. The server interacts with a MongoDB database and includes functionality for natural language processing (NLP), data transformation, and outlier detection.

## Features
- Web server built with Flask
- MongoDB integration using pymongo
- NLP capabilities using NLTK, TextBlob, Gensim, and other libraries
- Data transformation and outlier detection
- Cross-Origin Resource Sharing (CORS) support
- User authentication with bcrypt and JWT

## Prerequisites
- Python 3.x
- MongoDB database

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Set up the virtual environment
Create and activate a virtual environment:
```bash
python -m venv venv
# Activate the virtual environment (Windows)
venv\Scripts\activate
```

### 3. Install dependencies
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

## Configuration
### MongoDB
Ensure you have a MongoDB instance running. you can learn everything you need to do following this link: https://www.mongodb.com/docs/

## Usage

### Running the Server
To run the server, use the following command:
```bash
python server.py
```

### Example Routes
The routes for this project are defined in `routes.py`. Make sure to check the routes file to understand the available endpoints and their usage.

## Troubleshooting
If you encounter any issues with the virtual environment, you can create a new one and install the dependencies again:
```bash
python -m venv venv
# Activate the virtual environment (Windows)
venv\Scripts\activate
pip install -r requirements.txt
```

## Contributors
- **Numeric Data Processing**: Mohammed
- **Textual Data Processing**: @4bdex
- **None generic Data Processing**: @Khalid4dev

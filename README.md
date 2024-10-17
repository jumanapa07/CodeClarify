# CodeSnip Challenges

## Overview
CodeSnip Challenges is a comprehensive web application designed to help programmers enhance their coding skills. Users can share code snippets, practice coding challenges in multiple languages, and receive concise code summaries through the integration of the CodeBERT model.

## Features
- **Code Snippet Sharing**: Users can share and explore code snippets categorized by language.
- **Coding Challenges**: Engage in practice sessions with isolated environments using Docker.
- **Code Summarization**: Utilize the fine-tuned CodeBERT model for generating concise summaries of code snippets.
- **Multi-Language Support**: Practice coding challenges in languages like Python, C++, and Java.
- **Error Reporting**: View outputs and any compilation errors during code execution.

## Technologies Used
- **Frontend**: HTML, CSS, JavaScript
- **Backend**: Django, Flask
- **Containerization**: Docker
- **Machine Learning**: CodeBERT for code summarization

## Installation
To set up the project locally, follow these steps:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/codesnip-challenges.git
   cd codesnip-challenges
2. **Set Up Docker: Ensure Docker is installed and running on your machine.**

3. **Build and Run Docker Container**:

  ```bash
  
  docker build -t codesnip .
  docker run -p 5000:5000 codesnip

4. **Access the Application: Open your web browser and go to http://localhost:5000. **


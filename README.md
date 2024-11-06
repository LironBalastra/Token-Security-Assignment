# Token Security Project - Liron Balastra

## Description

A FastAPI-based application that exploring github repository.

## Prerequisites

- Python 3.10 or higher

## Project Structure

```
Token Security Github Assignment/
├── docker-compose.yml
├── frontend/
│   ├── Dockerfile
│   └── ... (frontend files)
└── backend/
    ├── Dockerfile
    ├── requirements.txt
    └── ... (backend files)
```

## Installation

1. Clone the repository:

    ```bash
    git clone [your-repository-url]
    cd Liron_Token_Security
    ```

2. Creating a personal access token:
   
    - Login to Github
    - In the upper-right corner of any page on GitHub, click your profile photo, then click on settings icon.
    - In the left sidebar, click Developer settings.
    - In the left sidebar, under Personal access tokens, click Tokens (classic).
    - In the "Note" field, give your token a descriptive name.
    - To give your token an expiration, select Expiration, then choose a default option or click Custom to enter a date.
    - Select the scopes you'd like to grant this token. To use your token to access repositories from the command line, select repo. A token with no assigned scopes can only access public information.
    - Click Generate token
    
    source: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens

3. Update Server with your Token:

   Create a .env file in backend directory:
    ```bash
    GITHUB_TOKEN=your_token_here
    ```
   
4. Run Project with Docker:

    ```bash
    docker compose up --build
    ```
5. Open the Front-React App:

   The Front-React will be available at: 'http://localhost:5173/'
   
(The API will be available at `http://localhost:8000`)



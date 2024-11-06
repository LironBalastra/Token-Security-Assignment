from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from github_service import GithubService
githubService = GithubService()

'''
    source-Github API:     https://docs.github.com/en/rest/repos/contents?apiVersion=2022-11-28
'''

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/repo-files/")
async def get_repo_files(repo_url: str):
    try:

        # Get owner and repo_name from repository url.
        valid, info = githubService.get_repo_details(repo_url)
        if not valid:
            raise HTTPException(status_code=400, detail=info["message"])
        
        owner, repo_name = info["owner"], info["repo_name"]

        # Get file names list from the input repo.
        name_list = await githubService.fetch_repo_content(owner, repo_name)
        return name_list

    except ValueError as e:
        print(e)
        raise HTTPException(status_code=400, detail=str(e))
    


@app.get("/file-content/")
async def file_content(repo_url, file_path):
    try:
        valid, info = githubService.get_repo_details(repo_url)
        if not valid:
            raise HTTPException(status_code=400, detail=info["message"])
        
        owner, repo_name = info["owner"], info["repo_name"]

        content_response = await githubService.get_file_content(owner, repo_name, file_path)

        return JSONResponse(content={
            "success": True,
            "data": {
                "content": content_response["content"],
                "type": content_response["type"],
                "extension": content_response["extension"],
                "filename": file_path
            }
        })
    
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "error": e.detail
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )


@app.get("/")
def get_repo_files():
    return "Hello, welcome to Liron's assignment for token security!"
import aiohttp
import asyncio
from fastapi import HTTPException
import base64
import os

class GithubService():
    def __init__(self):
        self.BASE_API = "https://api.github.com"

        self.GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')
        
        self.HEADER = {
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "Python/aiohttp",
                "Authorization": f"token {self.GITHUB_TOKEN}"
            }
        

    '''
        This function validates api github request for reepoistory content and returns {owner} and {repo_name}
    '''
    def get_repo_details(self, repo_url):
        # repo url struct:      https://github.com/{owner}/{repo_name}

        if "github.com" not in repo_url:
            return False, {"message": "invalid github repo url."}
        
        details_url = repo_url.split("github.com/")[1]
        if "/" not in details_url:
            return False, {"message": "invalid github repo url."}

        owner, repo_name = details_url.split("/")
        if not owner or not repo_name:
            False, {"message": "invalid github repo url."}
        
        return True, {"owner": owner,
            "repo_name": repo_name}



    '''
        Asynchronous function - sends from a given URL using aiohttp.
    '''
    async def __send_request(self, session, url, detail=""):
        async with session.get(url, headers=self.HEADER) as response:
            if response.status == 404:
                raise HTTPException(
                    status_code=404,
                    detail="not found"
                    )
            
            elif response.status != 200:
                raise HTTPException(
                    status_code=response.status,
                    detail=f'{detail}: {response.status}.'
                    )

            contents = await response.json()
            return contents
    

    '''
        Returns names list from {owner} reespository named {repo_name}, Recursively.
    '''
    async def fetch_repo_content(self, owner, repo_name):
        
        names = []
        await self.__fetch_repo_files_names(owner, repo_name, paths=[""], names=names) 
        print("Total files: ", str(len(names)))
        return names


    '''
        Helper recursively frunction, fetches all file names from a GitHub repository by traversing through all directories and subdirectories.
        Using aiohttp ClientSession for making asynchronous HTTP requests for improving performance.
        
        Parameters:
        * paths - list of relative repository paths to scan.
            (path = "" :     root repository)
        * names - list of file names that the recursion updates while scanning the repo.

        The function builds URLs for each path in paths and then scans the path:
            * adds all file names into the names list
            * adds all folder paths into the paths list for recursive scanning

        URL example: "https://api.github.com/repos/owner/repo/contents/path"
    '''
    async def __fetch_repo_files_names(self, owner, repo_name, paths, names):

        if not paths:
            return
        
        urls = []

        # Builds URLs for each path
        for p in paths:
            urls.append(f"{self.BASE_API}/repos/{owner}/{repo_name}/contents/{p}")  
            
        async with aiohttp.ClientSession() as session:
            tasks = [self.__fetch_file_names(session, url, names) for url in urls]
            
            '''
            any task(__fetch_file_names) returns list of files names so gather returns list of lists:
            [[path1_output], [path2_output], [path3_output]...]
            '''
            subdir_paths_nested = await asyncio.gather(*tasks)

            # Flatten the list of lists into a single list
            subdir_paths = []
            for sublist in subdir_paths_nested:
                subdir_paths.extend(sublist)

            await self.__fetch_repo_files_names(owner, repo_name, subdir_paths, names)


    '''
        Helper asynchronous function to fetch data from a given URL using aiohttp.
        The function:
            * updates the names list with file names in the current URL path
            * returns subdir_paths with relative paths of folders for recursive scanning
    '''
    async def __fetch_file_names(self, session, url, names):
        subdir_paths = []
        contents = await self.__send_request(session, url, "error during fetching file name.")

        if not isinstance(contents, list):
            raise HTTPException(
                status_code=400, 
                detail="Invalid response format from GitHub API - list expected."
            )
        
        # Checks path items, files of folders.
        for item in contents:
            if item["type"] == "file":
                names.append(item["path"])
            elif item["type"] == "dir":
                subdir_paths.append(item["path"])
        
        # Returns subdir paths for recursive tracking
        return subdir_paths



    '''
        Asynchronous function to fetch file content.
        The function returns file content based on format:
        * Images:       Base64 encoded (default from GitHub API)
        * Text files:   UTF-8 decoded
        * Other formats: Not supported and will raise an error

        The function returns dictionary.
        Dictionary format:
            {
                "success": true,
                "data": {
                    "content": "content_here",
                    "type": "image|text",
                    "extension": "file_extension"
                }
            }
    '''
    async def get_file_content(self, owner, repo_name, file_path):
        try:

            # GitHub API URL for getting file content
            url = f"{self.BASE_API}/repos/{owner}/{repo_name}/contents/{file_path}"

            async with aiohttp.ClientSession() as session:
                data = await self.__send_request(session, url, "Error fetching file content: ")

                if "content" not in data:
                    raise HTTPException(status_code=400, detail="No content found")
                
                file_extension = file_path.lower().split('.')[-1]

                # Images:
                if file_extension in ['png', 'jpg', 'jpeg', 'gif']:
                    content = data["content"]
                    return {
                            "content": content,
                            "type": "image",
                            "extension": file_extension
                        }
                
                # Text files:
                else:
                    try:
                        content = base64.b64decode(data["content"]).decode("utf-8")
                        return {
                                "content": content,
                                "type": "text",
                                "extension": file_extension
                            }
                    
                    # Not supported formats:
                    except UnicodeDecodeError:
                        raise HTTPException(
                            status_code=400, 
                            detail="File format is not supported for viewing"
                        )

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
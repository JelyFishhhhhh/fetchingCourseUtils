import os
import requests
from bs4 import BeautifulSoup
from asyncio import run, gather
import json

avalFiles= [".java", ".class", ".txt", ".form"]

async def fetch_course_files(url):
    
    print(f"Fetching from {url}")
    
    if url.endswith("/"):
        lastDir= url.split("/")[5:]
        os.makedirs(os.path.join(".", *lastDir), exist_ok=True)
        
    
    html= requests.get(url)
    
    soup= BeautifulSoup(html.content, "html.parser")
    
    files= soup.find_all("a")
    for file in files:
        href= file.get("href")
        if href.endswith("/"):
            if href.startswith("/~yien/"):
                continue
            await fetch_course_files(url+href)
        elif any(href.endswith(af) for af in avalFiles):
            lastDir= url.split("/")[5:]
            dir= os.path.join(".", *lastDir)
            try:
                file_response = requests.get(url + href)
                file_response.raise_for_status()
                with open(os.path.join(dir, href), "w", encoding="utf8") as f:
                    f.write(file_response.text)
            except requests.RequestException as e:
                print(f"Failed to fetch the file {href}: {e}")

async def main():
    
    with open("./info.json", "r") as f:
        info = json.load(f)
        url = info["url"]

    # fetch course
    tasks = [fetch_course_files(url+f"course0{i}/") for i in range(1, 8)]
    await gather(*tasks)
    

if __name__ == "__main__":
    if not os.path.exists("./info.json"):
        with open("./info.json", "w") as f:
            json.dump({"url": ""}, f)
        print("打開info.json並自行填入url(http://.../javaprog/)")
    run(main())

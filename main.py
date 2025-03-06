import os
import requests
from bs4 import BeautifulSoup
from asyncio import run, gather
import json

async def fetch_course_files(courseNum, url):
    
    url+= f"course0{courseNum}/"
    print(f"Fetching course {courseNum} from {url}")
    
    course_dir = f"./course{courseNum}"
    os.makedirs(course_dir, exist_ok=True)
    
    html= requests.get(url)
    
    soup= BeautifulSoup(html.content, "html.parser")
    
    files= soup.find_all("a")
    for file in files:
        href= file.get("href")
        if href.endswith(".java"):
            try:
                file_response = requests.get(url + href)
                file_response.raise_for_status()
                with open(os.path.join(course_dir, href), "w", encoding="utf8") as f:
                    f.write(file_response.text)
            except requests.RequestException as e:
                print(f"Failed to fetch the file {href}: {e}")

async def main():
    
    with open("./info.json", "r") as f:
        info = json.load(f)
        url = info["url"]

    # fetch course
    tasks = [fetch_course_files(i, url) for i in range(1, 8)]
    await gather(*tasks)
    

if __name__ == "__main__":
       
    run(main())

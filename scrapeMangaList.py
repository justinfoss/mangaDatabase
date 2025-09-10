import requests
from bs4 import BeautifulSoup
import re
import databaseInteract
import sqlite3
import asyncio

big = ["https://www.mangaupdates.com/lists/public/1v07qpu/2","https://www.mangaupdates.com/lists/public/1v07qpu/0"]
#url = "https://www.mangaupdates.com/lists/public/1v07qpu/2"

def get_chapter_number_from_latest_release(soup):
        # Find all divs with the correct class
        for div in soup.find_all("div", class_="info-box_sContent__CTwJh"):
            # Look for c.<i>118 (end)</i> pattern
            i_tags = div.find_all("i")
            for i_tag in i_tags:
                match = re.match(r"(\d+)", i_tag.get_text())
                if match:
                    return match.group(1)
        return None

def get_last_chapter(manga_url):
        resp = requests.get(manga_url)
        soup = BeautifulSoup(resp.text, "html.parser")
        # Try to get chapter number from latest release(s)
        chapter_number = get_chapter_number_from_latest_release(soup)
        if chapter_number:
            return chapter_number
        #print(f"--- HTML for {manga_url} ---")
        #print(resp.text)
        # Try to find the last released chapter info
        chapter_tag = soup.find("div", class_="series_latest_chapter__Qw2lO")
        if chapter_tag:
            return chapter_tag.get_text(strip=True)
        # Fallback: try to find by label
        for label in soup.find_all("div", class_="series_label__GvQ7r"):
            if "Latest Release" in label.get_text():
                value = label.find_next_sibling("div")
                if value:
                    return value.get_text(strip=True)
        return None
def pullFromWeb():
    for url in big:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        if url == "https://www.mangaupdates.com/lists/public/1v07qpu/2":
            for row in soup.select("div.public-list-row_alt__wlDod"):
                # Title and URL
                a_tag = row.select_one("a[title='Click for Series Info']")
                title = a_tag.get_text(strip=True)
                title = title.replace("'","")
                manga_url = a_tag["href"]
                #if title == "Crimson Karma":
                # Rating (the next div with class 'text text-center col-1')
                rating_div = row.select_one("div.text.text-center.col-1")
                try:
                    rating = float(rating_div.get_text(strip=True) if rating_div else None)
                except ValueError:
                    rating = None
                last_chapter = get_last_chapter(manga_url)
                mangaCompletion = "Completed"
                #print(f"Title: {title}")
                #print(f"URL: {manga_url}")
                #print(f"Rating: {rating}")
                #print(f"Last Released Chapter: {last_chapter}")
                #print("-----")
                #if 
                try:
                    databaseInteract.addManga(title, rating, mangaCompletion, manga_url,last_chapter)
                    #print("Added!")
                    pass
                except sqlite3.IntegrityError:
                    #print(f"[{title}] is already in the system")
                    databaseInteract.showSpecificManga(title)
                    #print(f"Updating {title}...")
                    databaseInteract.updateManga(title, rating, mangaCompletion, manga_url,last_chapter)
                    #print(f"{title} is updated :)")
                    print(" ")
                else:
                    print("Something broke")
        elif url == "https://www.mangaupdates.com/lists/public/1v07qpu/0":
            for row in soup.select("div.public-list-row_alt__wlDod"):
                # Title and URL
                a_tag = row.select_one("a[title='Click for Series Info']")
                title = a_tag.get_text(strip=True)
                title = title.replace("'","")
                manga_url = a_tag["href"]
                # Rating (the next div with class 'text text-center col-1')
                rating_div = row.select_one("div.text.text-center.col-1")
                try:
                    rating = float(rating_div.get_text(strip=True) if rating_div else None)
                except ValueError:
                    rating = None
                # Last chapter (from 'text text-center col-2')
                last_chapter_div = row.select_one("div.text.text-center.col-2")
                last_chapter_raw = last_chapter_div.get_text(strip=True) if last_chapter_div else None
                # Extract just the chapter number (e.g., from 'v.1 c.15' get '15')
                last_chapter = None
                if last_chapter_raw:
                    match = re.search(r"c\.?\s*(\d+)", last_chapter_raw)
                    if match:
                        last_chapter = match.group(1)
                    else:
                        # If no 'c.' pattern, try to find any number
                        match = re.search(r"(\d+)", last_chapter_raw)
                        if match:
                            last_chapter = match.group(1)
                mangaCompletion = "Reading"
                #print(f"Title: {title}")
                #print(f"URL: {manga_url}")
                #print(f"Rating: {rating}")
                #print(f"Last Released Chapter: {last_chapter}")
                #print("-----")
                try:
                    databaseInteract.addManga(title, rating, mangaCompletion, manga_url,last_chapter)
                    #print("Added!")
                    pass
                except sqlite3.IntegrityError:
                    #print(f"[{title}] is already in the system")
                    databaseInteract.showSpecificManga(title)
                    #print(f"Updating {title}...")
                    databaseInteract.updateManga(title, rating, mangaCompletion, manga_url,last_chapter)
                    #print(f"{title} is updated :)")
                    #print(" ")
                else:
                    print("Something broke")
    finalaile = "Database has been updated"
    return finalaile


def searchManga(title):

    url = "https://api.mangaupdates.com/v1/series/search"
    payload = {
        "search": title
    }
    response = requests.post(url, json=payload)
    data = response.json()

    # Refine to first four results
    refined_results = []
    for manga in data["results"][:4]:
        refined = {
            'title': manga['record']['title'],
            'bayesian_rating': manga['record']['bayesian_rating'],
            'type': manga['record']['type'],
            'url': manga['record']['url']
        }
        refined_results.append(refined)
    return refined_results

print(searchManga("Solo Leveling"))
import sqlite3

databaseName = "mangaCollection.db"
conn = sqlite3.connect(databaseName)


def addManga(mangaName: str, mangaRating: float, mangaCompletion: str, mangaLink: str,mangaChapter: int):
    cursor = conn.cursor()
    cursor.execute(f"""INSERT INTO manga (name,rating,completionStatus,link,chapter) VALUES ('{mangaName}','{mangaRating}','{mangaCompletion}','{mangaLink}',{mangaChapter})""")
    conn.commit()
    
def addColumn(columnAdd):
    cursor = conn.cursor()
    cursor.execute(f"""ALTER TABLE manga ADD COLUMN {columnAdd}""")
    conn.commit()
    print("Column has been added")

def showManga():
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM manga;""")
    rows = cursor.fetchall()
    return rows

def showSpecificManga(mangaName: str):
        cursor = conn.cursor()
        cursor.execute(f"""SELECT name, rating, completionStatus, chapter, link FROM manga WHERE name = '{mangaName}';""")
        rows = cursor.fetchall()
        for a in rows:
            return a

def showMostChaptersManga():
    cursor = conn.cursor()
    cursor.execute("""SELECT name, rating, completionStatus, chapter, link FROM manga ORDER BY chapter DESC LIMIT 1;""")
    row = cursor.fetchone()
    return row

def showHighRatingManga():
    cursor = conn.cursor()
    cursor.execute(f"""SELECT name, rating, completionStatus, chapter, link FROM manga WHERE rating IS NOT 'None' AND rating > 8;""")
    rows = cursor.fetchall()
    return rows
    #for a in rows:
    #     return a

def updateManga(mangaName: str, mangaRating: float, mangaCompletion: str, mangaLink: str,mangaChapter: int):
    cursor = conn.cursor()
    cursor.execute(f"""UPDATE manga SET rating = '{mangaRating}', completionStatus = '{mangaCompletion}', link = '{mangaLink}', chapter = {mangaChapter} WHERE name = '{mangaName}'""")
    conn.commit()
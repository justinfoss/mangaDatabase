import databaseInteract

while True:
    userWant=None
    userWant = int(input("""What do you want to do?
(1) See all manga
(2) Add a manga
(3)
What is your selection: """))
    if userWant == 1:
        for potential in databaseInteract.showManga():
            print("-----")
            print("Title: "+potential[0])
            print("Chapter: "+str(potential[4]))
            print("Rating: "+str(potential[1]))
            print("Completion Status: "+potential[2])
        cont = input("Press Enter: ")
    if userWant == 2:
        mangaName=input("Name of manga: ")
        mangaRating=float(input("Rating of manga: "))
        mangaCompletion=input("Completion status of manga: ")
        mangaLink=input("Link to manga: ")
        mangaChapters=int(input("How many chapters have been read: "))
        databaseInteract.addManga(mangaTitle, mangaRating, mangaCompletion, mangaLink,mangaChapters)
    if userWant == 3:
        mangaTitle = input("What manga: ")
        potential = databaseInteract.showSpecificManga(mangaTitle)
        print(potential)
        print("-----")
        print("Title: "+potential[0])
        print("Chapter: "+str(potential[3]))
        print("Rating: "+str(potential[1]))
        print("Completion Status: "+potential[2])
        cont = input("Press Enter: ")
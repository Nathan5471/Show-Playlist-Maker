import os.path
from showPlaylistMaker import *


def mainMenu():
    # The main menu
    print("")
    print("-------------------")
    print("1) Add show")
    print("2) Edit show")
    print("3) Remove show")
    print("4) Get shows")
    print("5) Change order")
    print("6) Create playlist")
    print("-------------------")
    print("")

    try:
        selection = int(input("Enter Your Selection: "))
    except ValueError:
        print("Please input a valid number")
        mainMenu()

    if selection == 1:
        addShowCLI()

    elif selection == 2:
        editShowCLI()

    elif selection == 3:
        removeShowCLI()

    elif selection == 4:
        getShowsCLI()

    elif selection == 5:
        changeOrderCLI()

    elif selection == 6:
        createPlaylistCLI()

    else:
        print("Please select a valid number")
        mainMenu()


def addShowCLI():
    showName = input("Enter the name of the show you want to add: ")
    while True:
        folderLocation = input("Enter the location of the folder: ")
        if os.path.exists(folderLocation):
            break
        else:
            print(
                "Folder location does not exists, please input a valid folder location"
            )
            continue
    while True:
        try:
            episodesPerRun = int(
                input("Enter the number of episodes you want per cycle: ")
            )
        except ValueError:
            print("Please input a integer")
            continue
        break
    result = addShow(showName, folderLocation, episodesPerRun)
    if result[0]:
        print("")
        print("The show was added succesfully, but to confirm here is the information")
        print(f"Name: {showName}")
        print(f"Episodes per cycle: {episodesPerRun}")
        print(f"Seasons: {result[1]}")
        print(f"Episodes: {result[2]}")
        print("")
        while True:
            informationIsCorrect = input("Is this information correct [y/n]: ")
            if informationIsCorrect == "y":
                print(f"{showName} has been added!")
                mainMenu()
            elif informationIsCorrect == "n":
                removeShow(showName)
                print("You can try to add the show again, if you would like")
                mainMenu()
            else:
                print("Please input y or n")


def editShowCLI():
    shows = getShows()
    print("")
    print("----------------------")
    for show in shows:
        print(f"{shows.index(show) + 1}) {show}")
    print("----------------------")
    print("")
    while True:
        try:
            showSelection = int(input("Enter the show to edit: "))
        except ValueError:
            print("Please input a valid number")
            continue
        if showSelection > len(shows):
            print("Please input a valid number")
            continue
        break
    print("")
    print("----------------------")
    print("1) Name")
    print("2) Folder location")
    print("3) Episodes per cycle")
    print("4) Rescan episodes")
    print("----------------------")
    print("")
    while True:
        try:
            editSelection = int(input("Enter your selection to edit: "))
        except ValueError:
            print("Please input a valid number")
            continue
        break
    if editSelection == 1:
        newName = input("Enter the new name for this show: ")
        while True:
            confirmation = input(
                f"Are you sure you want to rename {shows[showSelection - 1]} to {newName} [y/n]: "
            )
            if confirmation == "y":
                break
            elif confirmation == "n":
                mainMenu()
            else:
                print("Please input a valid y or n")
        result = changeShowName(shows[showSelection - 1], newName)
        if result == True:
            print("The show has been edited sucessfully!")
            mainMenu()
    elif editSelection == 2:
        newFolderLocation = input("Enter the new folder location for this show: ")
        if os.path.exists(newFolderLocation):
            previousFolderLocation = getShowInformation(shows[showSelection - 1])
            result = changeShowFolder(shows[showSelection - 1], newFolderLocation)
            if result[0]:
                print(
                    f"The location of {shows[showSelection - 1]} has been changed to {newFolderLocation}"
                )
                print(
                    f"In the new location, there is {result[1]} seasons and {result[2]} episodes"
                )
                while True:
                    confirmation = input("Is this information corret [y/n]: ")
                    if confirmation == "y":
                        mainMenu()
                    elif confirmation == "n":
                        print(
                            f"Changing the folder location back to {previousFolderLocation[2]}"
                        )
                        changeShowFolder(
                            shows[showSelection - 1], previousFolderLocation[2]
                        )
                        mainMenu()
                    else:
                        print("Please input y or n")
    elif editSelection == 3:
        while True:
            try:
                newEpisodesPerRun = int(
                    input("Enter how many episodes your want per cycle: ")
                )
            except:
                print("Please input a valid number")
                continue
            break
        result = changeEpisodePerRun(shows[showSelection - 1], newEpisodesPerRun)
        if result:
            print(f"{shows[showSelection - 1]} now has {newEpisodesPerRun} per session")
    elif editSelection == 4:
        showInformation = getShowInformation(shows[showSelection - 1])
        results = changeShowFolder(shows[showSelection - 1], showInformation[2])
        if results[0]:
            print(
                f"{shows[showSelection - 1]} now has {results[1]} seasons and {results[2]} episodes"
            )
            mainMenu()


def removeShowCLI():
    shows = getShows()
    print("")
    print("----------------------")
    for show in shows:
        print(f"{shows.index(show) + 1}) {show}")
    print("----------------------")
    print("")
    while True:
        try:
            showSelection = int(input("Enter the show to delete: "))
        except ValueError:
            print("Please input a valid number")
            continue
        if showSelection > len(shows):
            print("Please input a valid number")
            continue
        break
    while True:
        confirmation = input(
            f"Are you sure your want to delete {shows[showSelection - 1]} [y/n]: "
        )
        if confirmation == "y":
            break
        elif confirmation == "n":
            mainMenu()
        else:
            print("Please select y or n")
    result = removeShow(shows[showSelection - 1])
    if result:
        print(f"{shows[showSelection - 1]} has been succesfully deleted")
        mainMenu()


def getShowsCLI():
    shows = getShows()
    for show in shows:
        showInformation = getShowInformation(show)
        episodeCount = getEpisodeCount(show)
        print("")
        print(show)
        print(f"  Episodes per cycle: {showInformation[1]}")
        print(f"  Folder location: {showInformation[2]}")
        print(f"  Show position: {showInformation[3]}")
        print(f"  Episodes: {episodeCount[0]}")
        print(f"  Seasons: {episodeCount[1]}")
        print("")
    input("Press enter for main menu")  # Allows time for viewing information
    mainMenu()


def changeOrderCLI():
    shows = getShows()
    position = 1
    showsPosition = []
    while True:
        if shows == []:
            break
        print("")
        print("----------------------")
        for show in shows:
            print(f"{shows.index(show) + 1}) {show}")
        print("----------------------")
        print("")
        while True:
            try:
                showSelection = int(
                    input(f"Enter the show to be in position {position}: ")
                )
            except ValueError:
                print("Please input a number")
                continue
            if showSelection > len(shows):
                print("Please input a valid number")
                continue
            break
        showsPosition.append(shows[showSelection - 1])
        position += 1
        shows.remove(shows[showSelection - 1])
        print(f"The current order is {showsPosition}")
    for show in showsPosition:
        print(f"{showsPosition.index(show) + 1}) {show}")
    while True:
        confirmation = input("Are you sure you want the above order [y/n]: ")
        if confirmation == "y" or confirmation == "n":
            break
        print("Please input y or n")
    if confirmation == "n":
        mainMenu()
    for show in showsPosition:
        result = changeShowPosition(show, (showsPosition.index(show) + 1))
        if result:
            continue
    print("Show order sucessfully changed!")
    mainMenu()


def createPlaylistCLI():
    check = checkShowPositionExist()  # Makes sure every show has a position
    if not check:
        print("Please make an order for your shows")
        mainMenu()
    while True:
        try:
            lengthOfPlaylist = int(
                input("Enter how many episodes you want in your playlist: ")
            )
        except TypeError:
            print("Please input a number")
            continue
        break
    playlist = createShowOrder(lengthOfPlaylist)
    while True:
        folderLocation = input("Enter the folder to copy the playlist to: ")
        if os.path.exists(folderLocation):
            break
        else:
            print("Please print a valid folder location")
    connection = sqlite3.connect("shows.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT 1 FROM previousMain")
    fileNumber = cursor.fetchone()
    if not fileNumber:
        fileNumber = 1
        cursor.execute("INSERT INTO previousMAIN(fileNumber) VALUES (1)")
    else:
        fileNumber = fileNumber[0]
    for episode in playlist:
        showLocation = getShowInformation(episode[0])[2]
        season = re.search(r"S(\d+)", episode[1]).group(1)
        if os.path.exists(f"{showLocation}/Season {season}/{episode[1]}"):
            print(f"Copying {episode[1]} from {episode[0]}")
            copyShow(
                episode[0],
                f"{showLocation}/Season {season}/{episode[1]}",
                episode[1],
                fileNumber,
                folderLocation,
            )
            fileNumber += 1
    cursor.execute(f"UPDATE previousMain SET fileNumber = {fileNumber}")
    connection.commit()
    connection.close()
    print(f"Files sucessfully copied into {folderLocation}")
    mainMenu()


mainMenu()
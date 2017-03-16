"""
Name       : L Trevor Davies
Program    : itunes_search.py
Description: Searches iTunes store using Apple's API
"""

# Imports
import sys
import os
import json
import urllib
from tabulate import tabulate


def open_file(file_name):
    """
    Opens the user specified JSON file.
    Then calls the display function to display 
    the file to the user.
    :param file_name - name of file to be opened:
    :return None:
    """
    # Local variables

    # ******** start open_file() ******** #

    # Input JSON data from given file name
    with open(file_name, "r") as f:
        data = json.load(f)

    # Display the imported data
    display(data)


def output_file(data):
    """
    Outputs the data that was received from 
    the iTunes search API into a JSON file.
    :param data - JSON data to be outputted to a file:
    :return None:
    """
    # Local variables

    # ******** start output_file() ******** #
    
    # Load data into file
    with open("search_results.json", "w") as f:
        json.dump(data, f)

    print("File saved as search_results.json!")


def detailed_track(track):
    """
    Outputs a more detailed list for the 
    chosen track. 
    :param track - The track the user wants a detailed list for:
    :return None:
    """
    # Local variables
    artist     = track["artistName"]
    song       = track["trackName"]
    date       = get_date(track["releaseDate"])
    col_name   = track["collectionName"]
    col_price  = str(track["collectionPrice"])
    song_price = str(track["trackPrice"])
    song_num   = str(track["trackNumber"])
    song_count = str(track["trackCount"])
    kind       = track["kind"]
    genre      = track["primaryGenreName"]

    # ******** start detailed_track() ******** #

    # Output detailed page
    clear()
    print("-- " + song + " Details Page --")
    print("Artist: " + artist)
    print("Track: " + song)
    print("Release date: " + date)
    print("Collection name: " + col_name)
    print("Collection price: " + col_price)
    print("Track price: " + song_price)
    print("Track number: " + song_num)
    print("Track count: " + song_count)
    print("Kind: " + kind)
    print("Genre: " + genre)
    print("")
    pause()


def select(tracks):
    """
    Allows the user to either chose a track 
    to show more details or quit. 
    :param tracks - a list of tracks retrieved from the iTunes API:
    :return None:
    """
    # Local variables
    choice = -1

    # ******** start select() ******** #

    # Get user to input track number
    print("------------------")
    print("Enter track number (0 to quit)")
    choice = input("-> ")

    # Get input again if incorrect
    while choice > (len(tracks) + 1) or choice < 0:
        print("------------------")
        print("Enter track number (0 to quit)")
        choice = input("-> ")

    # User wants to exit
    if choice == 0:
        sys.exit()

    track = tracks[choice - 1]

    detailed_track(track)


def pause():
    """
    A simple function that pauses the terminal.
    This is used the pagination feature.
    :return None:
    """
    # Local variables

    # ******** start pause() ******** #

    raw_input("Press the <ENTER> key to continue...")


def get_date(date):
    """
    Quick function that makes the received date
    easier to look at.
    :param date - date retrieved from the iTunes API:
    :return date - an easier to look at date (to be outputted):
    """
    # Local variables
    date = date.split("T")
    date = date[0]

    # ******** start pause() ******** #
    return date


def display(results):
    """
    Displays whatever is retrieved from the API call.
    Gives the user the opprotunity to decide if they want
    to see the results in a pagination of 10, all results 
    at once, or output the results to a file.
    :param results - The JSON data retrieved from the API call:
    :return None:
    """
    # Local variables
    count = 0
    choice = 0
    lis = []
    output = []

    # ******** start display() ******** #

    # Add results to the list
    for wrapperType in results:
        count += 1
        lis.append(wrapperType)

    # Get users choice
    clear()
    print("-- Viewing Options --")
    print("1) 10 results per page")
    print("2) Show all results")
    print("3) Output to file")
    choice = input("-> ")

    # Get input again if incorrect
    while choice < 1 or choice > 3:
        clear()
        print("-- Viewing Options --")
        print("1) 10 results per page")
        print("2) Show all results")
        print("3) Output to file")
        choice = input("-> ")
    
    clear()

    # IF user chooses 10 results per page
    if choice == 1:
        # Loop through lis
        for i in range(0, len(lis)):
            # Output and pause if we have 10 listings
            if i % 10 == 0 and i != 0:
                clear()
                print(tabulate(output, headers=["Artist", "Release Date", "Track Name"]))
                pause()
                output = []
            track  = lis[i]
            artist = track["artistName"]
            date   = get_date(track["releaseDate"])
            song   = track["trackName"]
            output.append([str(i + 1), artist, date, song])
        clear()

        # Update the diplay one last time
        print(tabulate(output, headers=["Artist", "Release Date", "Track Name"]))
        select(lis)

    # IF user chooses all results
    if choice == 2:
        print("Artist\t\tRelease Date\t\tTrack Name")
        for i in range(0, len(lis)):
            track  = lis[i]
            artist = track["artistName"]
            date   = get_date(track["releaseDate"])
            song   = track["trackName"]
            output.append([str(i + 1), artist, date, song])
            print(str(i + 1) + ". " + artist + "\t\t" + date + "\t\t" + song)
        print(tabulate(output, headers=["Artist", "Release Date", "Track Name"]))
        select(lis)

    # IF user chooses to output to file
    if choice == 3:
        output_file(results)


def search(artist):
    """
    Calls the iTunes API and returns the results to main.
    :param artist - artist to be searched:
    :return results - The JSON data retrieved from the API call:
    """
    # Local variables
    encoded = urllib.quote(artist)
    rawData = urllib.urlopen("https://itunes.apple.com/search?term=" + encoded).read()
    jsonData = json.loads(rawData)
    results = jsonData["results"]

    # ******** start search() ******** #

    return results


def clear():
    """
    Simple function that clears the screen.
    Used in output functions.
    :return None:
    """
    # Local variables

    # ******** start clear() ******** #

    os.system("cls" if os.name == "nt" else "clear")


def main():
    """
    Gives the user the opprotunity to choose if they
    want to search using the iTunes API or input their
    own JSON file.
    :return None:
    """
    # Local variables
    choice = 0
    artist = ""
    file_name = ""

    # ******** start main() ******** #

    # User can search or input existing JSON file
    clear()
    print("-- iTunes Store Search --")
    print("1) Search artist")
    print("2) Import JSON file")
    choice = input("-> ")

    # Get input again if incorrect
    while choice < 1 or choice > 2:
        clear()
        print("-- iTunes Store Search --")
        print("1) Search artist")
        print("2) Import JSON file")
        choice = input("-> ")

    # IF user wants to search
    if choice == 1:
        clear()
        print("Artist to search:")
        artist = raw_input("-> ")

        # Get input again if blank
        while artist == "":
            clear()
            print("Artist to search:")
            artist = raw_input("-> ")

        results = search(artist)
        display(results)

    # IF user wants to import file
    if choice == 2:
        clear()
        print("Enter filename: ")
        file_name = raw_input("-> ")
        open_file(file_name)


if __name__ == "__main__": main()

import os

dir = r"A:\HSMW\2. Semester\Sachverständiger\DarkNight_Dataset"

def main(dir):

    jpg_files = list()
    mp4_files = list()
    png_files = list()
    text_files = list()
    gif_files = list()
    other_files = list()

    all_files = list()
    all_dirs = list()
    
    # Iterate for each dict object in os.walk()
    for root, dirs, files in os.walk(dir):
        # Add the files list to the all_files list
        all_files.extend(files)
        # Add the dirs list to the all_dirs list
        #all_dirs.extend(dirs)

    for file in all_files:
        if(file.split(".")[-1] == "jpg"):
            jpg_files.append(file)
        elif(file.split(".")[-1] == "png"):
            png_files.append(file)
        elif(file.split(".")[-1] == "mp4"):
            mp4_files.append(file)
        elif(file.split(".")[-1] == "txt"):
            text_files.append(file)
        elif(file.split(".")[-1] == "gif"):
            gif_files.append(file)
        else:
            other_files.append(file)

    print(f"Number of .jpg Files: {len(jpg_files)}")
    print(f"Number of .png Files: {len(png_files)}")
    print(f"Number of .mp4 Files: {len(mp4_files)}")
    print(f"Number of .gif Files: {len(gif_files)}")
    print(f"Number of .txt Files: {len(text_files)}")
    print(f"Number of other Files: {len(other_files)}")

main(dir)
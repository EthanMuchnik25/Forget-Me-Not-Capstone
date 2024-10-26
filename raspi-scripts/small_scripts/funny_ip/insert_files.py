import sys

creds_file = "service_account.json"
drive_folder_id_filename = "drive_folder_id.txt"
write_filename_filename = "write_filename.txt"


print("This script is supposed to try to make it easier for you to create all \
the startup file necessary for ip.py. This is some jank software engineering. I\
 don't care.\n")


def read_file_str(filename, description):

    print(description)
    print(f"Insert val for {filename} - press ctrl+d to finish.")
    in_val = sys.stdin.read()
    with open(filename, "w") as file:
        file.write(in_val)
    print("\nEpic.\n")

read_file_str(creds_file, "This input should be the big json key thing you get \
from fiddling with the google drive api guy.")

read_file_str(drive_folder_id_filename, "This input should be what comes after \
the /folder/<here> in the url when you are in the google drive folder you want \
to add the file to.")

read_file_str(write_filename_filename, "This should be the name of the file you\
 want to write to in google drive.")
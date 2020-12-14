import os
from glob import glob
from os import path

# delete all remaining file in the system

# def delete_old_input_file():
#     # remove file if old file exist ---
#     old_file = "input\*.png"

#     try:
#         for name in glob(old_file):

#             os.remove(name)
#             print("Old file removed. : " + str(name))

#     except Exception as e:
#         print("Error! " + str(e) + '\n')


def delete_old_output_file():
    # remove file if old file exist ---
    old_file = "output\*.png"

    try:
        for name in glob(old_file):
            
            os.remove(name)
            print("Old file removed. : " + str(name))

    except Exception as e:
        print("Error! " + str(e) + '\n')


def delete_old_denoised_file():
    # remove file if old file exist ---
    old_file = "output\denoise\*.png"

    try:
        for name in glob(old_file):
            
            os.remove(name)
            print("Old denoise file removed. : " + str(name))

    except Exception as e:
        print("Error! " + str(e) + '\n')


def delete_user_output():
    # remove file if old file exist ---
    old_file = "user-output\*.png"

    try:
        for name in glob(old_file):
            
            os.remove(name)
            print("Old user output file removed. : " + str(name))

    except Exception as e:
        print("Error! " + str(e) + '\n')


if __name__ == "__main__":
    
    print("Starting to remove all old file(s).")

    # delete old remaining file
    #delete_old_input_file()
    delete_old_output_file()
    delete_old_denoised_file()
    delete_user_output()

    print("All old file(s) removed.")


#################
#
# get_program_version
# written by: Andy Block
# date: Jan 3, 2021
#
#################
#
# this program simply prints out the version number of a given Windows executable.
# the only argument required is the file path of the exexcutable you want the version of.
#
# for example, the file path for chrome.exe at its default location is:
# filepath = 'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe'
#
# there are two different versions in Windows: the file version and the product version.
# usually these two values are equivalent, and if so, the program only prints one value.
# if they are not equal, both will be printed.
#
#################


from win32api import GetFileVersionInfo, HIWORD, LOWORD


def get_program_version(filepath):
    
        info = GetFileVersionInfo(filepath, '\\')
        
        file_version = str(HIWORD(info['FileVersionMS'])) + '.' + \
                       str(LOWORD(info['FileVersionMS'])) + '.' + \
                       str(HIWORD(info['FileVersionLS'])) + '.' + \
                       str(LOWORD(info['FileVersionLS']))
        
        product_version = str(HIWORD(info['ProductVersionMS'])) + '.' + \
                          str(LOWORD(info['ProductVersionMS'])) + '.' + \
                          str(HIWORD(info['ProductVersionLS'])) + '.' + \
                          str(LOWORD(info['ProductVersionLS']))
        
        if file_version == product_version:
            print("This program's version is: " + file_version)
        
        else:
            print("This program's file version is: " + file_version)
            print("This program's product version is: " + product_version)
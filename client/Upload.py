import os


def Upload_file(client, filename):
    if os.path.exists(filename):
        if os.path.isfile(filename):
            file_obj = open(filename, 'rb')
            client.send(file_obj.read())
            file_obj.close()

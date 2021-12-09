import socket
import sys
import os
import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

os.umask(000)

CHUNK_SIZE = 1_000_000


# dada
class Watcher:

    def __init__(self, directory=".", handler=FileSystemEventHandler()):
        self.observer = Observer()
        self.handler = handler
        self.directory = directory

    def run(self):
        self.directory = "C:\\Users\\User\\PycharmProjects\\network2\\CORPUS"
        self.observer.schedule(
            self.handler, self.directory, recursive=True)
        self.observer.start()
        print("\nWatcher Running in {}/\n".format(self.directory))
        try:
            while True:
                time.sleep(1)
        except:
            self.observer.stop()
        self.observer.join()
        print("\nWatcher Terminated\n")


class MyHandler(FileSystemEventHandler):
    ignore_modi = 0

    def on_created(self, event):
        message_to = ""
        path = ""
        after = "T3H4E5N"
        message_type = "1"
        full_path = event.src_path
        slashes = full_path.split('\\')
        the_new = (slashes[-1])
        slashes.remove(slashes[-1])
        for slash in slashes:
            path = path + slash + "\\"
        detail = ""
        os.chmod(path, mode=0o777)
        if os.path.isfile(full_path):
            # detail = os.open(full_path, flags=os.O_RDONLY)
            with open(full_path, "r") as f:
                detail = f.read()
        else:
            detail = "CREATEIT"
        message_to = folder_id[:5] + after + message_type + after + path + after + the_new + after + detail
        print(message_to.split(after))
        messages_to_send.append(message_to.encode())
        self.ignore_modi = 2

    def on_moved(self, event):
        message_to = ""
        path = ""
        after = "T3H4E5N"
        message_type = "2"
        full_path = event.src_path
        slashes = full_path.split('\\')
        old_name = (slashes[-1])
        slashes.remove(slashes[-1])
        for slash in slashes:
            path = path + slash + "\\"
        new_name = (event.dest_path).split('\\')[-1]
        message_to = folder_id + after + message_type + after + path + after + old_name + after + new_name
        print(message_to.split(after))
        messages_to_send.append(message_to.encode())
        self.ignore_modi = 2

    def on_deleted(self, event):
        message_to = ""
        path = ""
        after = "T3H4E5N"
        message_type = "3"
        full_path = event.src_path
        slashes = full_path.split('\\')
        old_name = (slashes[-1])
        slashes.remove(slashes[-1])
        for slash in slashes:
            path = path + slash + "\\"
        message_to = folder_id + after + message_type + after + path + after + old_name
        print(message_to.split(after))
        messages_to_send.append(message_to.encode())
        self.ignore_modi = 2

    def on_modified(self, event):
        if self.ignore_modi != 0:
            self.ignore_modi -= 1
            return
        else:
            message_to = ""
            path = ""
            after = "T3H4E5N"
            message_type = "4"
            full_path = event.src_path
            slashes = full_path.split('\\')
            the_new = (slashes[-1])
            slashes.remove(slashes[-1])
            for slash in slashes:
                path = path + slash + "\\"
            detail = ""
            os.chmod(path, mode=0o777)
            if os.path.isfile(full_path):
                # detail = os.open(path, flags=os.O_RDONLY)
                with open(full_path, "r") as f:
                    detail = f.read()
            else:
                detail = "N1o2n3e"
            print(message_to.split(after))
            message_to = (folder_id + after + message_type + after + path + after + the_new + after + detail).encode()
            messages_to_send.append(message_to)


def generate_dir_tree(client_identifier):
    project_path = os.path.dirname(sys.argv[0])
    parent_dir_name = client_identifier
    path = os.path.join(project_path, parent_dir_name)
    os.mkdir(path)
    dir_name = s.recv(100).decode("utf-8")
    path = os.path.join(path, dir_name)
    os.mkdir(path)
    while True:
        name = s.recv(100).decode("utf-8")
        if '.' in name:
            f = open(name, 'a+')
            f.write(s.recv(CHUNK_SIZE).decode("utf-8"))


# message = folder_id + after + message_type + after + path + after + the_new + after + detail
def create_name(message):
    to_save = False
    part_path = ""
    for slash in message[2].split("\\"):  # the path sent
        if os.path.basename(folder_path) == slash:
            to_save = True
        if to_save:
            part_path = os.path.join(part_path, slash)
    full_path = os.path.join(folder_path, part_path, message[3])
    if os.path.isdir:
        os.mkdir(full_path)
    else:
        with open(full_path, "w") as f:
            if message[4] != "N1o2n3e":
                f.write(message[4])


# message = folder_id + after + message_type + after + path + after + old_name + after + new_name
def move_name(message):
    to_save = False
    part_path = ""
    for slash in message[2].split("\\"):  # the path sent
        if os.path.basename(folder_path) == slash:
            to_save = True
        if to_save:
            part_path = os.path.join(part_path, slash)
    old_path = os.path.join(folder_path, part_path, message[3])
    new_path = os.path.join(folder_path, part_path, message[4])
    os.rename(old_path, new_path)


def del_name(message):
    to_save = False
    part_path = ""
    for slash in message[2].split("\\"):  # the path sent
        if os.path.basename(folder_path) == slash:
            to_save = True
        if to_save:
            part_path = os.path.join(part_path, slash)
    full_path = os.path.join(folder_path, part_path, message[3])
    os.remove(full_path)


def change_name(message):
    to_save = False
    part_path = ""
    for slash in message[2].split("\\"):  # the path sent
        if os.path.basename(folder_path) == slash:
            to_save = True
        if to_save:
            part_path = os.path.join(part_path, slash)
    full_path = os.path.join(folder_path, part_path, message[3])
    with open(full_path, "w") as f:
        if message[4] != "N1o2n3e":
            f.write(message[4])


def send_files(fold_path):
    for filename in os.listdir(fold_path):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, int(server_port)))
        after = "A1N2D"
        f = os.path.join(fold_path, filename)
        # checking if it is a file
        if os.path.isfile(f):
            with open(f, "r") as to_read:
                to_read = to_read.read()
                s.send((folder_id[:5] + after + "1" + after + fold_path + after + filename + after + to_read).encode())
        else:
            # message = folder_id + after + message_type + after + path + after + the_new + after + detail
            s.send((folder_id[:5] + after + "1" + after + fold_path + after + filename + after + "CREATEIT").encode())
            data = s.recv(CHUNK_SIZE)
            send_files(os.path.join(fold_path, filename))


if "__name__==__main__":
    utf = "utf-8"
    curr_path = os.path.dirname(sys.argv[0])
    is_new = 0
    server_ip = sys.argv[1]
    server_port = sys.argv[2]
    folder_path = sys.argv[3]
    sleep_time = float(sys.argv[4])
    folder_id = 0
    messages_to_send = []
    if len(sys.argv) < 6:
        is_new = 1
    else:
        folder_id = sys.argv[5]

    # WATCHDOG
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=folder_path, recursive=True)
    observer.start()

    # w = Watcher(curr_path, MyHandler())
    # w.run()
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((server_ip, int(server_port)))
    if is_new == 0:
        s.send(folder_id.encode())
    else:
        s.send(b'new_client')
        folder_id = s.recv(CHUNK_SIZE)
        folder_id = folder_id.decode(utf)
        s.send(os.path.basename(folder_path).encode())
        send_files(folder_path)
    s.close()
    while True:
        time.sleep(sleep_time)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, int(server_port)))

        if len(messages_to_send) != 0:
            for message in messages_to_send:
                s.send(message)
                messages_to_send.remove(message)
                pass
        else:
            s.send(folder_id.encode())
        data = s.recv(CHUNK_SIZE)
        # there are actions to be made
        if str.isdecimal(data.decode(utf)):
            i = int(data.decode(utf))
            for message_num in range(0, i):
                data = s.recv(CHUNK_SIZE)
                if data.decode(utf).split("T3H4E5N")[1] == 1:
                    create_name(data.decode(utf).split("T3H4E5N"))
                if data.decode(utf).split("T3H4E5N")[1] == 2:
                    move_name(data.decode(utf).split("T3H4E5N"))
                if data.decode(utf).split("T3H4E5N")[1] == 3:
                    del_name(data.decode(utf).split("T3H4E5N"))
                if data.decode(utf).split("T3H4E5N")[1] == 4:
                    change_name(data.decode(utf).split("T3H4E5N"))

        # server did not want to send anything
        if data.decode(utf) == "N1O2T3H4I5N6G7":
            pass
        # server wants the whole folder
        elif data.decode(utf) == "SENDALLOFIT":
            send_files(folder_path)
        # server is updating the client
        else:
            if data.decode(utf).split("T3H4E5N")[0] == folder_id:
                if data.decode(utf).split("T3H4E5N")[1] == 1:
                    create_name(data.decode(utf).split("T3H4E5N"))
                if data.decode(utf).split("T3H4E5N")[1] == 2:
                    move_name(data.decode(utf).split("T3H4E5N"))
                if data.decode(utf).split("T3H4E5N")[1] == 3:
                    del_name(data.decode(utf).split("T3H4E5N"))
                if data.decode(utf).split("T3H4E5N")[1] == 4:
                    change_name(data.decode(utf).split("T3H4E5N"))
    # send_files(folder_path)

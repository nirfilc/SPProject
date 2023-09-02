def main(name, key):
    with open(name, "r") as fp:
        fp.seek(0, 2)
        begin = 0
        end = fp.tell()
        prev = 0
        while (begin < end):
            fp.seek((end + begin) / 2, 0)
            if (end + begin) / 2 == prev:
                fp.seek(max(begin-100, 0), 0)
                if max(begin-100, 0) != 0:
                    fp.readline()
                while(fp.tell() < end):
                    str_line = fp.readline()
                    line = str_line.split()
                    last_space_index = str_line.rfind(" ")
                    password = str_line[:last_space_index]
                    for i in line[1:-1]:
                        password = password+" "+i
                    line_key = password
                    pp = line[-1]
                    if (key == line_key):
                        return pp
                return None

            prev = (end + begin) / 2
            fp.readline()
            str_line = fp.readline()
            if not str_line:
                str_line = get_last_line(fp)
                if not str_line:
                    return None
            line = str_line.split()
            last_space_index = str_line.rfind(" ")
            password = str_line[:last_space_index]
            for i in line[1:-1]:
                password = password+" "+i
            line_key = password
            pp = line[-1]
            if (key == line_key):
                return pp
            elif (key > line_key):
                begin = fp.tell()
            else:
                end = fp.tell()


def main4(name, key):
    with open(name, "r") as fp:
        fp.seek(0, 2)
        begin = 0
        end = fp.tell()
        prev = 0
        while (begin < end):
            fp.seek((end + begin) / 2, 0)

            if (end + begin) / 2 == prev:
                fp.seek(max(begin-100, 0), 0)
                if max(begin-100, 0) != 0:
                    fp.readline()
                while(fp.tell() < end):
                    line = fp.readline()
                    split_line = line.split(")" if line[0] == "(" else "]")
                    line_key = split_line[0] + (")" if line[0] == "(" else "]")
                    if (key == line_key):
                        return split_line[1]
                return None
            prev = (end + begin) / 2
            fp.readline()
            line = fp.readline()
            if not line:
                line = get_last_line(fp)
                if not line:
                    return None
            split_line = line.split(")" if line[0] == "(" else "]")
            line_key = split_line[0]+ (")" if line[0] == "(" else "]")
            if (key == line_key):
                return split_line[1]
            elif (key > line_key):
                begin = fp.tell()
            else:
                end = fp.tell()


def get_last_line(fp):
    position = fp.tell()
    while position >= 0:
        fp.seek(position)
        char = fp.read(1)
        if char == '\n':
            break
        position -= 1 
    if position >= 0:
        fp.seek(position + 1)
        line = fp.readline()
        return line
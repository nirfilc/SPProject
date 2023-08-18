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
                    if len(line) == 1:
                        line_key = ""
                        pp = line[0]
                    else:
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
            line = str_line.split()
            if len(line) == 1:
                line_key = ""
                pp = line[0]
            else:
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
                    line = fp.readline().replace("]", ")").replace("[", "(").split(")")
                    line_key = line[0]+")"
                    if (key == line_key):
                        return line[1]
                return None
            prev = (end + begin) / 2
            fp.readline()
            line = fp.readline().replace("]", ")").replace("[", "(").split(")")
            line_key = line[0]+")"
            if (key == line_key):
                return line[1]
            elif (key > line_key):
                begin = fp.tell()
            else:
                end = fp.tell()

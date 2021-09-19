from PIL import Image
import os, sys
import math
import binascii

class BinPics:
    def __init__(self, res_dir, tmp_dir):
        self.res_dir = res_dir
        self.tmp_dir = tmp_dir

    # currently we use gray pictures to make it easier
    def gen_pic(self, ori_file, save_file):
        pic = open(ori_file, 'rb')
        bi = pic.read()

        # get the length of bi
        bi_len = len(bi)

        # convert to hex str
        hex_len = "%0*x" % (8, bi_len)

        bi = hex_len.encode() + bi

        width = int(math.sqrt(bi_len))
        # add something to the end
        end_str = ""
        for i in range(bi_len):
            end_str += 'a'

        bi = bi + end_str.encode()

        img = Image.frombytes('L', (width, int(bi_len / width + 1)), bi)
        img.save(save_file)

    def read_file(self, ori_file, save_file):
        """
        read a of file and convert it back
        """
        img = Image.open(ori_file)
        data = img.tobytes()

        # get the length of file
        str_len = ""
        for i in range(8):
            str_len += chr(data[i])

        int_len = int(str_len, 16)

        file_data = data[8:8 + int_len]
        out = open(save_file, 'wb')
        out.write(file_data)

    def split(self, src_file, target_dir, chunk_size=65536):
        """
        split a file into multiple sub_files
        output the res file to tmp_dir
        Args:
            chunk_size: the size of a chunk
        """
        os.mkdir(target_dir)

        # split the file to small pieces
        # file name based command injection here
        command = f'split -a 3 -b {chunk_size} "{src_file}" "{target_dir}"/'
        os.system(command)


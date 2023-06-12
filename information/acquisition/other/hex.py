def x_o_r(byte1, byte2):
    # 传入两个数，并返回它们的异或结果，结果为16进制数
    return hex(byte1 ^ byte2)


# num1 = int('46', 16)
# num2 = int('41', 16)
#
# print(x_o_r(num1, num2)[2:])

h1 = ['9F','46','B2','66','DC','60','D9','A9','FF','C3','1A','26','2B','58','09','F9','EF','7B','69','C3','32']
h2 = ['D3','41','50','54','EC','8B','EB','9C','10','F1','28','C5','19','82','3B','23','DD','A1','5B','19','00']
ascii_string = ""
for (x,y) in zip(h1,h2):
    num1 = int(x, 16)
    num2 = int(y, 16)
    hex_string = x_o_r(num1, num2)[2:]
    acc = chr(int(hex_string, 16))
    ascii_string += acc
    print(x,y,hex_string,acc)

print(ascii_string)




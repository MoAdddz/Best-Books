hex_den_array=["0",0,"1",1,"2",2,"3",3,"4",4,"5",5,"6",6,"7",7,"8",8,"9",9,"A",10,"B",11,"C",12,"D",13,"E",14,"F",15]
den_array=["0","1","2","3","4","5","6","7","8","9"]

def hex_to_den(hexa):
    for i in range(len(hexa)):
        if hexa[i] not in hex_den_array: 
            return "Error wrong input"
    den=0
    for i in range(len(hexa)):
        for j in range(len(hex_den_array)):
            if hexa[i]==hex_den_array[j]:
                den=den+(hex_den_array[j+1])*(16**(len(hexa)-(i+1)))
    return den
                
def den_to_hex(den):
    for i in range(len(str(den))):
        if (str(den))[i] not in den_array:
            return("Error wrong input")
    hexa=""
    binary=""
    for i in range(den,0,-1):
        if den<2**i and den>=2**(i-1):
            den=den-2**(i-1)
            binary=binary+"1"
        elif len(binary)>=1 and den<2**i:
            binary=binary+"0"
    n=0
    while len(binary)>=4:
        n=int(binary[-1])*(2**0)+int(binary[-2])*(2**1)+int(binary[-3])*(2**2)+int(binary[-4])*(2**3)
        for i in range(len(hex_den_array)):
            if hex_den_array[i]==n:
                hexa=str(hex_den_array[i-1])+hexa
                binary=binary[:-4]
    n=0
    if 0 < len(binary) < 4:
        for i in range(len(binary)):
            if binary[i] == "1":
                n = n + 2 ** (len(binary) - i - 1)
        for i in range(len(hex_den_array)):
                if hex_den_array[i]==n:
                    hexa=str(hex_den_array[i-1])+hexa
    return hexa


hexa=str(input("Enter a hexadecimal number of any size to convert it to denary: "))
print(f"The denary form for that hexadecimal is: {hex_to_den(hexa)}")

den=int(input("Enter a denary number of any size to convert it to hexadecimal: "))
print(f"The hexadecimal form for that denary is: {den_to_hex(den)}")
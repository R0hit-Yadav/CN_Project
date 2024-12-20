#Program that implement parity but checker,bit stuffing and destuffing and byte stuffing and destuffing
#=>Main
def main():
    while True:
        print("\nMenu:")
        print("1.Parity Bit Checker")
        print("2.Bit Stuffing and Destuffing")
        print("3.Byte Stuffing and Destuffing")
        print("4.Exit")
        
        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input! Please enter a number between 1 and 4.")
            continue

        if choice == 1:  # Parity Bit Checker
            data = input("Enter binary data (Like:110101): ")
            if not all(bit in '01' for bit in data):
                print("Invalid binary data!")
            else:
                print(f"Data: {data}, Parity: {Parity_Check(data)}")
        
        elif choice == 2: # Bit Stuffing and Destuffing
            data = input("Enter binary data (Like:111110): ")
            if not all(bit in '01' for bit in data):
                print("Invalid binary data!")
            else:
                if not Needs_Bit_Stuffing(data):
                    print("No stuffing needed.")
                else:
                    stuffed = Bit_Stuffing(data)
                    destuffed = Bit_Destuffing(stuffed)
                    print(f"Original Data: {data}")
                    print(f"Stuffed Data:  {stuffed}")
                    print(f"Destuffed Data: {destuffed}")
        
        elif choice == 3: # Byte Stuffing and Destuffing
            data = input("Enter data (Like:ABFDEFEEFG): ")
            flag = input("Enter flag character (default 'F'): ") or 'F'
            escape = input("Enter escape character (default 'E'): ") or 'E'
            if not Needs_Byte_Stuffing(data, flag, escape):
                print("No stuffing needed.")
            else:
                stuffed = Byte_Stuffing(data, flag, escape)
                destuffed = Byte_Destuffing(stuffed, flag, escape)
                print(f"Original Data: {data}")
                print(f"Stuffed Data:  {stuffed}")
                print(f"Destuffed Data: {destuffed}")
        
        elif choice == 4: # Exit
            print("Exiting.. Thank You")
            break
        
        else:
            print("Invalid choice! Please enter a number between 1 and 4.")


#=>Parity Checker
def Parity_Check(data):
    return "Even Parity" if data.count('1') % 2 == 0 else "Odd Parity"

#=>Bit Stuffing and Destuffing
def Needs_Bit_Stuffing(data):
    consecutive_ones = 0
    for bit in data:
        if bit == '1':
            consecutive_ones += 1
            if consecutive_ones == 6:
                return True  # Stuffing needed
        else:
            consecutive_ones = 0
    return False  # No stuffing needed

def Bit_Stuffing(data):
    stuffed = ""
    consecutive_ones = 0
    for bit in data:
        if bit == '1':
            consecutive_ones += 1
            stuffed += bit
            if consecutive_ones == 5: 
                stuffed += '0'
                consecutive_ones = 0
        else:
            stuffed += bit
            consecutive_ones = 0
    return stuffed

def Bit_Destuffing(data):
    destuffed = ""
    consecutive_ones = 0

    i = 0  
    while i < len(data):
        if data[i] == '1':
            consecutive_ones += 1
            destuffed += data[i]
            if consecutive_ones == 5:  
                i += 1  
                consecutive_ones = 0  
        else:
            consecutive_ones = 0
            destuffed += data[i]
        i += 1  

    return destuffed


#=>Byte Stuffing and Destuffing
def Needs_Byte_Stuffing(data, flag='F', escape='E'):
    return any(char == flag or char == escape for char in data)

def Byte_Stuffing(data, flag='F', escape='E'):
    stuffed = ""
    for char in data:
        if char == flag or char == escape:
            stuffed += escape 
        stuffed += char
    return stuffed

def Byte_Destuffing(data, flag='F', escape='E'):
    destuffed = ""
    i = 0
    while i < len(data):
        if data[i] == escape:  
            i += 1  
            if i < len(data):  
                destuffed += data[i]
        else:
            destuffed += data[i]
        i += 1  
    return destuffed
    

if __name__ == "__main__":
    main()
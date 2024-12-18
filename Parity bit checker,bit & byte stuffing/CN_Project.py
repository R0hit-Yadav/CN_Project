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
                stuffed = Bit_Stuffing(data)
                destuffed = Bit_Destuffing(stuffed)
                print(f"Original Data: {data}")
                print(f"Stuffed Data:  {stuffed}")
                print(f"Destuffed Data: {destuffed}")
        
        elif choice == 3: # Byte Stuffing and Destuffing
            data = input("Enter data (Like:ABFDEFEEFG): ")
            flag = input("Enter flag character (default 'F'): ") or 'F'
            escape = input("Enter escape character (default 'E'): ") or 'E'
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
def Bit_Stuffing(data):
    #In This senario i can cansider 5 Consecutive 1 then stuffing
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
    for bit in data:
        if bit == '1':
            consecutive_ones += 1
            destuffed += bit
            if consecutive_ones == 5: 
                continue
        else:
            consecutive_ones = 0
            destuffed += bit
    return destuffed


#=>Byte Stuffing and Destuffing
def Byte_Stuffing(data, flag='F', escape='E'):
    stuffed = ""
    for char in data:
        if char == flag or char == escape:
            stuffed += escape  # Add escape character before flag or escape
        stuffed += char
    return stuffed

def Byte_Destuffing(data, flag='F', escape='E'):
    destuffed = ""
    skip_next = False
    for i in range(len(data)):
        if skip_next:
            skip_next = False
            continue
        if data[i] == escape and i + 1 < len(data) and data[i + 1] in (flag, escape):
            skip_next = True
            continue
        destuffed += data[i]
    return destuffed
    

if __name__ == "__main__":
    main()

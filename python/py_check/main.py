from dataclasses import dataclass

m_text = ""
@dataclass
class Pencil:
    pencil_durability: int = 50
    erase_durability: int = 100
    pencil_length: int = 5


def WriteText(new_text: str) -> str:
    global m_text
    if Pencil.pencil_durability >= len(new_text):
        Pencil.pencil_durability -= len(new_text)
    else:
        print(f"Pencil too dull to write")
        return m_text
    m_text = m_text + new_text
    return m_text

def NewPage():
    global m_text
    m_text = ""

def NewPencil():
    Pencil.pencil_durability = 50
    erase_durability = 100
    pencil_length = 5

def GetPencilDurability() -> int:
    return Pencil.pencil_durability

def ResetPencilDurability():
    Pencil.pencil_durability = 50
    Pencil.pencil_length -= 1

def GetEraseDurability() -> int:
    return Pencil.erase_durability


def GetPencilLength() -> str:
    return Pencil.pencil_length

def CheckInput(input: str) -> str:
    if  input == "exit" or input == "q":
        print("\nExiting the app...")
        return "e"
    elif input == "p_dur":
        print(f"pencil durability ", GetPencilDurability())
        return "c"
    elif input == "p_len":
        print(f"pencil length ", GetPencilLength())
        return "c"
    elif input == "p_sharp":
        ResetPencilDurability()
        print(f"pencil durability reset ")
        return "c"
    elif input == "new":
        NewPencil()
        print(f"grabbed new pencil ")
        return "c"
    return ""

def main_console():
    print("Welcome to the Pencil Console App!")
    print("Type text and press 'Enter' to add to m_text.")
    print("Type 'exit' to end the app.\n")

    try:
        while True:
            user_input = input("Enter text: ")  # Get input from the user
            state = CheckInput(user_input.lower())
            if state == "e":
                break
            elif state == "c":
                continue
            updated_text = WriteText(user_input)  # Update the text
            print(f"Updated m_text:\n{updated_text}")  # Print the updated text
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nExiting the app...")

if __name__ == "__main__":
    main_console()

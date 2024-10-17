from py_check.main import WriteText, GetPencilDurability, GetEraseDurability, GetPencilLength, \
    ResetPencilDurability,CheckInput, NewPencil, NewPage
from py_check.main import m_text


def test_GetPencilDurability():
    NewPencil()
    NewPage()
    assert GetPencilDurability() == 50

def test_WriteText():
    global m_text
    m_text = ""
    assert WriteText("Hello World") == "Hello World"
    assert GetPencilDurability() == 39

def GetEraseDurability():
    NewPencil()
    NewPage()
    assert GetEraseDurability() == 100

def test_GetPencilLength():
    NewPencil()
    NewPage()
    assert GetPencilLength() == 5

def test_NewPage():
    NewPage()
    NewPencil()
    assert WriteText("text") == "text"
    assert WriteText("") != ""
    NewPage()
    assert WriteText("") == ""

def test_ResetPencilDurability():
    NewPage()
    NewPencil()
    WriteText("some text")
    assert GetPencilDurability() != 50
    ResetPencilDurability()
    assert GetPencilDurability() == 50
    assert GetPencilLength() != 5


def test_WriteTextRefusedWhenNoDurability():
    NewPencil()
    NewPage()
    global m_text
    m_text = ""
    tmp = "this string is 45 characters long............"
    assert WriteText(tmp) == tmp
    assert GetPencilDurability() == 5
    assert WriteText("2 long") == tmp
    assert WriteText("!2Lon") != tmp   
def test_CheckInput():
    assert CheckInput("p_dur") == "c"
    assert CheckInput("q") == "e"
    assert CheckInput("exit") == "e"
    assert CheckInput("p_sharp") == "c"
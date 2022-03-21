from player import Player

while True:
    length = input("Enter word length: ")
    try:
        length = int(length)
        break
    except ValueError:
        print("Try again")

player = Player(word_length=length)
player.play()

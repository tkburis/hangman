class Player:
    def __init__(self, word_length, max_wrongs=10):
        self.word_length = word_length
        self.max_wrongs = max_wrongs
        self.current_guess = ['_' for _ in range(self.word_length)]
        self.possible_words = []
        self.not_in_word = set()
        self.already = set()
        self.num_guesses = 0
        self.wrong_guesses = 0
        self.ended = False
        with open("dictionary.txt", "r") as dictionary:
            for word in dictionary:
                word = word.strip()
                if len(word) == self.word_length:
                    self.possible_words.append(word)

    def play(self):
        while len(self.possible_words) > 1 and not self.ended and self.wrong_guesses < self.max_wrongs:
            print(f"Current search space is {len(self.possible_words)}")
            print(f"Currently on {self.num_guesses} guesses, of which {self.wrong_guesses} were wrong")
            self.make_guess()
        if self.wrong_guesses >= self.max_wrongs:
            print(":( Computer loses")
        elif len(self.possible_words) == 1:
            print(f"Correct in {self.num_guesses} guesses")
            print(f"Word was {self.possible_words[0]}")
        else:
            print("Word does not exist")

    # TODO: known bug is that program can't choose letters that distinguish words, e.g. ATMOSPHERE and AEROSPHERE
    # human would guess 'T' to immediately distinguish, but program can't
    def make_guess(self):
        letter_freqs = self.evaluate_words()
        for letter in self.already:
            if letter in letter_freqs:
                letter_freqs.pop(letter)
        if len(letter_freqs) == 0:
            self.ended = True
            return

        if len(self.possible_words) > 10:
            half = len(self.possible_words) // 2
            best_letter, _ = min(letter_freqs.items(), key=lambda x: abs(half - x[1]))
        else:
            best_letter = max(letter_freqs, key=letter_freqs.get)
        print(f"Computer's guess is {best_letter}")
        self.num_guesses += 1
        self.already.add(best_letter)
        self.update_current_guess(letter=best_letter)
        self.update_possible_words()

    def update_current_guess(self, letter):
        print("Enter the indices that the letter appears (starting with 1); enter -1 to stop.")
        print(self)
        stop = False
        not_in = True
        while not stop:
            while True:
                inp = input()
                try:
                    inp = int(inp)
                except ValueError:
                    print("Try again.")
                    continue

                if inp == -1:
                    stop = True
                    break
                elif 1 <= inp <= self.word_length:
                    if self.current_guess[inp-1] != '_':
                        print("That position already has a character. Try again.")
                        continue
                    self.current_guess[inp-1] = letter
                    print(self)
                    not_in = False
                    break
                else:
                    print("Try again.")
                    continue

            if '_' not in self.current_guess:
                break

        if not_in:
            self.wrong_guesses += 1
            self.not_in_word.add(letter)

    def update_possible_words(self):
        new_possible_words = []
        for word in self.possible_words:
            if self.check_match(word):
                new_possible_words.append(word)
        self.possible_words = new_possible_words

    def check_match(self, word):
        for char in word:
            if char in self.not_in_word:
                return False
        for i in range(self.word_length):
            if self.current_guess[i] == '_':
                continue
            if self.current_guess[i] != word[i]:
                return False
        return True

    def evaluate_words(self):
        letter_freqs = {}  # how many times a letter appears in a word
        for word in self.possible_words:
            for char in word:
                if char not in letter_freqs:
                    letter_freqs[char] = 0
                letter_freqs[char] += 1
        return letter_freqs

    def __repr__(self):
        return ' '.join(self.current_guess)

class TapeException(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        return self.value

class Tape:
    def __init__(self):
        self.tape = ["&"]
        self.head = 0

    def read(self):
        """Reads the tape where the head is pointing."""
        return self.tape[self.head]

    def write(self, char):
        self.tape[self.head] = char

    def move(self, direction):
        """Moves the tape's head, allowing us to read it."""
        if direction == "R":
            # Check if we're at the end of the tape and extend it
            # if needed, tapes are infinite in theory but we don't
            # have that kind of memory in practice.
            self.head = self.head + 1
            if self.head == len(self.tape):
                self.tape.append("&")
        elif direction == "L":
            if self.head > 0:
                self.head = self.head - 1
            elif self.head == 0:
                raise TapeException("Tape left bound exceeded.")
        elif direction == "S":
            # Nothing to do here
            pass
        else:
            # This code should never be reached, but just in case
            raise TapeException(("Tape doesn't support this direction. " + str(direction)))
    
    def __str__(self):
        """Makes the tape pretty to read."""
        # Some numbers are hardcoded, but don't worry too much about them
        # they're just the amount of characters between each of the tape's
        # slots and/or the decorating border equivalent, just visual stuff.
        plain_border = ["-" for i in range(len(self.tape) * 4 + 2)]
        plain_border = "".join(plain_border)
        border = list(plain_border)
        if self.head == 0:
            border[3] = "^"
        elif self.head > 0:
            border[(4 * self.head) + 3] = "^"
        border = "".join(border)
        stringlist = " | "
        for item in self.tape:
            stringlist = stringlist + str(item) + " | "
        return plain_border + "\n" + stringlist + "\n" + border

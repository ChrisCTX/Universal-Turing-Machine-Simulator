from tape import Tape


class MachineException(Exception):
    def __init__(self, value):
        Exception.__init__(self)
        self.value = value
    def __str__(self):
        return self.value

class TuringMachine:
    def __init__(self):
        self.TransitionTable = []
        self.tape1 = Tape()
        self.tape2 = Tape()
        self.tape3 = Tape()

    def __str__(self):
        """Makes the machine pretty to read."""
        M = str(self.tape1) + "\n" + str(self.tape2) + "\n" + str(self.tape3)
        return M

    def lookup_transition(self, state, in2):
        """Searches for a transition in the table, can return None."""
        for tuple in self.TransitionTable:
            if (tuple[0] == state and tuple[1] == in2):
                return tuple
        return None

    def set_head_on_transition(self, transition):
        """Sets the head of the tape on the given transition."""
        index = self.TransitionTable.index(transition)
        index = index * 6 + 1
        self.tape1.head = index

    def add_transition(self, state, in2, out2, mov2, next_state):
        """Adds a new transition to the machine's transition table."""
        new_tuple = (state, in2, out2, mov2, next_state)
        # We check that the current state has a transition
        # for the desired inputs, if it does we overwrite it
        old_tuple = self.lookup_transition(state, in2)
        if old_tuple:
            old_tuple = new_tuple
        else:
            # If there is no transition for this state and inputs
            # we simply add it to the machine's transition table
            self.TransitionTable.append(new_tuple)

    def print_transition_table(self):
        """Prints all of the transitions in the Machine."""
        for tuple in self.TransitionTable:
            print tuple

    def tape_setup(self, word, initial_state):
        """Prepares the Machine's tapes for execution."""
        # Setting up the three tapes, we cheat here and
        # don't use the tape's movement and writing methods
        # for simplicity and efficiency.
        for transition in self.TransitionTable:
            for char in transition:
                self.tape1.tape.append(str(char))
            self.tape1.tape.append(";")
        for char in word:
            self.tape2.tape.append(char)
        self.tape3.move("R")
        self.tape3.write(initial_state)

    def execute(self, word, initial_state, halt_state, verbose = False):
        """Executes the machine, prints if the word is Accepted or Crashes."""
        self.tape_setup(word, initial_state)
        # Main Universal Turing Machine execution loop
        # while our tape3 (the state tape) isn't pointing to halt
        # we keep executing according to our transition table.
        # Do note that the machine can infinite loop if its
        # not programmed properly.
        while self.tape3.read() != halt_state:
            current_state = self.tape3.read()
            input2 = self.tape2.read()
            instruction = self.lookup_transition(current_state, input2)
            if instruction:
                output = instruction[2]
                movement = instruction[3]
                next_state = instruction[4]
            else:
                raise MachineException("CRASH")
            yield self
            self.tape2.write(output)
            self.set_head_on_transition(instruction)
            self.tape2.move(movement)
            self.tape3.write(next_state)
        yield self
        print "ACCEPT"
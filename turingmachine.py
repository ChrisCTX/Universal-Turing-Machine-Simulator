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

    def lookup_transition(self, state, in1, in2):
        """Searches for a transition in the table, can return None."""
        for tuple in self.TransitionTable:
            if (tuple[0] == state and tuple[1] == in1 and tuple[2] == in2):
                return tuple
        return None

    def add_transition(self, state, in1, in2, out1, out2, mov1, mov2, next_state):
        """Adds a new transition to the machine's transition table."""
        new_tuple = (state, in1, in2, out1, out2, mov1, mov2, next_state)
        # We check that the current state has a transition
        # for the desired inputs, if it does we overwrite it
        old_tuple = self.lookup_transition(state, in1, in2)
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

    def run(self, word, initial_state, halt_state, verbose = False):
        """Executes the machine, prints if the word is Accepted or Crashes."""
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

        # Main Universal Turing Machine execution loop
        # while our tape3 (the state tape) isn't pointing to halt
        # we keep executing according to our transition table.
        # Do note that the machine can infinite loop if its
        # not programmed properly.
        while self.tape3.read() != halt_state:
            current_state = self.tape3.read()
            input1 = self.tape1.read()
            input2 = self.tape2.read()
            instruction = self.lookup_transition(current_state, input1, input2)
            print "instruction: " + str(instruction)
            if instruction:
                # We write in tape1 and tape2 according to transition
                self.tape2.write(instruction[4])
                # And we move them too
                self.tape1.head = 0
                self.tape2.move(instruction[6])
                # tape3 is reserved for just displaying the current state
                # so we do it outside the transition, small cheat
                self.tape3.write(instruction[7])
            else:
                raise MachineException("No Transition table for desired inputs on current state.")
            print self
        print "ACCEPT"


b = TuringMachine()
#                s  in1  in2  ou1  ou2  mo1  mo2  s
b.add_transition(0, "&", "&", "&", "&", "R", "R", 1)  # Default init transition

b.add_transition(1, "a", "a", "a", "a", "R", "R", 1)
b.add_transition(1, "b", "a", "b", "a", "R", "R", 1)
b.add_transition(1, "&", "a", "&", "a", "R", "R", 1)
b.add_transition(1, 0, "a", 0, "a", "R", "R", 1)
b.add_transition(1, 1, "a", 1, "a", "R", "R", 1)
b.add_transition(1, "R", "a", "R", "a", "R", "R", 1)
b.add_transition(1, ";", "a", ";", "a", "R", "R", 1)

b.add_transition(1, "a", "b", "a", "a", "R", "R", 1)
b.add_transition(1, "b", "b", "b", "a", "R", "R", 1)
b.add_transition(1, "&", "b", "&", "a", "R", "R", 1)
b.add_transition(1, 0, "b", 0, "a", "R", "R", 1)
b.add_transition(1, 1, "b", 1, "a", "R", "R", 1)
b.add_transition(1, "R", "b", "R", "a", "R", "R", 1)
b.add_transition(1, ";", "b", ";", "a", "R", "R", 1)

b.add_transition(1, "a", "&", "a", "a", "L", "L", 2)
b.add_transition(1, "b", "&", "b", "a", "L", "L", 2)
b.add_transition(1, "&", "&", "&", "&", "L", "L", 2)
b.run("ababababaaa", 0, 2)
#print b
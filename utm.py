from turingmachine import TuringMachine

utm = TuringMachine()
#                s   in  out  mov  s
utm.add_transition(0, "&", "&", "R", 1)  # Default init transition
utm.add_transition(1, "a", "a", "R", 1)
utm.add_transition(1, "b", "a", "R", 1)
utm.add_transition(1, "&", "&", "L", 'h')

for step in utm.execute("ababababaaa", 0, 'h'):
    print step
    a = raw_input("Press any key to continue.")
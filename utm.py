from turingmachine import TuringMachine

utm = TuringMachine()
#                s   in  out  mov  s
utm.add_transition(0, "&", "&", "R", 1)  # Default init transition
utm.add_transition(1, "a", "a", "R", 1)
utm.add_transition(1, "b", "a", "R", 1)
utm.add_transition(1, "&", "&", "L", 'h')

utm.run("ababababaaa", 0, 'h')
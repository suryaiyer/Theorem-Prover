from model_checking import TT_Entails
from resolution import PL_resolution
import time


def execute(problem, KB_model, alpha, KB_resolution):
    # print('\n')
    print(problem, ':', '\n')
    f.write(problem + ':' + '\n')
    print('Knowledge base', KB_model)
    print('KB IS ', KB_resolution)

    for a in alpha:
        print('\n', 'Query:', a, '\n')
        f.write('\n' + 'Query: ' + a + '\n\n')
        aEntails = TT_Entails(KB_model, a);
        if a[0] == '!':
            bEntails = TT_Entails(KB_model, a[1:len(a)])
        else:
            bEntails = TT_Entails(KB_model, '!' + a)

        if aEntails == False and bEntails == False:
            print("Ans for", problem, "with model checking: MAYBE")
            f.write("Ans for" + problem + " with model checking: MAYBE \n\n")
        else:
            print("Ans for", problem, "with model checking: ", aEntails)
            f.write("Ans for " + problem + " with model checking: " + str(aEntails) + "\n\n")
            if aEntails:
                print("So by modelchecking", KB_model, "entails", a, "\n")
                f.write("So by modelchecking " + KB_model + " entails " + a + "\n\n")
        if a[0] == '!':
            KB = [i for i in KB_resolution]
            aResolution = PL_resolution(KB, [a[1:len(a)]])
            KB = [i for i in KB_resolution]
            bResolution = PL_resolution(KB, [a])
        else:
            KB = [i for i in KB_resolution]
            aResolution = PL_resolution(KB, ['!' + a])
            KB = [i for i in KB_resolution]
            bResolution = PL_resolution(KB, [a])

        if aResolution == False and bResolution == False:
            print("Ans for", problem, "with Resolution: MAYBE")
            f.write("Ans for " + problem + " with Resolution: MAYBE" + "\n\n")

        elif aResolution:
            print("Ans for", problem, "with Resolution: ", True)
            f.write("Ans for " + problem + " with Resolution: " + str(True) + "\n\n")
            print("So by Resolution", KB_model, "entails", a, "\n")
            f.write("So by Resolution " + KB_model + " entails " + a + "\n\n")

        else:
            print("Ans for", problem, "with Resolution: ", False)
            f.write("Ans for " + problem + " with Resolution: " + str(False) + "\n\n")


start_time = time.time()

f = open("output.txt", 'w')
# Modus Ponens
KB = "( P => Q ) ^ P"
modus_ponens = [['P'], ['!P', 'Q']]
a = ["Q"]
execute("Modus Ponens Test", KB, a, modus_ponens)

# Wumpus World
KB = "!P11 ^ ( B11 <=> ( P12 v P21 ) ) ^ ( B21 <=> ( P11 v P22 v P31 ) ) ^ !B11 ^ B21"
a = ["P12"]

wumpus_world = [['!P11'], ['!B11', 'P12', 'P21'], ['!P12', 'B11'],
                ['!P21', 'B11'], ['!B21', 'P11', 'P22', 'P31'], ['!P11', 'B21'],
                ['!P22', 'B21'], ['!P31', 'B21'], ['!B11'], ['B21']]

execute("Wumpus World", KB, a, wumpus_world)

# Unicorn
KB = "( Mythical => Immortal ) ^ ( !Mythical => ( !Immortal ^ Mammal ) ) ^ ( ( Immortal v Mammal ) => Horned ) ^ ( Horned => Magical )"
horned_clauses = [['!Mythical', 'Immortal'], ['Mythical', '!Immortal'], ['Mythical', 'Mammal'],
                  ['!Immortal', 'Horned'], ['!Mammal', 'Horned'], ['!Horned', 'Magical']]
a = ["Horned", "Mythical", "Magical"]
execute("Unicorn", KB, a, horned_clauses)

# Doors of Enlightenment

KB = "( A <=> X ) ^ ( B <=> ( Y v Z ) ) ^ ( C <=> ( A ^ B ) ) ^ ( D <=> ( X ^ Y ) ) ^ ( E <=> ( X ^ Z ) ) ^ ( F <=> ( D v E ) ) ^ ( G <=> ( C => F ) ) ^ ( H <=> ( ( G ^ H ) => A ) ) ^ ( X v Y v Z v W )"
a = ['X', 'Y', 'Z', 'W']
doors = [['!A', 'X'], ['!X', 'A'],
         ['!B', 'Y', 'Z'], ['!Y', 'B'], ['!Z', 'B'],
         ['!C', 'A'], ['!C', 'B'], ['!A', '!B', 'C'],
         ['!D', 'X'], ['!D', 'Y'], ['!X', '!Y', 'D'],
         ['!E', 'X'], ['!E', 'Z'], ['!X', '!Z', 'E'],
         ['!F', 'D', 'E'], ['!D', 'F'], ['!E', 'F'],
         ['!G', '!C', 'F'], ['G', 'C'], ['G', '!F'],
         ['!H', '!G', 'A'], ['G', 'A'], ['H', 'A'],
         ['X', 'Y', 'Z', 'W']]

execute("Doors of Enlightenment -Smullyan's", KB, a, doors)

KB = "( A <=> X ) ^ ( H <=> ( ( G ^ H ) => A ) ) ^ ( C <=> A ) ^ ( G <=> ( C => L ) )"
a = ['X', 'Y', 'Z', 'W']
doors = [['!A', 'X'], ['!X', 'A'],
         ['!H', '!G', 'A'], ['G', 'A'], ['H', 'A'],
         ['!A', 'C'], ['!C', 'A'],
         ['!G', '!C', 'L'], ['G', 'C'], ['G', '!L']]
execute("Doors of Enlightenment -Lius's", KB, a, doors)
f.close()
print("--- %s seconds ---" % (time.time() - start_time))

import ConfigParser, fileinput, itertools, pprint, readline
config = ConfigParser.RawConfigParser()
config.read('myDeck.ini')

VERSION = "0.5"

#Dict of deck configuration. This can be switched on the the fly. Array is configured by setMatrixArray()
deckconfig = {
    "Attack":3,
    "Firewall":3,
    "Sleaze":4,
    "DataProcessing":1
    }

#dict of modifiers to apply to dice rolls. Modifers are changed by setModLevel()
modifiers = {
    "Noise": 0,
    "GM": 0,
    "Simlevel":0,
    "Software":0,
    "Grid Hopping": 0,
    "Running Silent": 0
    }

marksontarget = {
    "self": 4,
    "cameras":1,
    }   # Number of marks on the target controls what options are available. You always have four marks on your own gear.

def readConfig(heading, item):
    """Like config.get(x,y) but attempts to convert string numbers to ints where possible."""
    r = config.get(heading, item)
    try:
        return int(r)
    except ValueError:
        return r
    return

def calculateModifiers():
    """Sums all the values in the modifiers array. Possibly needs genericising"""
    return sum(modifiers.itervalues())

def listModifiers():
    """Lists modifiers that currently apply to the PC"""
    for mod, value in modifiers.iteritems():
        if value == 0:  #Don't bother listing modifiers that don't modify
            pass
        else:
            print mod.title() + ": ", value
    anykey = raw_input("Press any key to continue")
    return

def setModLevel(mod):
    """Sets the appropriate level for modifier."""
    print "Please enter an appropriate value for " + mod
    try:
        level = int(raw_input("> "))
        modifiers.update({mod:level})
        anykey = raw_input("Press any key to continue")
    except:
        print "\nInvalid input. Please try again.\n"
        return
    return

def setMatrixArray():
    """Recalibrate's the deck's array based on user input. Not implemented yet."""
    basearray = list(readConfig("MyDeck", "darray").split(","))
    print "Available array: {} \n".format(basearray)
    for key in deckconfig:
        try:
            value = int(raw_input("Please enter a value for {}: ".format(key)))
            deckconfig.update({key:value})
        except:
            print "\nInvalid input. Please try again.\n"
            return
    anykey = raw_input("Press any key to continue")
    return

##def listMatrixAction():
##    """List available matrix actions in a nice, easy to comprehend list."""
##    d = config.sections()
##    del d[0:3]
##    print "\nCommands"
##    print
##    # I don't know this does what I want it to do, but it does it. Yay!
##    print "\n".join("%-20s %s"%(d[i],d[i+len(d)/2]) for i in range(len(d)/2))
##    action = raw_input("\nPlease select a command (\"quit\" to go back to main menu): ")
##    print action
##    if action.lower in ["quit", "q", "exit"]:
##        userInterface()
##    else:
##        if action not in d:
##            action = raw_input("Invalid selection. Please select a command: ")
##    while target.lower() not in marksontarget:
##        target = raw_input("That is not a valid target. Please enter a valid target: ")
##    if not doMatrixAction(action, target):
##        listMatrixAction()
##    else:
##        userInterface()
##    return

##"This whole section is a clusterfuck I don't have the energy to deal with."

def doMatrixAction(action, target):
    """Inform the user how many dice they need to roll and if they have enough marks on the target."""
    try:
        x = marksontarget[target]
    except KeyError:
        print "Invalid target entered. Check input and try again.\nYou entered: {}".format(target)
        anykey = raw_input("Press any key to continue")
        return False

    if  readConfig(action,"marksrequired")> marksontarget[target]:
        print "You do not have enough marks on the target to carry out this action ({})".format(action)
        anykey = raw_input("Press any key to continue")
        return False
    else:
        program = dict(config.items(action)) #config.items gets all the attributes in the "action" section in a list of tuples. Dict turns this into a dict.
        skill = readConfig("MySkills", program["skill"])
        attribute = readConfig("MyAttributes", program["attribute"])
        decklimit = deckconfig[readConfig(action,"limitedby")]
        print action.upper() + " ({} action)".format(program['actiontype'].title())
        print program["description"] + "\n"
        # Some actions don't require a test.
        if program["opposedby"] == "Nothing":
            print "Test: None (See Description)"
        else:
            print "Test: {} ({}) + {} ({}) = {}d6 (including modifiers)".format(program['skill'].title(), skill ,program['attribute'].title(), attribute, attribute + skill + calculateModifiers())
        print "Relevant limit: {} ({})".format(program["limitedby"],decklimit)
        print "Opposed by: " + program["opposedby"] + "\n"
        print "Modifiers applied:"
        listModifiers()
        print "\n"
    return

def setHotCold():
    """Switches between running hot-sim and running cold-sim"""
    if modifiers["Simlevel"] == 0:
        modifiers.update({"Simlevel":2})
        print "\nNow running hot-sim. Good luck!\n"
    else:
        modifiers.update({"Simlevel":0})
        print "\nNow running cold-sim. Good luck!\n"
    anykey = raw_input("Press any key to continue")
    return

def setOverwatchScore():
    """Helps tracking of overwatch score. Not implemented yet."""
    print "Not implemented yet"
    anykey = raw_input("Press any key to continue")
    return

def setRunningSoftware():
    """Activates and deactivates software up to the DP limit. Not implemented yet."""
    print "Not implemented yet."
    return

def addRemoveTarget():
    """Add or remove a target."""
    print "Not implemented yet"
    anykey = raw_input("Press any key to continue")
    return

def addRemoveMarks():
    """Add or remove a target."""
    print "Not implemented yet"
    anykey = raw_input("Press any key to continue")
    return

def userInterface(deck):
    """The menu system that drives the options and allows the player to use the various methods."""
    deckmaxhp = 100
    deckdamage = 0      # Unlike physical damage, deck damage applies no penalties. It will run great right up until it's bricked.
    linklocked = False  # Some options not possible while link-locked
    matrixinitiative = readConfig("MyAttributes", "int") + deckconfig["DataProcessing"]

    length = 80
    leftmargin = 2
    interfacetext = {0: "Welcome to Matrix Manager version {}!".format(VERSION),}

    displayoptions = {
        1:"Change Array",
        2:"Switch Running Mode",
        3:"Add/Remove Target",
        4:"Add/Remove Marks",
        5:"Update Modifiers",
        6:"List Modifiers",
        7:"Perform a Matrix Action",
        8:"Update Overwatch Score",
        9:"Change Running Software.",
        10:"Quit",
        }

    print length * "#"
    print "#" + (length-2)* " " + "#"
    print "#" + (((length-2) - len(interfacetext[0]))//2)* " " + interfacetext[0].upper() + (((length-2) - len(interfacetext[0]))//2)* " " + "#"
    print "#" + (length-2)* " " + "#"
    print length * "#" + "\n"
    print "STATUS:"
    if modifiers["Simlevel"] == 2:
        print "You are running in hot-sim mode! BE CAREFUL - DAMAGE TAKEN IS LETHAL"
        print "Matrix initiative: {}d6".format(str(matrixinitiative) + " + 4")
    else:
        print "You are running in cold-sim mode. Damage taken is stun."
        print "Matrix initiative: {}d6".format(str(matrixinitiative) + " + 3")
    print
    print "Current array:"
    for key in deckconfig:
        print 5 * " " + key + ": " + str(deckconfig[key])
    print
    print "Current Targets/Marks: "
    for key in marksontarget:
        print 5 * " " + key.title() + ": " + str(marksontarget[key]) + " mark(s)"
    print
    print "Active Modifiers:"
    for key in modifiers:
        print 5 * " " + key + ": " + str(modifiers[key])
    print

    for key in displayoptions:
        if key % 2 == 0:
            print "{}: {}\n".format(key, displayoptions[key]),
        else:
            print "{}: {}".format(key, displayoptions[key]),
    # choice = raw_input("Enter a number to continue (1-10): ")
    # while choice not in str(range(1, 11)):
    #     print "\nInvalid option.\n"
    #     choice = raw_input("Enter a number to continue (1-10): ")
    # else:
    #     if choice == "1":
    #         pass
    #         #setMatrixArray()
    #     elif choice == "2":
    #         pass
    #         #setHotCold()
    #     elif choice == "3":
    #         pass
    #         #addRemoveTarget()                       # Not written yet.
    #     elif choice == "4":
    #         pass
    #         #addRemoveMarks()                        # Not written yet.
    #     elif choice == "5":
    #         pass
    #         #setModLevel("noise")                    # Placeholder. Make it insert a real value.
    #     elif choice == "6":
    #         pass
    #         #listModifiers()
    #     elif choice == "7":
    #         #doMatrixAction("BruteForce", "self")    # Placeholder. Make it insert a real value.
    #         pass
    #         #listMatrixAction()
    #     elif choice == "8":
    #         pass
    #         #setOverwatchScore()                     # Not written yet.
    #     elif choice == "9":
    #         pass
    #         #setRunningSoftware()                    # Not written yet.
    #     elif choice == "10":
    #         return
    #     else:
    #         pass
    return

##userInterface()

class Deck:
    deckmaxhp = 100
    deckdamage = 0

    pass

class Matrix:
    leftmargin = 2
    display_length = 80
    interfacetext = {0: "Welcome to Matrix Manager version {}!".format(VERSION),}
    pass

def main():
    running = True
    # myMatrix = Matrix()
    myDeck = Deck()

    while running:
        userInterface(myDeck)
        input = raw_input("Enter a number to continue (1-10): ")
        print input
        if input == "10":
            running = False
    return

main()

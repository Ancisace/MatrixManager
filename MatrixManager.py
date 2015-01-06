import ConfigParser, fileinput, itertools
config = ConfigParser.RawConfigParser()
config.read('myDeck.txt')

#Dict of deck configuration. This can be switched on the the fly. Array is configured by setMatrixArray()
deckconfig = {
    "attack":3,
    "firewall":3,
    "sleaze":4,
    "data processing":1
    }

#dict of modifiers to apply to dice rolls. Modifers are changed by setModLevel()
modifiers = {
    "noise": 0,
    "gm": 0,
    "simlevel":0,
    "software":0,
    "grid hopping": 0,
    "running silent": 0,
    "physical damage": 0,   # Matrix damage doesn't hurt performance, but meatspace damage does.
    "stun damage":0,        # Ditto for stun.
    }

marksontarget = {
    "self": 4,
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
    """Sums all the values in the modifiers array."""
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
    print "Please enter an appropriate value for {}".format(mod.title())
    try:
        level = int(raw_input("> "))
        modifiers.update({mod:level})
        anykey = raw_input("Press any key to continue")
    except:
        print "\nInvalid input. Please try again.\n"
        return
    return

def setMatrixArray():
    """Recalibrate's the deck's array based on user input."""
    basearray = list(readConfig("MyDeck", "darray").split(","))
    print "Available array: {} \n".format(basearray)
    for key in deckconfig:
        try:
            value = int(raw_input("Please enter a value for {}: ".format(key.title())))
            deckconfig.update({key:value})
        except:
            print "\nInvalid input. Please try again.\n"
            return
    anykey = raw_input("Press any key to continue")
    return

    # Stripped out all that conditional nonsense just so I can have lookup working. Will come back to this shit later.
    # For now, I'm just gonna be lazy and use trust the error handling in doMatrixAction() to handle any fuckups.
def listMatrixAction():     
    """List available matrix actions in a nice, easy to comprehend list."""
    d = config.sections()   # Make a list of all the sections in mydeck.txt
    del d[0:3]              # Ignore "MyAttributes, My Skills, MyDeck - not matrix actions
    print "\nCommands"
    print
    # This section turns the list of sections into a nice, readable, two-column menu that can be easily fed into the doaction function
    # Found this code on stackoverflow. I don't quite understand how this does what I want it to do, but it does it. Yay!
    print "\n".join("%-20s %s"%(d[i],d[i+len(d)/2]) for i in range(len(d)/2))
    print
    print "\nCurrent targets:"
    for key in marksontarget:
        print key.title() + ": {} marks.".format(marksontarget[key])
    action = raw_input("Enter a Command: ")
    target = raw_input("Enter a target from the list above: ").lower()
    print
    if not doMatrixAction(action, target):  # fucked up? Back to the top!
        listMatrixAction()
    else:
        userInterface() #Mission accomplished? Back to the menu.
    return


def doMatrixAction(action, target):
    """Inform the user how many dice they need to roll and if they have enough marks on the target."""
    try:
        x = marksontarget[target]   #error checking. If key error, target not valid and returns False to listMatrixAction()
    except KeyError:
        print "Invalid target entered. Check input and try again.\nYou entered: {}".format(target)
        anykey = raw_input("Press any key to continue")
        return False
        #Migt remove the marks check. What if you just want to know how a command works? It's not like it's rolling dice for the user.
    if  readConfig(action,"marksrequired")> marksontarget[target]: # Got marks?
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
        print "Relevant limit: {} ({})".format(program["limitedby"].title(),decklimit)
        print "Opposed by: " + program["opposedby"] + "\n"
        print "Modifiers applied:"
        print
        anykey = raw_input("Press any key to continue")
        userInterface()
        print
    return

def setMatrixDamage(total, damage):
    """Helps with damage tracking. Keeping this one really simple."""
    print "Current deck HP = {}/{}".format(total - damage, total)
    newHP = raw_input("How much damage did you take?: ")
    pain = int(newHP) * -1
    print pain
    return pain

def setHotCold():
    """Switches between running hot-sim and running cold-sim"""
    if modifiers["simlevel"] == 0:
        modifiers.update({"simlevel":2})
        print "\nNow running hot-sim. Good luck!\n"
    else:
        modifiers.update({"simlevel":0})
        print "\nNow running cold-sim. Good luck!\n"
    anykey = raw_input("Press any key to continue")
    return

def setRunningSilent():
    """Switches between silent running (-2) and normal running (0)"""
    if modifiers["running silent"] == 0:
        modifiers.update({"running silent":-2})
        print "\nNow running silent (-2). Good luck!\n"
    else:
        modifiers.update({"running silent":0})
        print "\nNo longer running silent. Good luck!\n"
    anykey = raw_input("Press any key to continue")
    return

def setRunningSoftware():
    """Activates and deactivates software up to the DP limit. Not implemented yet."""
    print "Not implemented yet."
    return 

def addRemoveTarget():
    """Add or remove a target."""

    choice = raw_input("[1] Add or [2] Remove a target?: ")
    if choice not in str(range(1,3)):
        print "Invalid choice. Try again.\n"
    elif choice == str(1):
        newtarget = raw_input("Please enter ID of target: ")
        marksontarget[newtarget.lower()] = 0
    else:
        deltarget = raw_input("Please enter ID of target: ")
        del marksontarget[deltarget.lower()]        
    anykey = raw_input("Press any key to continue")
    print
    userInterface()
    return

def addRemoveMarks():
    """Add or remove marks from a target."""
    choice = raw_input("Please enter ID of target: ")
    if choice not in marksontarget:
        print "Invalid choice. Try again.\n"
    else:
        marks = raw_input("Please enter the number of marks on target: ")
        marksontarget[choice.lower()] = int(marks)
    anykey = raw_input("Press any key to continue")
    print
    userInterface()
    return

def userInterface():
    """The menu system that drives the options and allows the player to use the various methods."""
    deckmaxhp = 9       # Actually, it's 8 + (Deck Rating/2) but I can't quite work out how to make this behave with a level 1 device
    deckdamage = 0      # So for now, it's hard coded.
    linklocked = False  # Some options not possible while link-locked
    matrixinitiative = readConfig("MyAttributes", "int") + deckconfig["data processing"]

    length = 80
    leftmargin = 2
    interfacetext = {0: "Welcome to Matrix Manager version 0.5!",}

    displayoptions = {
        1:"Change Array",
        2:"Toggle Running Mode",
        3:"Add/Remove Target",
        4:"Add/Remove Marks",
        5:"Update Modifiers",
        6:"Toggle Running Silent",
        7:"Perform a Matrix Action",
        8:"Add/Remove damage",
        9:"Change Running Software.",
        10:"Quit",
        }
    
    print length * "#"
    print "#" + (length-2)* " " + "#"
    print "#" + (((length-2) - len(interfacetext[0]))//2)* " " + interfacetext[0].upper() + (((length-2) - len(interfacetext[0]))//2)* " " + "#"
    print "#" + (length-2)* " " + "#"
    print length * "#" + "\n"
    print "STATUS:" + 10 * " " + "dHP: {}/{}".format(deckmaxhp - deckdamage, deckmaxhp)
    if modifiers["simlevel"] == 2:
        print "You are running in hot-sim mode! BE CAREFUL - DAMAGE TAKEN IS LETHAL"
        print "Matrix initiative: {} + 4d6".format(matrixinitiative)
    else:
        print "You are running in cold-sim mode. Damage taken is stun."
        print "Matrix initiative: {} + 3d6".format(matrixinitiative)
    print
    print "Current Array:"
    for key in deckconfig:
        print 5 * " " + key.title() + ": " + str(deckconfig[key])
    print
    print "Current Targets/Marks: "
    for key in marksontarget:
        print 5 * " " + key.title() + ": " + str(marksontarget[key]) + " mark(s)"
    print
    print "Active Modifiers:"
    for key in modifiers:
        print 5 * " " + key.title() + ": " + str(modifiers[key])
    print
    
    for key in displayoptions:
        if key % 2 == 0:
            print "{}: {}\n".format(key, displayoptions[key])
        else:
            print "{}: {}".format(key, displayoptions[key])
    choice = raw_input("Enter a number to continue (1-10): ")
    while choice not in str(range(1, 11)):
        print "\nInvalid option.\n"
        choice = raw_input("Enter a number to continue (1-10): ")        
    else:
        if choice == "1":
            setMatrixArray()
        elif choice == "2":
            setHotCold()
        elif choice == "3":
            addRemoveTarget()                       # Now working!
        elif choice == "4":
            addRemoveMarks()                        # Now working!  
        elif choice == "5":
            #Insert fancy menu thing here, but for now a placeholder.
            #setModLevel("noise")
            print "boop."
        elif choice == "6":
            setRunningSilent()                      # Toggle whether you're running silent or not. Could be done by setModLevel() but it doesn't need flexibility
        elif choice == "7":
            listMatrixAction()
        elif choice == "8":                         # This should be trivial, but for some reason it's just not working. Fuck it, not important for now.
            damage = setMatrixDamage(deckmaxhp,deckdamage)
            deckdamage = deckmaxhp - deckdamage          
        elif choice == "9":
            setRunningSoftware()                    # Not written yet. Actually kinda important, but I'm being lazy.
        elif choice == "10":
            exit()
        else:
            pass
        userInterface()
    return

userInterface()


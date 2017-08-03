"""
Exits

Exits are connectors between Rooms. An exit always has a destination property
set and has a single command defined on itself with the same name as its key,
for allowing Characters to traverse the exit to its destination.

"""
from evennia import DefaultExit

class Exit(DefaultExit):
    """
    Exits are connectors between rooms. Exits are normal Objects except
    they defines the `destination` property. It also does work in the
    following methods:

     basetype_setup() - sets default exit locks (to change, use `at_object_creation` instead).
     at_cmdset_get(**kwargs) - this is called when the cmdset is accessed and should
                              rebuild the Exit cmdset along with a command matching the name
                              of the Exit object. Conventionally, a kwarg `force_init`
                              should force a rebuild of the cmdset, this is triggered
                              by the `@alias` command when aliases are changed.
     at_failed_traverse() - gives a default error message ("You cannot
                            go there") if exit traversal fails and an
                            attribute `err_traverse` is not defined.

    Relevant hooks to overload (compared to other types of Objects):
        at_traverse(traveller, target_loc) - called to do the actual traversal and calling of the other hooks.
                                            If overloading this, consider using super() to use the default
                                            movement implementation (and hook-calling).
        at_after_traverse(traveller, source_loc) - called by at_traverse just after traversing.
        at_failed_traverse(traveller) - called by at_traverse if traversal failed for some reason. Will
                                        not be called if the attribute `err_traverse` is
                                        defined, in which case that will simply be echoed.
    """
    def return_appearance(self, looker):
        if self.db.desc:
            desc = self.db.desc
        else:
            desc = u"|yThrough the {} {}:|n\n|c{}|n\n{}".format(
                self.db.typename or 'exit',
                self.key,
                self.destination.get_display_name(looker),
                self.destination.db.desc or '\n'
            )
        return desc

class Door(Exit):
    """
    Represents a closable door. Closes self after x seconds.
    """

    def at_object_creation(self):
        self.db.open = False
        self.db.typename = "door"

    def return_appearance(self, looker):
        if self.db.open:
            return super(Door, self).return_appearance(looker)
        else:
            return "|y{}|n\nA closed {}.".format(
                self.get_display_name(looker),
                self.db.typename or "door"
            )

from characters import Character
from evennia import search_script

class NPC(Character):
    def at_object_creation(self, *args, **kwargs):
        try:
            self.db.signalhandler = search_script('signalhandler')[0]
        except:
            print("Unable to find SignalHandler, please start the SignalHandler")

        if self.db.signalhandler:
            self.db.signalhandler.subscribe(self, self.at_heard_noise, 'noise')

    def at_heard_noise(self, *args, **kwargs):
        if 'source' in kwargs:
            source = kwargs['source']
            to_say = "{}, pipe down!".format(source.key)
        else:
            to_say = "Woah! What was that?"
        self.execute_cmd("say {}".format(to_say))

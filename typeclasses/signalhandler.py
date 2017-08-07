"""
SignalHandler
Allows objects to subscribe to and throw signals
"""
from evennia import DefaultScript
from twisted.internet.defer import inlineCallbacks


class Signal(object):
    def __init__(self):
        # the signal's key should be unique - the signal handler
        # will use a dict of subscriptions
        self.key = self.__class__.__name__


class SignalHandler(DefaultScript):
    def subscribe(self, subscriber, callback, *signals, **kwargs):
        if callable(callback) and callback.__self__ == subscriber:
            callback = callback.__name__
        for signal in signals:
            if isinstance(signal, Signal):
                if signal.key in self.db.subscribers:
                    self.db.subscribers[signal.key].append((subscriber, callback))
                else:
                    self.db.subscribers[signal.key] = [(subscriber, callback)]
            elif isinstance(signal, (str, unicode)):
                if signal in self.db.subscribers:
                    self.db.subscribers[signal].append((subscriber, callback))
                else:
                    self.db.subscribers[signal] = [(subscriber, callback)]
            else:
                # might wanna throw error
                pass

    def is_subscribed(self, subscriber, signal):
        if isinstance(signal, Signal):
            signal = signal.key
        if signal in self.db.subscribers:
            for stored_sub, callback in self.db.subscribers[signal]:
                if subscriber == stored_sub:
                    return True
        # if we get here we either didn't find the subscriber or the signal    
        return False

    def unsubscribe(self, subscriber, *signals, **kwargs):
        keys_to_remove = []
        for signal in signals:
            if isinstance(signal, Signal):
                keys_to_remove.append(signal.key)
            elif isinstance(signal, (str, unicode)):
                keys_to_remove.append(signal)
        for key in keys_to_remove:
            if key in self.db.subscribers:
                to_remove = []
                for item in self.db.subscribers[key]:
                    if item[0] is subscriber:
                        to_remove.append(item)
                for item in to_remove:
                    try:
                        self.db.subscribers[key].remove(item)
                    except ValueError as e:
                        pass
        return True

    def throw(self, signal, *args, **kwargs):
        if isinstance(signal, Signal):
            key = signal.key
        else:
            key = signal

        if key in self.db.subscribers:
            caught_signal = []
            for subscriber, callback in self.db.subscribers[key]:
                status = getattr(subscriber, callback)(*args, **kwargs)
                caught_signal.append(subscriber)
            return caught_signal
        else:
            return []

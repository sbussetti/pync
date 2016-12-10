#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import subprocess
from dateutil.parser import parse

LIST_FIELDS = ["group", "title", "subtitle", "message", "delivered_at"]


class TerminalNotifier(object):
    TERMINAL_NOTIFIER_VERSION = "1.6.1"

    def __init__(self):
        """
        Raises an exception if not supported on the current platform or
        if terminal-notifier was not found.
        """
        proc = subprocess.Popen(["which", "terminal-notifier"], stdout=subprocess.PIPE)
        env_bin_path = proc.communicate()[0].strip()
        if env_bin_path and os.path.exists(env_bin_path):
            self.bin_path = os.path.realpath(env_bin_path)
        elif os.path.exists("/usr/local/bin/terminal-notifier"):
            self.bin_path = os.path.join("/usr/local/bin/", "terminal-notifier")
        else:
            self.app_path = os.path.join(
                os.path.dirname(__file__),
                "vendor/terminal-notifier-%s/terminal-notifier.app" % self.TERMINAL_NOTIFIER_VERSION
            )
            self.bin_path = os.path.join(self.app_path, "Contents/MacOS/terminal-notifier")

        if not self.is_available():
            raise Exception("pync is only supported on Mac OS X 10.8, or higher.")

        if not os.path.exists(self.bin_path):
            raise Exception("pync was not properly installed. Head over to https://github.com/SeTeM/pync/"
                            " and file a bug.")

        if not os.access(self.bin_path, os.X_OK):
            os.chmod(self.bin_path, 111)
            if not os.access(self.bin_path, os.X_OK):
                raise Exception("You have no privileges to execute \"%s\"" % self.bin_path)
        self.wait = False

    def notify(self, message, **kwargs):
        """
        Sends a User Notification.

        The available options are `title`, `group`, `activate`, `open`, `sound`, and
        `execute`. For a description of each option see:

          https://github.com/alloy/terminal-notifier/blob/master/README.markdown

        Examples are:

          notifier = TerminalNotifier()

          notifier.notify('Hello World')
          notifier.notify('Hello World', title='Python')
          notifier.notify('Hello World', sound='Ping')
          notifier.notify('Hello World', group=os.getpid())
          notifier.notify('Hello World', activate='com.apple.Safari')
          notifier.notify('Hello World', open='http://github.com/')
          notifier.notify('Hello World', execute='say "OMG"')

          The options `wait` is a boolean for whether or not we need to
          wait (block) for the background process to finish
        """
        message = message.encode('utf-8')

        self.wait = kwargs.pop('wait', False)

        args = ['-message', message]
        args += [a for b in [("-%s" % arg, str(key)) for arg, key in kwargs.items()] for a in b]  # flatten list

        return self.execute(args)

    def execute(self, args):
        args = [str(arg) for arg in args]
        output = subprocess.Popen(
            [self.bin_path, ] + args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )

        if self.wait:
            output.wait()

        if output.returncode:
            raise Exception("Some error during subprocess call.")

        return output

    def remove(self, group="ALL"):
        """
        Removes a notification that was previously sent with the specified
        ‘group’ ID, if one exists.

        If no ‘group’ ID is given, all notifications are removed.
        """
        return self.execute(["-remove", group])

    def list(self, group="ALL"):
        """
        If a ‘group’ ID is given, and a notification for that group exists,
        returns a dict with details about the notification.

        If no ‘group’ ID is given, an array of hashes describing all
        notifications.

        If no information is available this will return [].
        """

        output = self.execute(["-list", group]).communicate()[0]
        res = list()

        for line in output.splitlines()[1:]:
            res.append(dict(zip(LIST_FIELDS, line.split("\t"))))
            try:
                res[-1]["delivered_at"] = parse(res[-1]["delivered_at"])
            except ValueError:
                pass

        return res

    @staticmethod
    def is_available():
        """ Returns whether or not the current platform is Mac OS X 10.8, or higher."""
        if not platform.system() == 'Darwin':
            return False

        major, minor = platform.mac_ver()[0].split('.')[:2]

        return int(major) > 10 or int(minor) >= 8



def notify(message, **kwargs):
    """
    Sends a User Notification.

    The available options are `title`, `group`, `activate`, `open`, `sound`, and
    `execute`. For a description of each option see:

      https://github.com/alloy/terminal-notifier/blob/master/README.markdown

    Examples are:

      import pync

      pync.notify('Hello World')
      pync.notify('Hello World', title='Python')
      pync.notify('Hello World', sound='Ping')
      pync.notify('Hello World', group=os.getpid())
      pync.notify('Hello World', activate='com.apple.Safari')
      pync.notify('Hello World', open='http://github.com/')
      pync.notify('Hello World', execute='say "OMG"')

      The options `wait` is a boolean for whether or not we need to wait (block) for the background process to finish
    """
    notifier = TerminalNotifier()
    notifier.notify(message, **kwargs)


def remove_notifications(group="ALL"):
    """
    Removes a notification that was previously sent with the specified
    ‘group’ ID, if one exists.

    If no ‘group’ ID is given, all notifications are removed.
    """
    notifier = TerminalNotifier()
    return notifier.execute(["-remove", group])


def list_notifications(group="ALL"):
    """
    If a ‘group’ ID is given, and a notification for that group exists,
    returns a dict with details about the notification.

    If no ‘group’ ID is given, an array of hashes describing all
    notifications.

    If no information is available this will return [].
    """
    notifier = TerminalNotifier()
    return notifier.list(group)


def main():
    """Show a test notification."""
    notifier = TerminalNotifier()
    notifier.notify("Notification from {0}".format(__file__),
                    open="http://github.com")


if __name__ == '__main__':
    main()

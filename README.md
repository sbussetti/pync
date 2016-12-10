## ⚠️ Disclaimer
I just found this library, updated it to also support Python 3 and updated terminal-notifier to version 1.7.1. At the moment I have no intention to support the library.

But it was fun to fiddle around a bit and learn about Travis CI. :)


pync
====

A simple Python wrapper around the [`terminal-notifier`][HOMEPAGE] command-line tool (version 1.7.1), which allows you to send User Notifications to the Notification Center on Mac OS X 10.8, or higher.

![Screenshot](http://f.cl.ly/items/1k051n3k0u0i101m1i0U/Screen%20Shot%202012-08-24%20at%2012.20.40%20PM.png)

Installation
------------

```
pip install git+https://github.com/jasperges/pync.git
```
or
```
git clone git://github.com/jasperges/pync.git
cd pync
python setup.py install
```
or for the older versions by SeTeM:
```
pip install pync
```

Usage
-----

For full information on all the options, see the tool’s [README][README].

### Examples:

Using the notify function
```python
import pync

pync.notify('Hello World')
pync.notify('Hello World', title='Python')
pync.notify('Hello World', group=os.getpid())
pync.notify('Hello World', activate='com.apple.Safari')
pync.notify('Hello World', open='http://github.com/')
pync.notify('Hello World', execute='say "OMG"')

pync.remove_notifications(os.getpid())

pync.list_notifications(os.getpid())
```

Using the notifier object
```python
from pync import TerminalNotifier

notifier = TerminalNotifier()
notifier.notify('Hello World')
notifier.notify('Hello World', title='Python')
notifier.notify('Hello World', group=os.getpid())
notifier.notify('Hello World', activate='com.apple.Safari')
notifier.notify('Hello World', open='http://github.com/')
notifier.notify('Hello World', execute='say "OMG"')

notifier.remove(os.getpid())

notifier.list(os.getpid())
```


License
-------

All the works are available under the MIT license. **Except** for ‘Terminal.icns’, which is a copy of Apple’s Terminal.app icon and as such is copyright of Apple.

See [LICENSE][LICENSE] for details.

[HOMEPAGE]: https://github.com/alloy/terminal-notifier
[README]: https://github.com/alloy/terminal-notifier/blob/master/README.markdown
[LICENSE]: https://github.com/setem/pync/blob/master/LICENSE

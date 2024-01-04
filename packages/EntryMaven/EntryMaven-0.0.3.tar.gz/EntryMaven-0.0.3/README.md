# About EntryMaven

Python package aiming to offer a simple and efficient customizable logger using the native Logging library.

With this module, you can easily create records that automatically generate log files, allowing you to customize the names of these records files.

## Getting Started - Library

### Installation

```Python
pip install entrymaven
```

### Usage

Simple example of how to use:

```Python
import entrymaven as emav

generic_logger = emav.Essentials.gen()
l = emav.l

l.info('First entry in this log file')

# Output: 2000-01-01 00:00:00,000 - INFO - First entry in this log file
```

> **Note**: As default, the log file name is "entries.log" and the log level is DEBUG

An alternative, more concise approach that includes defining a custom log file name and log recording level:

```Python
from entrymaven import l, Essentials
Essentials.gen(filename= 'test.log', level= 'INFO')

l.info('First entry in this log file')
```

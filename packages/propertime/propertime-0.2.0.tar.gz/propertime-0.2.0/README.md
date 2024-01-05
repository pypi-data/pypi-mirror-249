# Propertime

An attempt at proper time management in Python.

[![Tests status](https://github.com/sarusso/Propertime/actions/workflows/ci.yml/badge.svg)](https://github.com/sarusso/Propertime/actions) [![Licence Apache 2](https://img.shields.io/github/license/sarusso/Propertime)](https://github.com/sarusso/Propertime/blob/main/LICENSE) [![Semver 2.0.0](https://img.shields.io/badge/semver-v2.0.0-blue)](https://semver.org/spec/v2.0.0.html) 


## Quickstart

Propertime is an attempt at implementing proer time managemtt in Python, embracing several traits of how we masure time both as physical and calender time, including that timethat time arithmetic is some operations are not alwas well defined

In a nutshell, it provides two main classes: the ``Time`` class for representing time (similar to a datetime) and the ``TimeUnit`` class for representing units of time (similar to timedelta). 

Such classes are implemented assuming two strict base hypotheses:

- Time is a floating point number corresponding the number of seconds after the zero on the time axis, which is set to 1st January 1970 UTC. Any other representations (as dates and hours, time zones, daylight saving times) are indeed just representations and built on top of it.

- Time units can be of both fixed length (seconds, minutes, hours) and *variable* length (days, weeks, months, years). This means that the length (i.e. the duration in seconds) of a one-day time unit is not defined *unless* it is put in context, which means to know when it is applied.

These two assumptions allow Propertime to solve by design many issues arising in manipulating time that are still present in Python's built-in datetime module as well as in most third-party libraries.

Implementing "proper" time comes at a price: it optimizes for consistency over performance and it is quite strict. It heavily depends on the use-case if it is a suitable solution or not.

Propertime provides a simple and neat API, it is realitvely well tested and its objects play nice with Python datetimes so that you can mix and match and use it only if and when needed.

You can get started by having a look at the [quickstart notebook](Quickstart.ipynb), or by reading the [reference documentation](https://propertime.readthedocs.io).



## Installing

To install Propertime, simply run ``pip install propertime``.

It has just a few requirements, listed in the ``requirements.txt`` file, which you can use to manually install or to setup a virtualenv.


## Testing

Propertime is relatively well tested using the Python unittest module. Just run a ``python -m unittest discover`` in the project root.

To test against different Python versions, you can use Docker. Using Python official images and runtime requirements installation:

    docker run -it -v $PWD:/Propertime python:3.9 /bin/bash -c "cd /Propertime && pip install -r requirements.txt && python -m unittest discover"
    
There is also a ``regression_test.sh`` script that tests, using Docker, from Python 3.6 to Python 3.12.
 


## License
Propertime is licensed under the Apache License version 2.0. See [LICENSE](https://github.com/sarusso/Propertime/blob/master/LICENSE) for the full license text.




Communications
**************

The main scenario :index:`scenario;communications` is one of:

- An observing network of sites (observatories)
- Each observatory has one or more buildings
- Each building has one or more piers
- Each pier has its elements, and one or more OTAs
- Each OTA has lots of things. One or more of them may be Flex Spec 1 spectrographs.

This project implements its OTAs with piggy-back Raspberry Pi processors
on the OTA with one power cable and one Ethernet cable. This makes wire
maintenance very easy. Since the Raspberry Pi is already deployed, with
Astroberry KStars/INDI/Ekos -- there is spare room for our instrument's
control Single Board Microcontrollers (SBMs). 

In spectroscopy it is desirable to have a piggy-back system for simultaneous
photometry of the target.

Each OTA may have one or more Raspberry computers. Each computer may have one or
more serial connections (multi-drop destinations using a serial interface)
to one or more Arduino-class SBMs. 

Remembering the mantra, "Flexible is Flexible" -- how this gets built and
orchestrated makes for a very interesting problem.

The message origination may be a GUI like interface or an intelligent
scheduler. Ideally the scheduler is inter-operable with other schedulers
to maximize the observing output of its network. This is the "lofty" future goal.
Now is present-time for architecture.

There are two paradigms to help with understanding the FlexSpec 
communication:

- The Captain of a Ship concept: Here directions are supplied to the crew in the form of orders in common terms (rotate n degrees) and the crew translates that into a compass heading.

- The matryoshkas :index:`matryoshkas` (nested-doll) model: messages within messages.

- Postal Delivery System, with a set of inter-related postmasters. The postmaster accepts packages or envelopes, with a return address. 

The implementation is a nested set of restricted JSON dictionaries.

A dictionary is a "key" : "value" pair. The key is restricted to always be a quoted-string
without spaces.  The "value" may be a quoted string, an integer (no quotes), a float
(no quotes and not using exponential notation) or -- yup a dictionary.

The idea is to have a set of "matched classes" for each widget utilized. They
are matched as:

Character Set
-------------

The JSON communications strings are taken from a restricted ASCII
character set ANSI X3.4-1986 :index:`communication;ASCII ANSI
X3.4-1986` with an 8-bit data frame, MSB defined to be zero. This
permits traditional 8-bit serial terminal code (PuTTY) :index:`PuTTY`
to monitor lines, permits using out of band characters as an alarm
for corrupted serial communications, allows special characters
(ASCII control characters) to serve allow in-band synchronization
and special "in-band" control.

Here the characters ``{}"":,`` are strictly reserved for JSON use
to promote very restricted hand-coded JSON capability for lesser
machines. 

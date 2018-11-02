---
author:
- 'Luca Parolari[^1]'
date: '2018/10/04'
title: '**Work Pay Calculator**'
---

**Abstract**

[2cm]{}[2cm]{} WPC is a light-weight, highly configurable and easy to
use library with a minimal CLI, with the objective of manage your work
(hours and costs) and emit invoices.\
This document contains a brief, requirements and design project for the
library.\

WPC
===

What is
-------

*Work Pay Calculator* has the objective to simplify the **management**
of the work done in terms of hour, cost and profits. In other hands WPC
is an application that smartly stores hours done for a work and allows
to automatize the process of hours pay calculation and *occasional
performance*[^2] emission.

What is not
-----------

WPC is not a management tool for fiscal things, futhermore, for now,
it’s not an hour marker in terms of real-time start and stop counter
(see \[subsec:enhancements\]).

Features
--------

1.  Light-weight, simple and easy to use.

2.  Easily syncronizable with cloud services: only the executable and
    the data storage is needed. Data storage needs to be syncronized
    only if the SQLite engine is chosed.

3.  CLI inteface, in order to focus the objective to the application
    functionalities.

4.  Highly configurable: personalize environment variables and achieve
    your needs.

5.  Default answer configuration. Lot of configurable default answers,
    avoing boring data typing.

Examples
--------

**Scenario 1**: today I’ve worked for a customer 6 hours: 3 of coding, 1
learing a new technology and 2 to publish the work online. What the
hell, I have to register this things before I forget them.

No problem, open WPC and insert a new work in a way like this:

    wpc> work: today 14:30 17:30 true
    wpc> work: km? [0]: 
    wpc> work: add? [0]: 
    wpc> work: registry? [General work]: I've coded the
    pinco pallo project
    wpc> Work inserted successfully!

And you can repeate this procedure any time you want to increase the
datail of hours done in this day.

Analisys
========

This chapter will report the result of the project analisys, and its
requirements.

Requirements
------------

The system will be developed as a library written in Python (for
educational purposes) with a minimal CLI[^3]. The system will need a
dababase, in this context SQLite will be chosen (for educational
purposes again), however a strategy to make db engine interchangable
could be adopted in later versions (see \[subsec:enhancements\]).

The system should allow the user to:

1.  Setup system variables, even if default values are setted. (see
    *\[subsec:configuration\]*);

2.  Manage clients;

3.  Enter a new line of work with following data:

    1.  Date of work;

    2.  Start and end time of work, or directly number of hours done;

    3.  Boolean production value: true if the work can be marked as
        production, false otherwise;

    4.  The kilometers done to reach the work place (if any);

    5.  An add value, if any extra outgoings;

    6.  Some notes, to mark down any noticeable data or to specify what
        the add value stands for;

    7.  A description of work done;

4.  Mark some dates as paid;

5.  Allow registering forfait payments, that should be removed from the
    next bill;

6.  Show some statistics:

    1.  Total hours done;

    2.  Total non-production hours done;

    3.  Total production hours done;

    4.  Total kilometers done;

    5.  Total add;

    This should be allowed for each paid “session”, including not paid
    data as default.

7.  Financial report:

    1.  Total hours profit;

    2.  Total non-taxable hours profit;

    3.  Total taxable hours profit;

    4.  Total kilometers cost;

    5.  Total add cost;

    6.  Total profit;

    7.  Total profit with fiscal elaboration (IVA, gross and net to
        pay).

    Also this should be available for each paid “session”, including not
    paid data as default.

Configuration {#subsec:configuration}
-------------

The system needs some static parameters that can change in the future.
The a configuration manager is needed to handle this requirement.

Configuration to handle are:

1.  euro/hour value, i.e. how much an hour of work cost for the
    customer. For now, every hour has the same cost, but in future could
    be implemented a way to make some hours with a price and some other
    with other price;

2.  kilometers/litre, in order to calculate how miny litres of gas are
    needed base on km done;

3.  litre/euro, in order to calculate a possible value to expose as a
    cost (will be approximate);

4.  IVA, the italian fistal number for taxes.

Enhancements {#subsec:enhancements}
------------

Here will be listed all programmate or desiderable changes to the
project.

Programmed enhancements: *none* for now. To consider:

1.  Multiple database engine support;

2.  Different hour cost based on work;

Design
======

Add some nice diagrams or attachments.

![image](wpc_data_model)

Version
=======

Analisys
--------

Analisys version **0.4.0**. Requirements are a draft, might change. No
new official version will be issued until the end of the draft.

Design
------

Design version **0.2.0**.

Authors
=======

Luca Parolari (luca.parolari23@gmail.com), computer science’ student at
Unversity of Parma, Italy.

Collaborating
-------------

Contact me at luca.parolari23@gmail.com, or contribute directly on
GitHub. If you find an issue please report it on GitHub.

License
=======

GNU/GPL v3, or any later versions.\

[^1]: luca.parolari23@gmail.com

[^2]: This is an italian fiscal document that certifies work for
    someone.

[^3]: Command Line Interface

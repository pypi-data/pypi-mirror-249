The Ember Factory
=================

Objective
---------
The purpose of this software is to facilitate the (re)production of burning ember diagrams of the style used 
in IPCC reports.
An example is figure 2 from the Summary for Policymakers of the 
Special Report on a global warming of 1.5°C: 
[SR15 Figure SPM.2](https://www.ipcc.ch/site/assets/uploads/sites/2/2019/02/SPM2-1003x1024.png). 

The Ember Factory is a small web application ('the factory') that relies on the related 
[EmberMaker](https://pypi.org/project/embermaker/) project 
(...'the machine') to produce the diagrams. While the EmberFactory produces diagrams in just a few clicks,
[EmberMaker](https://pypi.org/project/embermaker/) can be integrated into other applications as a library.

The ability of this software to reproduce many of the figures published to date by the IPCC has been carefully tested
(however, the IPCC would not be responsible for any errors in this software).

How to use
----------
This software (hereafter 'the EF') is designed to work as a web application. 
However, it is relatively easy to run it "locally":

- The application is publicly available here: https://climrisk.org/emberfactory

- To run it on your own computer, you need to have Python >= 3.10 installed, then install the EF with pip: `pip3 install emberfactory`
  Then set the environment variable needed by flask: `export FLASK_APP=emberfactory` (for Windows: `$env:FLASK_APP = "emberfactory"`) 
  and start with `flask run`. You should receive an url to open in your browser and access the EF, such as for example
  http://127.0.0.1:5000/

- To run the app on a server, you need a *WSGI server such as Gunicorn* (*not included* in the required packages
because you do not need it to run the EF locally, and you may have another WSGI server).  
If you want a root path such as /emberfactory, the EF is written so that you should set this path 
in the APPLICATION_ROOT variable within a file called emberfactory.cfg that needs to be
located in your /instance folder (this is not entirely standard).

Development history
-------------------
This software was created by philippe.marbaix -at- uclouvain.be at the end of 2019.
The first objective was to produce figure 3 of Zommers et al. 2020 ([doi.org/10/gg985p](https://doi.org/10/gg985p)).
Improvements were regularly provided during 2020 and this will likely continue if there are needs. 
Some aspects of the coding may still reflect the logic of the first versions rather than 
what would be done if starting from scratch; changes are done when they become useful, as experience
also drives further development. Any feedback is thus very helpful!

Help is welcome to further improve the application. All contributions will be recognised :-).

No tracking
-----------
I am making efforts to avoid anything that could result in
user tracking: no fonts, icons or libraries downloaded from third-parties by the user.
I would like this to continue in the future. Advice would be welcome.
It is also why the code is hosted by [framasoft](https://framasoft.org) using [gitlab](https://gitlab.org). 
I thank them both.  
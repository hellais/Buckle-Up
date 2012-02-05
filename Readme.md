# Buckle Up!
The aim of this project is raise sensibility of security on OS X
and develop seatbelt profiles for all of the common used OSX applications.

## The Buckle Up script
Buckle Up is also a python script that assists you in patching your applications to
run with seatbelt profiles.

Here is it's help banner:

    Buckle Up!
    -------
    Mac OS X sandboxing helper scripts
    by Arturo Filasto' <art@fuffa.org>

    Usage: buckleup.py [options]

    Options:
      -h, --help            show this help message and exit
      -l, --list            list all application profiles
      -p APP, --patch=APP   patch the desired application
      -a APP, --application=APP
                            explicitly set the application location
      -u APP, --unpatch=APP
                        remove patch from the desired application
      -r APP, --run=APP     run the desired application in sandbox

To list the currently available profiles run `./buckleup.py  -l`:

    [-] Listing Buckle Up sandbox profiles...
          Name: Adium default (APP: adium)
          App Location: /Applications/Adium.app/Contents/MacOS/Adium

          Name: Firefox default (APP: firefox)
          App Location: /Applications/Firefox.app/Contents/MacOS/firefox

You can then either run the application from Buckle Up with `./buckleup.py -r adium`
or patch it to use seatbelt every time your run it `./buckleup.py -p adium`.

To remove the patch you should run `./buckleup.py -u adium`

## Manually running apps with seatbelt profiles

To run an app with sandboxing enabled all you have to do is:

    sandbox-exec -f <sandbox_file>.sb /path/to/the/app

For example to run the Adium sandbox plugin do this:

    sandbox-exec -f adium.sb /Applications/Adium.app/Contents/MacOS/Adium


## Buckle Up header

Sandbox profiles for Buckle Up include a special header that allows the shell script to offer a pretty output
to the user and automagically install the application.

When writing an application profile for Buckle up you should use this format. The header should be on the first
line of the sandbox profile:

    ;:buckleup:<buckleup version number>:<app short name>:<app long name>:<path to executable>:

_buckleup version number_: (default 0.1) This is the Buckle Up version number for the app profile

_app short name_: This is the shortname of the profile, it is what the user will provide as arugment to
buckle up to patch the application or run it

_app long name_: This is the full name of the profile, it controls what will show in the list view

_path to executable_: This is the full path of the executable that should be patched, it is generally
something like /Applications/MyApp.app/Contents/MacOS/MyApp

## How to write a sandbox profile


### They easy way

Use the example.sb sandbox file that contains in particular the line

   (trace "profile.sb")

This instructs sandbox-exec to output a profile.sb file that will contain
the raw output of what resources are being accessed during the runtime of the
target application.

You would therefore start the application with:

    sandbox-exec -f example.sb /Path/To/The/Application/

Then run sandbox-simplify on the profile.sb and pipe it to another file:

    sandbox-simplify profile.sb > simplified.sb

You can then start editing that simplified file to see what makes sense to keep,
what can be compacted more and what should be changed.

A useful vi macro to keep handly is this:

    %s/literal "\/Users\/replace_with_your_username/regex #"^\/Users\/[^\.]+/gc

This basically makes your profile work for people that don't have your same username.

### Boring way

You want to start from a basic sandbox profile that contains the bare minimum necessary to start the application.
Something along the lines of this is a good starting point:

    (version 1)
    (debug allow)
    (allow process*)
    (deny default)

What this does it it allow processes to run and it is a whitelist based profile (i.e. the default policy is
to not allow).

The next thing that you want to do is start

    tail -f /var/log/system.log

All the denied by policy lines will end up in that file. Then start your application with your sandbox profile:

    sandbox-exec -f <sandbox_file>.sb /path/to/the/app

You will then see in the `tail -f` terminal lines containing something like:

    Dec 22 14:58:08 x sandboxd[12281] ([12280]): firefox-bin(12280) deny file-read-data /private/tmp

This is saying, for example, that firefox was denied "file-read-data" access to the file in /private/tmp.
You should then evaluate if you want to allow that or not and in the first case add the entry that allows
that in your sandbox file, like so:

    (file-read-data
        (regex "^/private/tmp")
    )

Continue iteratively until you reach a point where your application runs properly and all the error messages
are thing you don't want to happen.

Safe hacking and remember to fasten your seatbelt :)

## Resources

- Apple's Sandbox Guide - http://reverse.put.as/wp-content/uploads/2011/09/Apple-Sandbox-Guide-v1.0.pdf

- Chromium sandboxing - http://www.chromium.org/developers/design-documents/sandbox/osx-sandboxing-design

- http://techjournal.318.com/security/a-brief-introduction-to-mac-os-x-sandbox-technology/

- Iron Suite - https://www.romab.com/ironsuite/


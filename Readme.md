# Buckle Up!
The aim of this project is raise sensibility of security on OS X
and develop seatbelt profiles for all of the common used OSX applications.

To run an app with sandboxing enabled all you have to do is:

    sandbox-exec -f <sandbox_file>.sb /path/to/the/app

For example to run the Adium sandbox plugin do this:

    sandbox-exec -f adium.sb /Applications/Adium.app/Contents/MacOS/Adium


## How to write a sandbox profile

You want to start from a basic sandbox profile that contains the bare minimum necessary to start the application. Something along the lines of this is a good starting point:

    (version 1)
    (debug allow)
    (allow process*)
    (deny default)

What this does it it allow processes to run and it is a whitelist based profile (i.e. the default policy is to not allow).

The next thing that you want to do is start

    tail -f /var/log/system.log

All the denied by policy lines will end up in that file. Then start your application with your sandbox profile:

    sandbox-exec -f <sandbox_file>.sb /path/to/the/app

You will then see in the `tail -f` terminal lines containing something like:

    Dec 22 14:58:08 x sandboxd[12281] ([12280]): firefox-bin(12280) deny file-read-data /private/tmp

This is saying, for example, that firefox was denied "file-read-data" access to the file in /private/tmp. You should then evaluate if you want to allow that or not and in the first case add the entry that allows that in your sandbox file, like so:

    (file-read-data
        (regex "^/private/tmp")
    )

Continue iteratively until you reach a point where your application runs properly and all the error messages are thing you don't want to happen.

Safe hacking and remember to fasten your seatbelt :)

## Resources

- Apple's Sandbox Guide - http://reverse.put.as/wp-content/uploads/2011/09/Apple-Sandbox-Guide-v1.0.pdf

- Chromium sandboxing - http://www.chromium.org/developers/design-documents/sandbox/osx-sandboxing-design

- http://techjournal.318.com/security/a-brief-introduction-to-mac-os-x-sandbox-technology/



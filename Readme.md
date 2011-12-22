# Buckle Up!
The aim of this project is raise sensibility of security on OS X
and develop seatbelt profiles for all of the common used OSX applications.

To run an app with sandboxing enabled all you have to do is:

    sandbox-exec -f <sandbox_file>.sb /path/to/the/app

For example to run the Adium sandbox plugin do this:

    sandbox-exec -f adium.sb /Applications/Adium.app/Contents/MacOS/Adium


## Resources

- Apple's Sandbox Guide - http://reverse.put.as/wp-content/uploads/2011/09/Apple-Sandbox-Guide-v1.0.pdf

- Chromium sandboxing - http://www.chromium.org/developers/design-documents/sandbox/osx-sandboxing-design

- http://techjournal.318.com/security/a-brief-introduction-to-mac-os-x-sandbox-technology/



#!/usr/bin/env python
# Buckle Up
# -----------
# Mac OS X sandboxing helper scripts
# by Arturo Filasto' <art@fuffa.org>
#

import os
import shutil
from optparse import OptionParser
from subprocess import Popen, PIPE

class BuckleUp(object):
    """Buckle Up assists in the patching and running of Mac OS X
    applications in a sandboxed environment.
    """
    def __init__(self):
        # Debugging
        self.debug = True
        # Where the script should look for sandbox file to be installed
        self.sb_file_location = "./profiles"
        # Where sandbox files should be installed to
        self.bu_dir = os.path.expanduser("~/.buckleup")
        if not os.path.exists(self.bu_dir):
            print "[-] First run, creating buckleup config dir"
            os.mkdir(self.bu_dir)
        # Already parsed sandbox files
        self.sbs = []
        self.app_path = None
        self.argument_parser()

    def parse_sb(self, file):
        """Parse a sandbox file written using the Buckle Up header ;:
        The format for Buckle Up headers is:
        ;:buckleup:<buckle_up_version>:<app_shortname>:<app_name>:<app_executable_location>:
        return
            False if the file does not start with the magic header
            Dict containing bu_version, shortname, name, file (sb file),
                patched (True|False), patch_location (patched app filename)
        """
        sb = False
        try:
            f = open(file, 'r')
            line = f.readline()
            if line.startswith(';:buckleup'):
                sb = {}
                v = line.split(":")
                sb['version'] = v[2]
                sb['shortname'] = v[3]
                sb['name'] = v[4]
                if self.app_path:
                    sb['app_location'] = self.app_path
                else:
                    sb['app_location'] = v[5]
                sb['file'] = file
                sb['patched'] = False
                sb['patch_location'] = sb['app_location'] + "-sandboxed"
                if os.path.exists(sb['patch_location']):
                    sb['patched'] = True

        finally:
            f.close()
            return sb

    def unpatch(self, app):
        """Remove a patch from a patched application. Looks in the apps
        directory for the application_name-sandbox, removes the wrapper
        and renames the patched application
        """
        print "[-] Removing patch from %s" % app
        sb = self.get_sb(app)
        # Check to see if the sandboxing profile exists
        if not sb:
            print "[!] Error! sandboxing profile not found. Exiting..."
            return False
        if sb['patched']:
            os.rename(sb['patch_location'], sb['app_location'])
            print "[+] Patch removed from %s (%s)" % (sb['name'],sb['patch_location'])
        else:
            print "[!] No patch detected. No changes made to file system. Exiting..."

    def patch(self, app):
        """Creates a simple shell script wrapper in place of the original application
        and renames the original executable to name-sandboxed
        """
        print "[-] Patching %s" % app
        sb = self.get_sb(app)
        # Check to see if the sandboxing profile exists
        if not sb:
            print "[!] Error! sandboxing profile not found. Exiting..."
            return False

        if sb['patched']:
            print "[!] Application already patched. Try running it!"

        else:
            sb_file_dst = os.path.join(self.bu_dir,sb['file'])

            if self.debug:
                print "Copying the sandbox profile to home config"
            shutil.copyfile(sb['file'], sb_file_dst)

            cmd = "sandbox-exec -f " + str(sb_file_dst) + " " + str(sb['patch_location'])
            if self.debug:
                print "renaming sandbox application to -sandboxed"
            os.rename(sb['app_location'], sb['patch_location'])

            try:
                patch = open(sb['app_location'], 'w')
                patch.write("#!/bin/sh\n")
                patch.write("# This patch was written by Buckle Up ")
                patch.write("v 0.1 (http://github.com/hellais/Buckle-Up/)\n")
                patch.write(cmd)
                patch.write("\n")
            except Exception, e:
                print "[!] Error in writing patch, reverting %s" % e
                os.rename(sb['patch_location'], sb['app_location'])
            finally:
                os.chmod(sb['app_location'], 0755)
                patch.close()
                print "[+] Patch successful!"

    def get_sb(self, name):
        for sb in self.sb_list():
            if sb['shortname'] == name:
                return sb
        return None

    def sb_list(self):
        list = []

        if len(self.sbs) > 0:
            return self.sbs

        for file in os.listdir(self.sb_file_location):
            if file.endswith(".sb"):
                sb = self.parse_sb(file)
                if sb:
                    list.append(sb)
        self.sbs = list
        return list

    def list(self):
        print "[-] Listing Buckle Up sandbox profiles..."
        for sb in self.sb_list():
            print "    Name: %s (APP: %s)" % (sb['name'], sb['shortname'])
            print "    App Location: %s\n" % sb['app_location']


    def run(self, app):
        print "[-] Running %s" % app
        sb = self.get_sb(app)

        # Check to see if the sandboxing profile exists
        if not sb:
            print "[!] Error! sandboxing profile not found. Exiting..."
            return False

        if sb['patched']:
            print "[!] Detected a patched version of %s" % app
            app = sb['patch_location']
        else:
            app = sb['app_location']
        cmd = ["sandbox-exec", "-f", sb['file'], app]
        print "     launch command %s" % ' '.join(cmd)
        p = Popen(cmd, stdout=PIPE)
        while p:
            o = p.stdout.readline()
            if o == '' and p.poll() != None:
                break

    def argument_parser(self):
        description="""Buckle Up!
-------
Mac OS X sandboxing helper scripts
by Arturo Filasto' <art@fuffa.org>
"""
        parser = OptionParser()

        parser.add_option("-l", "--list", dest="list", action="store_true",
                          help="list all application profiles")

        parser.add_option("-p", "--patch", dest="patch",
                          help="patch the desired application",
                          metavar="APP")

        parser.add_option("-a", "--application", dest="app",
                          help="explicitly set the application location")

        parser.add_option("-u", "--unpatch", dest="unpatch",
                          help="remove patch from the desired application",
                          metavar="APP")

        parser.add_option("-r", "--run", dest="run",
                          help="run the desired application in sandbox",
                          metavar="APP")

        (o, args) = parser.parse_args()

        if o.app:
            self.app_path = o.app

        if o.list:
            self.list()

        elif o.patch:
            self.patch(o.patch)

        elif o.unpatch:
            self.unpatch(o.unpatch)

        elif o.run:
            self.run(o.run)

        else:
            print description
            parser.print_help()

if __name__ == "__main__":
    b = BuckleUp()



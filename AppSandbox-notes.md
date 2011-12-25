In OS X 10.7 it is advised to use App Sandbox instead of sandbox-exec.
App sandbox exposes only a subset of the features that sandbox-exec profiles did
but they should be good for most applications and profiles.

These are just some random notes that still need to be structured:

To specify app sandbox parameters you use entitlments. These give certain
permissions to your applications. An entitlement is a .plist file and it looks
something like this:

    <?xml version="1.0" encoding="utf-8"?>
    <plist version="1.0">
    <dict>
        <key>com.apple.security.app-sandbox</key><true/>
        <key>com.apple.security.network.client</key><true/>
        <key>com.apple.security.network.server</key><true/>
    </dict>
    </plist>

To apply the entitlement to your application you use the `codesign` command. To self
sign applications you can run `codesign -s -`.

To apply the entitlement to you app do this:

    codesign -s - -f --entitlements entitlement.plist /Applications/MyApp.app/

WARNING: the -f flag overrites the signature present in your file.

Once an application is sandboxed it may be necessary to regenerate its container.
The container is a special part of your Library folder dedicated to that applications
resources (this means that an app cannot read other applications resources).

To do so run this:

    asctl container acl update /Applications/MyApp.app/



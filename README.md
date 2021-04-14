# CrypticCyrillic
Embed secrets in text that appears normal to the naked eye. 

An exploration of using the cyrillic alphabet alongside the standard alphabet. 

Basically, some cyrillic letters look just like the ones you'd type with your keyboard, but they aren't. 
There's a lotta abuse that can happen because of this, like account impersonation.
Discord makes usernames unique by giving them a discriminator. But Discord also allows just about any character in a username, including cyrillic. 
And, with Discord Nitro, you can change your discriminator. All you have to do to impersonate someone is get discord nitro, run their username through this program, and now you've got a seemingly identical account, aside from the account ID.

It also presents trickery with domain names. Here, go to facebook, I swear it's actually facebook. 
(Don't actually go here, it could be a domain in use by someone malicious, and I haven't checked it yet)
[https://fаcebook.com](https://fаcebook.com)

But here's where cyrillic becomes fun: if you want to embed secret messages. This program does that by converting a message to binary, and every time it comes across a letter than can be "cyrillicized", it decides to make it cyrillic based on the current index in the binary message being either a 0 or a 1. It can also decode. Have fun sending secret messages to people, signing your essays covertly, or impersonating people on platforms that aren't strict with usernames.

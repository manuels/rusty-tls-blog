---
layout: post
title: Initial Commit
---
# Introduction
I thought about the idea of implementing the TLS protocol in Rust. Probably you think this is crazy: Crypto is hard, I mean *hard*.
And yes, probably this will just become some playground for some silly crypto algorithm implementations.

However, if you look at [the list of OpenSSL vulnerabilities](https://www.openssl.org/news/vulnerabilities.html) there are *a lot* of vulnerabilities that exist just because of C: null pointer dereferences, buffer overflows, integer {over,under}flows.

# First Steps
First of all I want to analyse the OpenSSL vulnerabilities of the last ~15 years. Let's see what these vulnerabilities have in common. What failed and why did it fail.

Second, will probably implement [Curve25519](https://en.wikipedia.org/wiki/Curve25519) for basic key exchange (no RSA or DSA at first). There exists a reference implementation of it by the authors ([NaCl](https://nacl.cr.yp.to/)) and I remember watching [a good presentation](https://media.ccc.de/v/31c3_-_6369_-_en_-_saal_1_-_201412272145_-_ecchacks_-_djb_-_tanja_lange) about pitfalls at the Congress ([this one](https://media.ccc.de/v/27c3-4295-en-high_speed_high_security_cryptography#video&t=1990) is proably also worth watching).
There are some nice ways to prevent timing attacks. I have to refresh this knowledge.


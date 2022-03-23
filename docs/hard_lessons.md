# Hard Lessons

1. Do not commit binary files unless it's for documentation or permanently needed.
2. `Sphinx` is the dominant documentation generator for Python, and it's so bloated and complicated to setup. `pdoc` is infinitely better.
3. `string.Template` is a really basic find-and-replace templating engine, and it's miles better than other more complicated, bloated, and slow templating engines.
4. [Checklists are helpful.](checklists/README.md)
5. The new M1 chip is cool, but cx_Oracle (Oracle DB driver) is x86 only, still. [This article was really helpful for setting it up on M1.](https://mnml.blog/2021/12/connection-to-oracle-from-python-on-m1-mac/)
6. If you are getting an `Internal Server Error` from `git push`, then close down the Flask app. I wasted about an hour trying to figure out that riddle.

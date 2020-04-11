Basic Revision Control
======================

Early on in my development career I realized the usefulness of being able to
go back in time and review old code I had written. At first I saw it was a way
for me to go back and retest use cases that broke in newer updates of projects
that I was working on. As I improved I also realized archiving old code
allowed me to recall lessons that I've learned or grab snippets of code that
I've developed before to reuse in a different project.

Before I discovered that revision control tools existed, I relied on very
basic tools in my workflow. Mainly *zip* and *notepad* to archive and compare
changes between my workspace and my archives.


First iteration of revision control
-----------------------------------

My first "revision" workflow was very simple. Every time I had a working
version of my project, I would *zip* the contents of my source code directory
with a number and save it in a dedicated archives folder for the project. You
might know this today as **tagging** your release. This was great and allowed
me the ability to look at the code differences between 2 versions when
troubleshooting a feature breakage in my code. This workflow was great for
awhile.

Eventually though I realized this simple tagging wasn't enough because a major
downside to only archiving releases is that between 2 releases there could be
a significant number of changes or maybe even a complete code rewrite and a
simple zip of code every release wasn't detailed enough to track. Another
thing I realized was sometimes I had a really good idea the previous day but
completely forgot about it when I resumed my work later. I needed a more
robust system that would allow me to go back in smaller increments in time.


Second iteration of revision control
------------------------------------

In this iternation, I started zipping my source code every single day with a
YYYY-MM-DD in the zip filename to track my daily progress of code changes.
If I had interested parallel ideas I wanted to try out, I would copy the code
directory into another folder and work on the idea separately from the main
code directory. This gave me a very rudimentary code branch that I could copy
back to my main code base if the idea worked out.

With this I had a very good system that I used for many years that allowed me
to branch and tag my code so that I can look back on any time I wanted.


Modern Revision control
-----------------------

When I was in my 3rd year of my undergraduate degree I was introduced to SVN
which was the first revision control tool that I ever heard of. It made me
realize that everything I had done until now was something people already
thought of and wrote real tools to handle, I wish I had known this sooner.
This eventually lead me to Git as my favourite revision control tool.

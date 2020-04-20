Basic Revision Control
======================

.. code-block:: none

    ./archive
    ./archive/2020-03-20-project.zip
    ./archive/2020-04-16-project.zip
    ./archive/2020-04-16-project-test-feature.zip
    ./archive/2020-04-21-project.zip
    ./archive/project-1.0.0.zip
    ./archive/project-1.0.1.zip
    ./archive/project-2.0.0.zip
    ./src
    ./src/project.py


Early on in my development career I realized the usefulness of being able to
go back in time and review old code I had written. At first I saw it was a way
for me to go back and retest use cases that broke in newer updates of projects
that I was working on. As I improved I also realized archiving old code
allowed me to recall lessons that I've learned or grab snippets of code that
I've developed before to reuse in a different project.

Before I discovered that revision control tools existed, I relied on very
basic tools in my workflow. Mainly *zip* and *notepad++* to archive and
compare changes between my workspace and my archives.

Workflow:

* Zip the project for every release (Tagging)
* Zip the project every day to record development progress
* Zip the project with a descriptor when testing out new features (branching)
* Unzip the archives to revert code back to a previous state

These days you should use a tool like Git, but the basic nature of this is
fairly similar to what Git is doing in the backend.

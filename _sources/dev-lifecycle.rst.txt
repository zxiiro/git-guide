Development lifecycle: Branches and Tags
========================================

In this section we will discuss commands useful for everyday Git use.

Topics:

* Viewing commits

  * git status
  * git log
  * git diff
  * gitk

* Worktree management

  * .gitignore
  * git clean

* Working with Branches and Tags

  * git branch
  * git checkout
  * git tag


Viewing Commits
---------------

git status
^^^^^^^^^^

The ``git status`` command is a useful command for showing the current state
of your Git directory. Showing the relation between your :term:`Worktree`.


**git status: brand new repo**

.. code-block:: none

    On branch master

    No commits yet

    nothing to commit (create/copy files and use "git add" to track)


**git status: clean worktree**

.. code-block:: none

    On branch master
    nothing to commit, working tree clean


**git status: untracked file**

.. code-block:: none

    On branch master
    Untracked files:
      (use "git add <file>..." to include in what will be committed)

        abc

    nothing added to commit but untracked files present (use "git add" to track)


**git status: modified file**

.. code-block:: none

    On branch master
    Changes not staged for commit:
      (use "git add <file>..." to update what will be committed)
      (use "git checkout -- <file>..." to discard changes in working directory)

        modified:   test

    no changes added to commit (use "git add" and/or "git commit -a")


**git status: staged file**

.. code-block:: none

    On branch master
    Changes to be committed:
      (use "git reset HEAD <file>..." to unstage)

        new file:   abc


git log
^^^^^^^

The ``git log`` command is useful for inspecting the branch history.
This command unfortunately is only as useful as participants on the project
make it. See :ref:`commit-msg:The importance of a Commit Message` for best
practices on managing your commit message.

Check the log of the projects you work on often and try to see if you can
understand the progress of the project from the log. Use the following log
commands and explore the differences:

* git log
* git shortlog
* git log 1.0.0..2.0.0

Many Git commands support passing a commit range to tell Git to show you what
changes are in the 2nd reference point that's not in the 1st reference point.
What Git is doing in this case is taking the 2 commits as a starting point,
then walk through the commit history looking for a common ancestor or parent
commit. Then it uses the commit parent as the starting point of history and
returning the results from the parent commit until the 2nd reference point.

Try reversing the 2 reference points and see how the log changes.


git diff
^^^^^^^^

The ``git diff`` command is useful for checking out what changed between 2
commit points. Try the following:

* git diff
* git diff HEAD~1
* git diff origin/master
* git diff BranchA BranchB


gitk
^^^^

This is the default Git GUI that comes with standard Git. It's a powerful
GUI based viewer to allow you to see the state of the local Git repo. It's
a combination of ``git log`` and ``git diff`` put together into a single
easy to navigate viewer.

.. figure:: img/gitk.png
   :alt: gitk

   gitk - Graphical history viewer


Worktree management
-------------------

.gitignore
^^^^^^^^^^

The ``.gitignore`` file is a special file that can be checked into your Git
repo to tell the Git client to ignore **tracking** certain files.

As mentioned in the :ref:`building-blocks:Local Repository` section there is
also a ``.git/info/excludes`` file which can also be used to ignore files
however this file is not shared in Git so any changes here will only affect
your local work. Typically folks will use ``.gitignore`` as it can be shared
with the team.

One point of confusion for many folks with ``.gitignore`` is the idea of
**tracking** files. This means Git will only ignore the file if it is not yet
tracked (as in checked into Git). So if you already did ``git add file`` to a
specific file, then that file is already tracked in the Git database so the
file won't be ignored.

Let's try a few use cases.

**Case 1: Add a .gitignore**

.. code-block:: bash

    git status
    echo "password.txt" > .gitignore

    git status
    echo "Password" > password.txt

    git status
    git add .gitignore

    git status
    git commit

    git status

Notice that even though we did not commit ``.gitignore`` yet, the fact that
the file exists is enough for the Git client to read the file and ignore
any files that match the pattern.

**Case 2: Force tracking on an ignored file**

.. code-block:: bash

    git status
    git add -f password.txt

    git status
    git commit

    git status
    echo "Password 2" >> password.txt

    git status
    git diff

In this case we see that despite the ``.gitignore`` in place we can track a
file with force. Once tracked however we can see that Git will not ignore
subsequent ignores.


git clean
^^^^^^^^^

The ``git clean`` command is useful to quickly manage your local Worktree.
It provides a quick way to remove temporary files from the repo such as
leftover build artifacts, temporary test files, or even cleanup tool
directories.

* git clean
* git clean -fd
* git clean -fdx


Manipulating Branches:

.git/HEAD
.git/refs/*

Branches don't really exist in Git. They are a convenience for humans as a way
to point to commit objects that would otherwise be impossible for a human to
track.

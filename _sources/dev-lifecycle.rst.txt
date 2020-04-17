Development lifecycle: Branches and Tags
========================================

In this section we will discuss commands useful for everyday Git use.

Topics:

.. contents::
    :local:
    :depth: 2


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


Git References
--------------

As mentioned earlier, Git References are stored in the ``.git/refs/*``
directory. References offer a human readable way to reference specific
commits, think of them as bookmarks.

There are 4 useful reference points one should know to effectively use Git:

.. contents::
    :local:
    :depth: 1

At a rudimentary level you can create new references by simply creating files
in these directories, however Git offers commands to handle this automatically
for you.


HEAD
^^^^

Stored in ``.git/HEAD``, HEAD is a special reference point that always points
to your current location in Git. Typically this is a symbolic reference to the
*branch* or *tag* you have checked out but it can also point to a specific
commit hash. In which case you'll be in Detached HEAD mode.

**HEAD** will move to a new commit every time ``git commit`` or
``git checkout`` is issued.


Branches
^^^^^^^^

Stored in ``.git/refs/heads/*``, **branches** are a human readable reference
to a specific commit that moves along as you commit new code to the project.
Often we work on branches in a development workflow to indicate the code path
we are working on such as active development or to maintain supported releases.

The **branch** reference point will move every time ``git commit`` is issued.


Tags
^^^^

Stored in ``.git/refs/tags/*``, **tags** are human readable reference points
to a specific Git Object. Tags are immutable meaning once a tag is created it
should never be changed once it is shared.

For this reason the most common use case for tags is to reference a release so
that folks can refer back to the exact source code that built a particular
release for historical reasons. Another less common use case though for tags
is to reference specific interesting points in time. Maybe there's an
interesting lessons learned that you want to refer others to, or interesting
commit that might be interesting to reference back to for historical reasons,
we can use a tag to bookmark those commits.

The **tag** reference point is not expected to ever move.


Remotes
^^^^^^^

Stored in ``.git/refs/remotes/*``, **remotes** are read-only copies of
branches from another Git repository. They are read-only to you so you cannot
update these references but they get updated when you sync via ``git fetch``
if the remote repository has moved since you lasted fetched.

The **remote** reference points will move every time ``git fetch`` is issued.

.. note::

    You may notice that there are no such thing as remote tags, mainly because
    as mentioned earlier tags never move so tags should always be the same in
    every Git repo. When ``git fetch --tags`` is called if there are tags you
    are missing they will be created in the usual ``.git/refs/tags/*``
    directory.


Accessing references
^^^^^^^^^^^^^^^^^^^^

You can access references using the full reference path or by their short
references.

* ``git checkout master``
* ``git checkout heads/master``
* ``git checkout refs/heads/master``

All 3 commands checkout the same commit but the last 2 will put you in
``detached HEAD`` mode but it's good to understand that Git is making an
assumption on your behalf when you do not reference the full path.

If you have a branch and a tag with the same name for example:

* ``.git/refs/heads/1.0``
* ``.git/refs/tags/1.0``

Git will prefer the *branch* over the *tag*. If you want the tag you will have
to be more explicit.

.. code-block:: none

    $ git checkout 1.0
    warning: refname '1.0' is ambiguous.
    Switched to branch '1.0'

Apart from branches, all other checkouts will result in ``detached HEAD`` mode.
It is recommended if you are planning to do any development make sure you
turn it into a branch so that you can get proper tracking.


Working with Branches and Tags
------------------------------

.. figure:: img/git-directory-branches.png
   :alt: Workspace: Branches and Tags

   Workspace: Branches and Tags


git-checkout
^^^^^^^^^^^^

This is the main command we can use to fetch files from the Git Local
Repository into our Worktree.


**git checkout**

.. code-block:: bash

    git checkout master
    cat .git/HEAD
    cat .git/refs/heads/master

    git checkout SHA
    cat .git/HEAD

    # Create a new commit
    git add file
    git commit
    cat .git/HEAD

    # Create a new commit on a branch
    git checkout master
    cat .git/HEAD
    cat .git/refs/heads/master
    git add file
    git commit
    cat .git/HEAD
    cat .git/refs/heads/master


**git checkout & create branch**

.. code-block:: bash

    git checkout -b new-branch master
    cat .git/HEAD
    cat .git/refs/heads/new-branch


git-branch
^^^^^^^^^^

.. figure:: img/git-branch-basic.png
    :alt: Branching

    Branching

.. code-block:: bash

    echo 'a1b2c3' > .git/refs/heads/new-branch
    git branch new-branch master
    cat .git/HEAD
    cat .git/refs/heads/new-branch

**Tracking branches** are useful to have your branch track another branch so
that when you do ``git status`` it will tell you how many commits difference
between the 2 branches. This is typically useful when working with remotes
which we will discuss later however can be used to track any local branch as
well.

.. code-block:: bash

    git status
    git branch -u master new-branch
    git status

This tells Git to make **new-branch** track the **master** branch for changes.

.. code-block:: bash

    git status
    git checkout new-branch
    git status

    git add file
    git commit
    git status

    git rebase -i master
    git status

    git checkout master
    git add file
    git commit
    git checkout new-branch
    git status

We can see how the tracking branch affects the result of ``git status``.


git-tag
^^^^^^^

Similar to branch we can create a tag easily and quickly with the ``git tag``
command.

**Lightweight tag**

.. code-block:: bash

    git tag v1.0.0

This creates a lightweight tag that is a simple reference to a specific
``commit`` or ``object``. Yes, you do not need to tag a commit you can also
tag Blobs, Trees, etc...

.. code-block:: bash

    git tag some-object SHA
    git cat-file -p some-object

Which can be useful if you want a quick way to reference some object in the
future.

**Annotated tag**

This creates a tag that can have additional information attached to it.
Similar to a commit message. This might be useful if there are detailed
information you wish to add to the tag such as upgrade procedures or release
notes which you might want to archive in a git tag.


Code Merges: 3 types of merges
------------------------------

.. figure:: img/git-directory-merges.png
   :alt: Workspace: Merge & Rebase

   Workspace: Merge & Rebase

When working with Git there comes the eventual point in time where we need to
copy code from one branch to another. This is referred to as merging code
in Git.

In Git there are 3 distinctive ways to merge code which we will discuss:

* Fast Forward Merges
* Merge Commit
* Rebase

Contents:

.. contents::
    :local:
    :depth: 1


Cherry Pick: git cherry-pick
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Technically not a merge type but is a basic building block to copying code
from one branch to another which is effectively what merging code is doing
in Git.

.. code-block::

    git status
    git checkout -b add-new-file master

    echo "Yo" > newfile.txt
    git add newfile.txt
    git commit -s
    git status

    git checkout master
    git status

    git cherry-pick add-new-file
    git status

    git log
    git diff HEAD~1
    gitk


Fast Forward Merge: git merge --ff-only
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Merge Commit: git merge --no-ff
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


Rebasing: git rebase
^^^^^^^^^^^^^^^^^^^^


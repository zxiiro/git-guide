Git References: Branches and Tags
=================================

.. figure:: img/git-repo-branches.svg

    Branches & Tags

As mentioned earlier, Git References are stored in the ``.git/refs/*``
directory. You might know them as **branches** and **tags**.
References offer a human readable way to reference specific commits (think of
them as bookmarks).

At a rudimentary level you can create new references by simply creating files
in the ``refs/*`` directories and assigning the Commit SHA that you want to
reference. Git offers commands to handle this automatically for you.

Topics:

.. contents::
    :local:
    :depth: 1


Core References
---------------

There are 4 useful reference points one should know to effectively use Git:

.. contents::
    :local:
    :depth: 1


HEAD
^^^^

* Stored in ``.git/HEAD``
* **HEAD** is a special reference point that always points to your current
  location in the Git timeline
* Typically this is a symbolic reference to the checked out *branch*
* In ``Detached HEAD`` points to a specific commit hash
* The **HEAD** reference will move every time ``git commit`` or
  ``git checkout`` is issued


Branches
^^^^^^^^

* Stored in ``.git/refs/heads/*``
* **branches** are a human readable reference to a specific
  :term:`Commit object`
* Used in a development workflow to indicate the code path
  (development, maintanence, production)
* The **branch** reference point will move every time ``git commit`` is issued


Tags
^^^^

* Stored in ``.git/refs/tags/*``
* **tags** are human readable reference points to a specific
  :ref:`Git Object <core-concepts:The Git Object Model>`
* Tags are immutable meaning once a tag is created it should never be changed

For this reason the most common use case for tags is to reference a release so
that folks can refer back to the exact source code that built a particular
release for historical reasons. Another less common use case though for tags
is to reference specific interesting points in time. Maybe there's an
interesting lessons learned that you want to refer others to, or interesting
commit that might be interesting to reference back to for historical reasons,
we can use a tag to bookmark those commits.

The **tag** reference point is not expected to ever move.

There are 2 types of tags:

* Lightweight tag is similar to a branch and points to a single
  :ref:`Git object <core-concepts:The Git Object Model>`
* Annotated tag references a :term:`Tag object`


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


Accessing References
--------------------

You can access references using the full reference path or by their short
references.

.. code-block:: bash

    git checkout master
    git checkout heads/master
    git checkout refs/heads/master

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

When working with remotes:

.. code-block:: bash

    git checkout feature
    git checkout origin/feature
    git checkout refs/remotes/origin/master

* The last 2 commands checkout the same commit
* The first command checks out the LOCAL copy of ``feature`` branch
* If ``feature`` does not exist Git will try to guess from available remotes
* If 2 remotes have the same branch name Git won't checkout any branch


Branch and Tag commands
-----------------------

git checkout
^^^^^^^^^^^^

This is the main command we can use to copy files from the
:term:`Git Database` into our :term:`Worktree`.

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


git branch
^^^^^^^^^^

.. figure:: img/git-branch-basic.svg
    :alt: Branching

    Branching

* Use ``git branch -a`` to list all available branches including remotes
* Use ``git branch [new-branch] [reference]`` to create a new branch
* Use ``git checkout -b [new-branch] [reference]`` to create a new branch and
  checkout the branch in 1 command

.. code-block:: bash

    git branch -a

    cp .git/refs/heads/master .git/refs/heads/copy-branch
    git branch -a

    git branch new-branch master
    git branch -a

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
    # Remove the commit we just made
    git status

    git checkout master
    git add file
    git commit
    git checkout new-branch
    git status

We can see how the tracking branch affects the result of ``git status``.


git tag
^^^^^^^

Similar to branch we can create a tag easily and quickly with the ``git tag``
command.

**Lightweight tag**

.. code-block:: bash

    git tag v1.0.0

This creates a lightweight tag that is a simple reference to a specific
``commit`` or ``object``. Yes, you do not need to tag a commit you can also
tag Blobs, Trees, and Commits.

.. code-block:: bash

    git tag some-object SHA
    git cat-file -p some-object

Which can be useful if you want a quick way to reference some object in the
future.

**Annotated tag**

Reference back to the :ref:`core-concepts:Tag object` section.

.. figure:: img/git-object-tag.svg
   :alt: Commit object

   Tag object

.. code-block:: bash

    git tag -a v2.0.0

* Creates a tag that can have additional details attached
* Useful to attach additional information

  * Release notes
  * Upgrade procedures


Merging Code: 3 types of merges
-------------------------------

.. figure:: img/git-repo-merge.svg

    Merge & Rebase

When working with Git there comes the eventual point in time where we need to
copy code from one branch to another. This is referred to as merging code
in Git.

In Git there are 3 distinctive ways to merge code which we will discuss:

* Fast Forward Merges
* Merge Commit
* Rebase

Each merge type results in a branch with commits from both the source branch
and the destination branch but the order the commits appear depend on which
type of merge is used.

Contents:

.. contents::
    :local:
    :depth: 1


Cherry Pick: git cherry-pick
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Technically not a merge type but is a basic building block to copying code
from one branch to another which is effectively what merging code is doing
in Git.

Cherry-pick lets you tell Git that you want a specific commit copied to the
current ``HEAD`` ignoring the commit's *parent*.

**git cherry-pick before**

.. image:: img/git-branch-basic.svg

Let's say we want to get commit ``Z`` from the ``INFRA-123`` branch ignoring
any parents of the original commit.

.. code-block:: bash

    git checkout master
    git cherry-pick Z

**git cherry-pick after**

.. image:: img/git-branch-cherry-pick-after.svg

.. code-block:: bash

    git status
    git checkout -b add-new-file master

    echo "Yo" > newfile.txt
    git add newfile.txt
    git commit
    git status

    git checkout -b test-cherry-pick master
    git status

    git cherry-pick add-new-file
    git status

    git log
    git diff HEAD~1
    gitk


Fast Forward Merge: git merge --ff-only
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A fast forward merge is a merge that is trivial that Git does not need to worry
about managing the commit history. It is one where the branch that is merging
in already has the current ``HEAD`` as it's parent.

**ff-merge before**

.. image:: img/git-branch-ff-merge-before.svg

**ff-merge after**

.. image:: img/git-branch-ff-merge-after.svg

* ``git merge`` will perform this merge type if ``HEAD`` is the immediate
  parent
* Exact same commits are used, no commit hashes need to be updated

Reusing the previous example but instead using ``git merge --ff-only``.

.. code-block:: bash

    git status
    git checkout -b test-ff-merge master

    gitk

    git merge --ff-only add-new-file
    git status

    git log
    git diff HEAD~1
    gitk


Merge Commit: git merge --no-ff
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A merge commit happens when a commit cannot be trivially merged, meaning the
branch that is merging does not have ``HEAD`` as it's immediate parent.

**merge commit before**

.. image:: img/git-branch-basic.svg

**merge commit after**

.. image:: img/git-branch-merge-commit-after.svg

* ``git merge`` will perform this merge type if ``HEAD`` is not the immediate
  parent
* A new commit is created representing the Merge Commit
* You can force a merge commit even if a Fast-Forward commit is possible by
  explicitly passing ``git merge --no-ff``
* Typically though avoid using merge commits in Pull Request branches as those
  branches are not yet merged


Rebasing: git rebase
^^^^^^^^^^^^^^^^^^^^

A rebase is kind of like a rewind and replay function in Git. It does 3 things:

1) It undoes all of your changes in the current branch up until the common
   parent of the declared branch
2) Updates the current branch with the new changes from the declared branch
3) Replays your changes ontop of the updated current branch

**rebase before**

.. image:: img/git-branch-rebase-before.svg

**rebase after**

.. image:: img/git-branch-rebase-after.svg

Basically this kind of Git merge rewrites the history of the current branch so
should not ever be done on production branches. On work in progress branches
use rebase to make sure your work is based on the most current copy of the
relevant branch.

``git rebase -i origin/master`` is a powerful tool to edit previous commits in
a commit chain.

.. code-block:: bash

    git rebase -i origin/master


Merging Code: Resolving merge conflicts
---------------------------------------

Inevitably when working with others we will run into merge conflicts. Merge
conflicts happen when 2 commits modify the same file within 3 lines of each
other.


A simple patch
^^^^^^^^^^^^^^

.. code-block:: diff

    diff --git a/CONTRIBUTING.markdown b/CONTRIBUTING.markdown
    index cdfd6a61..9cf6b78a 100644
    --- a/CONTRIBUTING.markdown
    +++ b/CONTRIBUTING.markdown
    @@ -10,6 +10,8 @@ code review system and all contributions should be directed to there. Please
     refer to our documentation on [Submitting patches][3] for details on how to
     submit code to this project.

    +Hello World.
    +
     ## Reporting a Bug

     OpenDaylight uses [Bugzilla][5] as our issue tracking system and any feature


A conflicting patch
^^^^^^^^^^^^^^^^^^^

.. code-block:: diff

    diff --git a/CONTRIBUTING.markdown b/CONTRIBUTING.markdown
    index cdfd6a61..b8591bd0 100644
    --- a/CONTRIBUTING.markdown
    +++ b/CONTRIBUTING.markdown
    @@ -10,6 +10,8 @@ code review system and all contributions should be directed to there. Please
     refer to our documentation on [Submitting patches][3] for details on how to
     submit code to this project.

    +Conflicting patch!
    +
     ## Reporting a Bug

     OpenDaylight uses [Bugzilla][5] as our issue tracking system and any feature


git merge conflicting patch
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here we merge patch-a into patch-b ``git merge patch-a``.

.. code-block:: none

    $ git merge patch-a
    Auto-merging CONTRIBUTING.markdown
    CONFLICT (content): Merge conflict in CONTRIBUTING.markdown
    Automatic merge failed; fix conflicts and then commit the result.

    $ git status
    On branch patch-b
    Your branch is ahead of 'origin/master' by 1 commit.
      (use "git push" to publish your local commits)

    You have unmerged paths.
      (fix conflicts and run "git commit")
      (use "git merge --abort" to abort the merge)

    Unmerged paths:
      (use "git add <file>..." to mark resolution)
        both modified:   CONTRIBUTING.markdown

    no changes added to commit (use "git add" and/or "git commit -a")

.. code-block:: diff

    diff --cc CONTRIBUTING.markdown
    index b8591bd0,9cf6b78a..00000000
    --- a/CONTRIBUTING.markdown
    +++ b/CONTRIBUTING.markdown
    @@@ -10,7 -10,7 +10,11 @@@ code review system and all contribution
      refer to our documentation on [Submitting patches][3] for details on how to
      submit code to this project.

    ++<<<<<<< HEAD
     +Conflicting patch!
    ++=======
    + Hello World.
    ++>>>>>>> patch-a

      ## Reporting a Bug

* ``<<<<<<< HEAD`` is the current reference we are on
* ``=======`` separates the 2 changes
* ``>>>>>>> patch-a`` is the reference that's being merged in

There are 3 possible outcomes when deciding to resolve a merge conflict:

1) Pick the change from ``HEAD``
2) Pick the change from the reference being merged (``patch-a``)
3) A combination of the 2

Let's say we want to go with option 3, we would need to rewrite the conflicting
section and then remove the 3 markers from above.

.. code-block:: diff

    diff --git a/CONTRIBUTING.markdown b/CONTRIBUTING.markdown
    index b8591bd0..7c74583e 100644
    --- a/CONTRIBUTING.markdown
    +++ b/CONTRIBUTING.markdown
    @@ -10,7 +10,7 @@ code review system and all contributions should be directed to there. Please
     refer to our documentation on [Submitting patches][3] for details on how to
     submit code to this project.

    -Conflicting patch!
    +Hello world. But I also like conflicting patches!

     ## Reporting a Bug

The result of this is a **Merge Commit** with the resolved change. Use ``gitk``
to inspect the resulting commit timeline.


git rebase conflicting patch
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Now we merge patch-a again into patch-b using ``git rebase patch-a``.

.. code-block:: none

    $ git rebase patch-a
    Auto-merging CONTRIBUTING.markdown
    CONFLICT (content): Merge conflict in CONTRIBUTING.markdown
    error: could not apply 12553a27... Patch B
    Resolve all conflicts manually, mark them as resolved with
    "git add/rm <conflicted_files>", then run "git rebase --continue".
    You can instead skip this commit: run "git rebase --skip".
    To abort and get back to the state before "git rebase", run "git rebase --abort".
    Could not apply 12553a27... Patch B

    $ git status
    interactive rebase in progress; onto e85da853
    Last command done (1 command done):
       pick 12553a27 Patch B
    No commands remaining.
    You are currently rebasing branch 'patch-b' on 'e85da853'.
      (fix conflicts and then run "git rebase --continue")
      (use "git rebase --skip" to skip this patch)
      (use "git rebase --abort" to check out the original branch)

    Unmerged paths:
      (use "git restore --staged <file>..." to unstage)
      (use "git add <file>..." to mark resolution)
        both modified:   CONTRIBUTING.markdown

    no changes added to commit (use "git add" and/or "git commit -a")

.. code-block:: diff

    diff --cc CONTRIBUTING.markdown
    index 9cf6b78a,b8591bd0..00000000
    --- a/CONTRIBUTING.markdown
    +++ b/CONTRIBUTING.markdown
    @@@ -10,7 -10,7 +10,11 @@@ code review system and all contribution
      refer to our documentation on [Submitting patches][3] for details on how to
      submit code to this project.

    ++<<<<<<< HEAD
     +Hello World.
    ++=======
    + Conflicting patch!
    ++>>>>>>> 12553a27... Patch B

      ## Reporting a Bug

Pretty similar to the merge case except this time we see ``HEAD`` is patch-a
and ``patch-b`` is the one being merged in. This is because rebase undoes your
work, pulls in the merge branch, and then replays your commits ontop.

Once the conflict is resolved we can use ``git add [FILE]`` and
``git rebase --continue`` to complete the rebase.

The result of this is a new **Patch B** commit that contains the resolved
change instead of a **Merge Commit**. Use ``gitk`` to inspect the commit
timeline.


How to avoid merge conficts
^^^^^^^^^^^^^^^^^^^^^^^^^^^

Merge conflicts are inevitable if you are working with a team of people. You
can reduce the chances of it happening though following a few rules:

* Do not work on the same files
* If you do work on the same files, do not work in the same section

These points are not realistic in the real world however. So some better
suggestions to minimize the amount of merge conflicts.

* Keep your commits on topic, do not make unnecessary and unrelated changes
* Keep your commits small, break your larger contributions into smaller logical
  commits

This will reduce the chances of running into merge conflicts as well as makes
it easier to resolve conflicts when they do occur.

.. tip::

    Use a GUI merge tool could greatly simplify the merge resolution process.
    There's many out there to pick from so try a few and decide which one you
    like.


Git References: Key Takeaways
-----------------------------

* ``HEAD`` is your :term:`Worktree`'s current checkout
* Branches are references that automatically updates it's reference point along
  with ``HEAD``
* Tags are static references
* Remotes track branches from a remote repository
* There are 3 types of merges: Fast-Forward, Merge-Commit, and Rebase
* **Merge Conflicts** are inevitible, understanding merge order and how to
  resolve conflicts is valuable
* If you are about to do something you are unsure of, try it out on a test
  branch with ``git checkout -b test-branch REFERENCE``

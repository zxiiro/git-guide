Working with remotes
====================

.. figure:: img/git-repo-remotes.svg
   :alt: Remotes: Fetch & Pull

   Remotes: Fetch & Pull

Remotes are Git's way of allow your local :term:`Git Repository` with another
repository somewhere else, it could be another path on your computer or over
the internet. It's purpose is to allow you to get a copy of another repos
references and committed files.

* Remote references are stored in the ``refs/remotes/[NAME]/*``

  * [NAME] is a keyword you assign the remote
  * The default [NAME] is ``origin``

* Tags are expected to be the same so are stored in ``refs/tags/*``


refs/remotes vs refs/heads
--------------------------

References in ``refs/remotes/origin/*`` and ``refs/heads/*`` are not the same
even if they have the same name.

* ``git checkout feature`` copies files from ``refs/heads/feature`` to your
  :term:`Worktree`
* ``git checkout origin/feature`` copies files from
  ``refs/heads/origin/feature`` to your :term:`Worktree`
* If the local ``feature`` branch does not exist ``git checkout`` will try to
  interpret if any available remotes has the same reference branch name and
  creates a copy of that in ``refs/heads/feature`` and then copies the files
  to :term:`Worktree`

Tracking branches
^^^^^^^^^^^^^^^^^

You can tell Git to have your branch track another branch which tells
``git status`` to print additional information to you if your branch has
diverged from the tracking branch. This is useful with remotes to track if we
are missing changes in your local repo.

Typically tracking branches are setup for same named branches of local and
remote repositories.


Commit timelines of remotes vs local
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**Local master & origin/master in sync**

.. figure:: img/git-commit-timeline-remotes-basic.svg

* The local ``refs/heads/master`` branch is in sync with the remote
  ``refs/remotes/origin/master`` branch

**Fetch a remote origin with new changes**

If you ran ``git fetch origin`` and origin has new changes you might see
something like this.

.. figure:: img/git-commit-timeline-remotes-origin-new.svg

.. code-block:: bash

    cat .git/refs/heads/master
    cat .git/refs/remotes/origin/master
    git checkout master
    git checkout origin/master
    gitk origin/master

* The references are pointing at 2 different commits
* The ``master`` reference is in the commit timeline of ``origin/master``

.. code-block:: none
    :caption: git status

    On branch master
    Your branch is behind 'origin/master' by 2 commits, and can be fast-forwarded.
      (use "git pull" to update your local branch)

* This message is a little misleading, you do not need to ``git pull`` instead
  it's there's changes detected between ``master`` and ``origin/master`` that
  you have not merged yet into your local branch yet.
* We will discuss branching in more detail later but for now a
  ``git merge origin/master`` will move our branch up.
* The reason for ``git pull`` recommendation is Git wants you to do another
  ``git fetch origin`` before merging just in case there's even more changes
  your local remotes does not yet know about.

**Local branch made new changes**

In this case if you made some changes locally and have no yet pushed to origin.
The Git timeline is reversed in this situation.

.. figure:: img/git-commit-timeline-remotes-local-new.svg

.. code-block:: bash

    cat .git/refs/heads/master
    cat .git/refs/remotes/origin/master
    git checkout master
    git checkout origin/master
    gitk origin/master

* The references are pointing at 2 different commits
* The ``origin/master`` reference is in the commit timeline of ``master``

.. code-block:: none
    :caption: git status

    On branch source
    Your branch is ahead of 'origin/master' by 2 commits.
      (use "git push" to publish your local commits)

* ``git push origin master:refs/heads/master`` to push your local copy of
  ``master`` to the remote ``origin`` into the branch ``master`` on the remote
  end.
* Code changes on your copy of ``master`` is based on last parent that
  ``origin/master`` that you fetched and merged.


Git Remote Commands
-------------------

.. contents::
    :local:
    :depth: 1


git clone
^^^^^^^^^

Most folks are first introduced to Git with the ``git clone`` command as a way
of creating their Git repo for the first time.

``git clone https://example.com/repo.git`` is a convenient shortcut for:

.. code-block:: bash

    git init repo
    cd repo
    git remote add origin https://example.com/repo.git
    git fetch origin

``origin`` is the default remote name in Git so ``git clone`` initializes a
Git repo with this default remote name.


git remote
^^^^^^^^^^

Use this command to manage a remote Git repositories we are interested in
working with. While it's possible to work with remote Git repositories without
utilizing the remote command it saves us from having to type out long strings
of URLs to fetch commits from a remote repo.

The default remote in Git is called ``origin`` this is the one many Git
commands will use if you omit the *remote* paramenter in those commands.

You can have as many remotes as you like and all branch references for those
remotes will be stored in ``.git/refs/remotes/*`` in the Local Repository.

**List current remotes**

.. code-block::

    git remote -v

**Add a remote origin**

.. code-block::

    git remote add origin https://git.example.com/repo.git

For most folks we typically only work with a single remote but having multiple
is handy if you are working with multiple people who are not sharing code in
a common central repo.

**Add a remote github**

.. code-block::

    git remote add github https://github.com/example/repo.git

You might want to name your remote after the name of the service
(github, bitbucket, gerrit, etc...) or the name of the person you are
collaborating with to make it easy to remember where the remote points to.


git fetch
^^^^^^^^^

Fetching is probably the most important remote related command to utilize. It
is used to get the latest available commits from the remote repository that
you are interested in.

Ideally you should be fetching as often as possible to ensure that you are up
to date with whatever changes are available in the remote repos (imagine you
are using social media).

The most important times to fetch however are:

* Before you create a new branch based off of a remote branch
* Before you continue working on some code
* Before you push your code to a remote

.. code-block:: bash

    git fetch origin

Remember ``origin`` is the default branch. So if you call ``git fetch``
without specifying a remote, then it will assume ``origin``. Be explicit so
that you are 100% sure you are getting what you need.


git push
^^^^^^^^

Pushing allows you to make your code available to the remote repository. You
can also think of it as a way of backing up your code. You should always push
somewhere to save your work in case something happens to your local system.

The ``git push [remote] [refspec]`` command has 2 important parameters. The
first one ``remote`` being the remote repository you'd like to push your code
to, and the ``refspec`` which is a kind of branch mapping of where you'd like
your code to go to.

By default if you don't pass any parameters, ``git push`` will assume you want
to push to ``origin`` with a branch mapping of ``branch:refs/heads/branch`` so
if you were on the master branch this will be ``master:refs/heads/master``.

.. code-block:: bash

    git push
    git push origin master
    git push origin master:refs/heads/master

    git push origin HEAD:refs/heads/INFRA-123
    git push origin HEAD~2:refs/heads/INFRA-123

* Push often to backup your work in progress
* Pushing often also shows activity and that your work is not stale

Remotes: Key Takeaways
----------------------

* Branches in ``refs/remotes/[NAME]/*`` and ``refs/heads/*`` are NOT the same
  and should not be confused as such
* ``git fetch`` often to stay up to date
* ``git push`` often to backup your work-in-progress

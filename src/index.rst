#########################
Git, a follow along guide
#########################

Git is a distributed revision control system. At it's most basic level it
tracks the historical changes in contents of files over time.

It's distributed nature means everyone working on a project has their own
separate offline copy of all of the code allowing folks to work on the same
project in parallel.

Git is probably the single most important skill for anyone working in
technology today on any kind of collaborative project. If you are struggling
to use Git you will be limited in your ability to collaborate with others.

Throughout the course of this Guide, I hope to pass on some knowledge that
will help you more effectively use Git and hopefully be interesting to both
newbies as well as veterans of Git.

.. contents:: Table of Contents
	:local:
	:depth: 2


The building blocks of Git
==========================

Topics:

* The Git directory

  * Local Repository
  * Worktree (Working Directory)
  * Staging Area (Index)

* The Git Object Model

  * Commit
  * Trees
  * Blobs
  * Tags

* Demo: Working with the Git directory

  * git init
  * git add
  * git commit
  * git checkout

* Demo: Working with multiple Worktrees
* Takeaways


Overview of the Git directory
-----------------------------

.. figure:: img/git-directory-1.png
   :alt: Worktree | Staging Area | Local Repository

   Worktree | Staging Area | Local Repository


A directory containing a Git repo can contains 3 important parts:

1. Worktree (Working directory)
2. Staging Area
3. Local Repository

It is really difficult for a new user to effectively use Git until they
understand the difference between these 3 components.


Local Repository
^^^^^^^^^^^^^^^^

The ``.git`` directory contains the Git configuration and database. When
you're talking about a Git repository, this is the repository itself.

Contents:

.. code-block:: none
    :caption: ls .git

    HEAD
    config
    description
    hooks
    info
    objects
    refs

:HEAD: Contains the active checkout of your current workspace.

:config: Contains your local git configuration.

:description: Only locally significant and allows you to give your Git repo a
    name. Typically not used by users, it's mostly for server use.

:hooks: Contains scripts that can be run automatically upon certain git
    actions. Commonly ``pre-commit`` is used for things like automated linting
    and testing client-side before pushing to a remote repository for CI.

:info: Contains an ``excludes`` file which is similar to ``.gitignore``
    except it is unversioned. Useful if you want to ignore things that are only
    significant to you and no one else (such as maybe you use a different IDE
    then everyone else and don't want to pollute .gitignore with your snowflake
    environmnet). Otherwise it's better to use ``.gitignore`` in most cases.

:objects: Contains the Git **object database** itself. It is a key-value store
    and every single file you check into git exists here. This is where git
    pulls the files from when you do a ``git checkout``. Every file is a SHA
    hash.

:refs: Contains all of your references, you might know them as branches,
    tags, commits... They are essentially a bunch of SHA hashes.


Worktree (Working directory)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The worktree or working directory is where all your untracked files and work
in progress files are. When you do a ``git checkout`` you are telling Git to
copy files from the Git repository to this working area so that you can work
on them. The files are checked out in the state (or snapshot) at the reference
point you pass to the Git command.

For example ``git checkout master`` tells Git to fetch all the files from the
**master** revision and make sure the worktree's copy of all the files are
up to date with what's in the branch.


Staging Area (Index)
^^^^^^^^^^^^^^^^^^^^

The Staging area or Index is the area between your **Local Repository** and
your **Worktree**. You use this area to build up a set of changes that you
want to commit together.


The Git Object Model
--------------------

The SHA
^^^^^^^

Before we can get to the objects, it is important to understand that every Git
object is represented as a SHA1 hash in the Git database.

Everything in Git is represented by a 40 character SHA1 hash that looks
something like this ``557db03de997c86a4a028e1ebd3a1ceb225be238`` (This is
'Hello World'). This is the object name (or key in a key-value store) that Git
will use to store your contents into the :term:`Object database`.

Since SHA1 hashes are always computed exactly the same on every system, this
guarentees that the same contents are always stored with the same name in the
database and duplicate files are never stored in a Git repo.


Blob object
^^^^^^^^^^^

.. figure:: img/git-object-blob.png
   :alt: Blob object

   Blob object

A Blob object contains the complete contents of a file.

As mentioned previously, all Git objects are stored via SHA1 hash so 2 files
with the identical contents gets stored in the :term:`Object database` as the
same exact same Blob object so there can be no duplicate files.

Another thing you may notice as we go through this guide is that Git always
stores the complete contents of files into Blobs, but when you look at a Git
commit using ``git diff`` or any tools to show the commit you will see what
changed in the file instead. What Git's doing in the background is comparing
any Blob objects that changed in a commit with the previous Blob object that
it replaced.


Tree object
^^^^^^^^^^^

.. figure:: img/git-object-tree.png
   :alt: Tree object

   Tree object

A Tree object contains the complete contents of a directory.

It can contain additonal Tree objects and Blob objects. If you follow a tree
all the way down the final tree will only contain Blob objects, this is why
you cannot store just an empty directory in Git.

In other words, a Tree does not just contain the files that changed but
actually contains a list of all the files that currently exist at that
particular point in time.


Commit object
^^^^^^^^^^^^^

.. figure:: img/git-object-commit.png
   :alt: Commit object

   Commit object

A Commit object represents a particular point in time in the Git timeline.
It contains a tree, parent, author, committer, and commit message.

This is the object folks generally interact with the most in Git. You can
think of it as kind of an email. If you can imagine:

* The Tree is your attachments
* The commit message is your Subject line as well as email Body
* The rest of the info is metadata to describe where the commit came from

.. note::

    While the **author** and **committer** timestamps iare generated the first
    time a commit is created. The **committer** timestamp is updated every
    time ``git commit --amend`` is run.
    This is part of the reason why the commit SHA changes on ever amend.


Tag object
^^^^^^^^^^

.. figure:: img/git-object-tag.png
   :alt: Commit object

   Tag object

A Tag object contains supporting metadata and reference to a
:term:`Commit object`.

Tags are typically used for for things like releases to provide a pointer back
to the original codebase that produced a release. It can also be used to share
interesting points in time in a codebase.


.. note::

    You may have noticed that branches are not a basic building block of Git.
    We'll explore this further later on.


Git Objects Full Example
^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: img/git-objects-example.png
   :alt: Git Objects Full Example

   Git Objects Full Example

From here we can see how all the 4 Git Object types interact with each other:

* A Tag references a particular commit
* A Commit references both a parent commit and a Tree
* A Tree can reference another Tree as well as a Blob
* 2 files can also reference the same Blob


Demo: Working with the Git Directory
------------------------------------

Before we start there are a few low level commands we'll be using throughout
this guide to explore the Git database. You do not need to remember these
commands as they are not typically used in everyday Git use but are
useful for exploring the Git database.

.. code-block:: bash

    git cat-file -t <hash>
    git cat-file -p <hash>
    echo 'Hello World' | git hash-object
    git hash-object /path/to/file


git init
^^^^^^^^

A new git repo can be initialized with the ``git init`` command.

Example:

.. code-block:: bash

    mkdir demo
    cd demo
    git init
    ls -la

It will create a single directory in the repo named ``.git`` containing the
**Local Repository** and an empty **Worktree**. The contents of a fresh
``.git`` directory is as follows:

.. code-block:: none
    :caption: find .git
    :name: find-dot-git
    :emphasize-lines: 2-3, 6, 22-24

    .git
    .git/config
    .git/objects
    .git/objects/pack
    .git/objects/info
    .git/HEAD
    .git/info
    .git/info/exclude
    .git/description
    .git/hooks
    .git/hooks/commit-msg.sample
    .git/hooks/pre-rebase.sample
    .git/hooks/pre-commit.sample
    .git/hooks/applypatch-msg.sample
    .git/hooks/fsmonitor-watchman.sample
    .git/hooks/pre-receive.sample
    .git/hooks/prepare-commit-msg.sample
    .git/hooks/post-update.sample
    .git/hooks/pre-applypatch.sample
    .git/hooks/pre-push.sample
    .git/hooks/update.sample
    .git/refs
    .git/refs/heads
    .git/refs/tags

Throughout this guide we will be monitoriing changes to the highlighted parts
of the repo to see how commands affect changes to the **Local Repository**.

.. code-block:: bash

    cat .git/config
    cat .git/HEAD
    find .git/objects
    find .git/refs/heads
    find .git/refs/tags

The only file so far is ``.git/config`` which isn't too interesting just yet
and ``.git/HEAD`` contains a reference to ``refs/heads/master`` which does
not yet exist.


git add
^^^^^^^

The ``git add`` command is used to stage files for committing into the Git
database. The area where files are staged is referred to as the **Git Index**
(or Staging Area). The easiest way to look at the **Git Index** is to use
the ``git status`` command.

.. code-block:: bash
    :caption: Demo: git add

    git status
    touch README

    git status
    git add README

    git status
    find .git/objects

    echo 'Hello World' | git hash-object --stdin
    echo 'Hello World' > README

    git status
    git diff
    git add README

    git status
    find .git/objects

    git cat-file -p 557d

With the understanding that ``git add`` is used to stage commits. We should
try to be precise in our use of the ``git add`` command. Many newbies to Git
tend to use ``git add .`` which effectively means please stage everything in
my current directory and down. Often newbies get confused when they
unintentionally pull in changes that they did not make. Instead you should
always use ``git add /path/to/file`` and select explicitly which files you
intend to commit rather than committing everything.

The commands ``git status`` and ``git diff`` can be used to review file
changes before ``git add /path/to/file`` to stage the commit so that we can
be precise in our staging.

In a more advanced example ``git add -p /path/to/file`` can be used to select
specific changes inside of a single file for staging.

.. code-block:: bash
    :caption: Demo: git add -p

    git status
    vi README  # Prepend a header and append a footer.

    git status
    git diff
    git add -p README

    # Split, and stage only the header.

    git status
    git diff
    find .git/objects
    git cat-file <SHA>


git commit
^^^^^^^^^^

The ``git commit`` command is used to checkin your work to your
**Local Repository**. This is probably the most important command in Git and
is one of the main commands of Git.

If your work is not committed, it effectively does not exist. One way to think
of committing is to think of it as **saving** your work. You should do this
regularly and often as you work on your task.

Imagine you are working on a document in your favourite office suite on an
important document, how often do you press the save button? You should be
running ``git commit`` just as often.

Continuing from the :ref:`git add` section previously we can commit our
``README``.

.. code-block:: bash
    :caption: Demo: git commit

    git status
    git commit

    cat .git/refs/heads/master

    git status
    git diff
    find .git/objects

    # Looks look at the tree and commit objects
    git cat-file -t <SHA>
    git cat-file -p <SHA>

After committing ``refs/heads/master`` now exists and points to the latest
commit SHA that was just created.

Notice that a new Blob object is not created. The Blob object created when
we staged the file results in the same Blob object so the commit just reuses
the existing one when it creates the Tree object.

.. note::

    We will discuss the importance of the **Commit Message** in the next
    chapter.

Since this is the first commit, there is no parent commit so let's create
another commit so that we can see the parent.

.. code-block:: bash
    :caption: Demo: git commit with parent

    git status
    git diff
    git add README
    git commit README

    cat .git/refs/heads/master

    git status
    find .git/objects

    git cat-file -t <SHA>
    git cat-file -p <SHA>

Notice that ``refs/heads/master`` has moved forward to a new commit SHA.

Notice that this new commit has a parent. So when you share this commit with
others (like pushing a git commit to a remote repository) this commit will
always be based against this parent so when a remote repository merges this
commit it will be merged against this parent in the Git timeline.

**git commit --amend**

As mentioned previously it is good practice to commit often to save your work,
of course if you do this you might end up having a lot of incremental commits.
To avoid that we can instead use the ``--amend`` parameter which tells Git to
allow you to **update** your previous commit with new changes to include in
it. If you haven't shared your work with the world yet you should always
**amend** your commit until you have shared it.

Once you start sharing though there are practical situations you need to
consider when amending which we will discuss in more detail later.

.. code-block:: bash
    :caption: Demo: git commit --amend

    git status
    vi README

    git status
    git diff
    git add README
    git commit --amend

    cat .git/refs/heads/master

    git status
    git log

    find .git/objects
    git cat-file -t <SHA>
    git cat-file -p <SHA>

Notice that ``refs/heads/master`` is yet again updated with a new commit SHA.
Every time you commit you can expect ``refs/heads/master`` to move. We will
talk in more detail about this when we discuss branching.


Demo: Working with multiple Worktrees
-------------------------------------

As mentioned earlier in this chapter, the Git Worktree (Working Directory) is
where your working files are so that you can work on the files and check them
into the Git **Local Repository**.

.. note::

    This is a bit of an advanced topic but it good to know in case you
    need it. This is meant to be a basic introduction to the feature.
    Most folks can effectively use Git without ever requiring this feature.

When you create a Git repo you get one worktree in the Git directory, however
with the ``git worktree`` command it is possible to create additional
Worktrees. This is useful for those who need to work on multipel things in
parallel and don't want to disturb your editor for your existing checked out
files.

Maybe you need to work on a quick hotfix that needs to get out ASAP, Worktrees
are a great way temporarily create a new workspace.

.. code-block:: bash
    :caption: Demo: git worktree

    git worktree list
    git worktree add ../demo-hotfix
    find .git/worktrees

.. code-block:: none
    :caption: find .git/worktrees
    :emphasize-lines: 5, 9

    .git/worktrees
    .git/worktrees/demo-hotfix
    .git/worktrees/demo-hotfix/ORIG_HEAD
    .git/worktrees/demo-hotfix/commondir
    .git/worktrees/demo-hotfix/HEAD
    .git/worktrees/demo-hotfix/logs
    .git/worktrees/demo-hotfix/logs/HEAD
    .git/worktrees/demo-hotfix/index
    .git/worktrees/demo-hotfix/gitdir

Notice that a new directory is created to hold all the worktrees. Each
worktree contains metadata about the tree similar to the default Worktree.
with it's own separate HEAD and Git Index (Staging Area).

Next let's switch to the new Worktree and take a look at what's there.

.. code-block:: bash

    cd ../demo-hotfix
    find .
    cat .git

This worktree also has a .git however instead of it being a directory it is
a file containing a reference to the original Git Directory we looked at
above. From here we can see that it is sharing information with the original
repo and no duplication is happening here.

You can remove the worktree when you are done with
``git worktree remove <worktree>`` or just delete the worktree directory with
your usual commandline commands. Git will automatically clean up the metadata.


Key Takeaways
-------------

In this chapter we learned the fundamental functions of Git. The main
takeaways you should take from this chapter is try to understand.

* Git Local Repository
* Git Index (Staging Area)
* Git Worktree (Workspace)
* The Git Object Model

  * Blob object
  * Tree object
  * Commit object

We will discuss in more details about these things in later chapters.


Glossary
========

.. glossary::

    Blob object
        Represents the contents of a file.

    Commit object
        Represents a snapshot of the state and point in time in the repo
        history. Contains a :term:`Tree object`.

    Object database
        The Git database located in ``.git/objects/`` containing a key-value
        store of all the objects in Git.

    Tag object
        Represents a easy to remember reference to a particular Git Object.
        Often used to tag a :term:`Commit object`.

    Tree object
        Represents the state of files in a directory. Can contain
        :term:`Blob objects <Blob object>` and
        :term:`Tree objects <Tree object>`.

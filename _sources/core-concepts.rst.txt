Git Core Concepts
=================

Topics:

.. contents::
    :local:
    :depth: 2


The Git Repository
------------------

.. figure:: img/git-repo.svg

   Worktree | Git Index | Git Directory


The directory containing a Git repo can contains 3 important parts:

1. Worktree         (Working directory)
2. Git Index        (Staging Area)
3. Local Repository (Git Database)

It is really difficult for a new user to effectively use Git until they
understand the difference between these 3 components.

Main commands to interact with the :term:`Git Directory` include:

* ``git status`` shows the current state of the :term:`Git Repository`
* ``git add`` adds files to the :term:`Git Index`
* ``git commit`` submits the files into the :term:`Git Directory`
* ``git checkout`` pulls out files from the :term:`Git Directory`

**Creating a new Git Repository**

Create a new :term:`Git Repository` with the ``git init [PROJECT]`` command.

Example:

.. code-block:: bash

    git init demo

**Setup your Git metadata**

.. code-block:: bash

    git config --global user.name "Thanh Ha"
    git config --global user.email "thanh@example.com"

.. code-block:: none

    [user]
        name = Thanh Ha
        email = thanh@example.com


Worktree
^^^^^^^^

The Worktree or working directory is where all your checked out files reside.
This is the space where you do work on files. When you do a ``git checkout``
you are telling Git to copy files from the :term:`Git Directory` to this
working area so that you can work on them. A snapshot of the files are checked
out from the reference point that you pass to the ``git checkout REFERENCE``
command.

For example ``git checkout master`` tells Git to fetch all the files from the
reference point that **master** is currently pointing to.


Git Index
^^^^^^^^^

The Git Index or staging area is where you can stage files in preparation to
commit into the :term:`Git Database`. You can use ``git add FILE`` to take a
file from the :term:`Worktree` and copy it into the staging area. You use the
staging area to build up a set of changes that you want to commit together.

For example ``git add README`` tells Git to copy the README file from the
:term:`Worktree` and put it into the Git Index. Keyword here is *copy* because
even after you add the file it is still possible to edit the file without
affecting the copy in the Git Index.


Git Directory
^^^^^^^^^^^^^

The ``.git`` directory contains the Git configuration and database. When
you are talking about committing code to Git, this is where the code is stored.

Contents:

.. code-block:: none
    :emphasize-lines: 1-2, 6-7

    HEAD
    config
    description
    hooks
    info
    objects
    refs

:HEAD: Contains the active reference point of your current workspace. This
    could be a SHA or a reference to another reference inside the ``refs``
    directory.

:config: Contains your local Git configuration for this repo. You can put any
    repo specific configurations here if they differ from the global Git
    config.

:description: Only locally significant and allows you to give your Git repo a
    description. Typically not used by users, it's mostly for server use.

:hooks: Contains scripts that can be run automatically upon certain Git
    actions. Commonly ``pre-commit`` is useful for things like automated
    linting and testing client-side before pushing to a remote repository to
    trigger CI.

:info: Contains an ``excludes`` file which is similar to ``.gitignore``
    except it is not saved in the :term:`Git Database` so does not get shared
    with others. Useful if you want to ignore things that are only significant
    to you and no one else (such as maybe you use a different IDE then everyone
    else and don't want to pollute ``.gitignore`` with your snowflake
    environmnet). Otherwise it's better to use ``.gitignore`` in most cases.

:objects: Contains the Git **object database** itself. It is a key-value store
    and every single file you commit into Git exists here. This is where Git
    pulls the files from when you do a ``git checkout``. Every file is a SHA
    hash that acts as the key and the contents of the file is the value in the
    key-value store.

:refs: Contains all of your references, you might know them as branches and
    tags.

    * ``refs/heads/*`` is where all the branches are stored
    * ``refs/tags/*`` is where all the tags are stored
    * ``refs/remotes/[REMOTE]/*`` is where remote branches are stored

    They are essentially a bunch of pointers to SHA hashes that allow you to
    pull from the Git object database.


The Git Object Model
--------------------

The SHA
^^^^^^^

Before we can get to the objects, it is important to understand that every Git
object is represented as a SHA1 hash in the :term:`Git Database`.

Everything in Git is represented by a 40 character SHA1 hash that looks
something like this ``557db03de997c86a4a028e1ebd3a1ceb225be238`` (This is
'Hello World'). This is the object name (or key in a key-value store) that Git
will use to store your contents into the :term:`Git Database`.

Since SHA1 hashes are always computed exactly the same on every system, this
guarentees that the same contents are always stored with the same name in the
database and duplicate files are never stored in a Git repo.

.. note::

    This is also how Git can detect if you have files that are corrupt,
    basically if the contents of the files no longer match up with the SHA1
    hash in the database Git will report that the file has been tampered with
    and will consider your database corrupt.


Blob object
^^^^^^^^^^^

.. figure:: img/git-object-blob.svg
   :alt: Blob object

   Blob object

A Blob object contains the complete contents of a file.

As mentioned previously, all Git objects are stored via SHA1 hash so 2 files
with the identical contents gets stored in the :term:`Git Database` as the
same exact same Blob object so there can be no duplicate files.

Another thing you may notice as we go through this guide is that Git always
stores the complete contents of files into Blobs, but when you look at a Git
commit using ``git diff`` or any tools to show the commit you will see what
changed in the file instead. What Git's doing in the background is comparing
any Blob objects that changed in a commit with the previous Blob object that
it replaced.


Tree object
^^^^^^^^^^^

.. figure:: img/git-object-tree.svg
   :alt: Tree object

   Tree object

A Tree object contains the contents of a directory.

It is a mapping of Tree and Blob objects to filenames. If you follow a tree all
the way down the final tree will only contain Blob objects, this is why you
cannot store just an empty directory in Git.

When you do a ``git checkout`` of a commit. Git will use the Tree to fetch all
of the files the commit represents into your :term:`Worktree`.


Commit object
^^^^^^^^^^^^^

.. figure:: img/git-object-commit.svg
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

    While the **author** and **committer** timestamps are generated the first
    time a commit is created. Only the **committer** timestamp is updated every
    time ``git commit --amend`` is run.
    This is part of the reason why the commit SHA changes on ever amend a
    commit.


Tag object
^^^^^^^^^^

.. figure:: img/git-object-tag.svg
   :alt: Commit object

   Tag object

Also known as an annotated Tag, the Tag object contains supporting metadata
and reference to a :term:`Commit object`.

Tags are typically used for for things like releases to provide a pointer back
to the original codebase that produced a release. It can also be used to share
interesting :ref:`Git Objects <core-concepts:The Git Object Model>`, perhaps a
particular commit of interest or a useful file from the repo.


Git Objects Full Example
^^^^^^^^^^^^^^^^^^^^^^^^

.. figure:: img/git-objects-example.svg
   :alt: Git Objects Full Example

   Git Objects Full Example

From here we can see how all the 4 Git Object types interact with each other:

* A Tag references a particular commit
* A Commit references both a parent commit and a Tree
* A Tree can reference another Tree as well as a Blob
* 2 files can also reference the same Blob

.. note::

    You may have noticed that branches are not a basic object of Git.
    Branches are basically a human readable alias to a :term:`Commit object`.

Below is an example of a simplified Git Commit view which shows a basic
timeline which we will build upon later on.

.. figure:: img/git-commit-timeline.svg
   :alt: Git Commit timeline

   Git Commit timeline

* Git is a history tracking tool meaning every commit that has parent commit
  is an ancestor of a previous commit
* Following the parents you can trace the entire change history of a project
* Storing large binary objects in Git is bad practice because the history
  will maintain a copy of every version of all files that ever existed
* There is no ``delete`` once a file is committed to the :term:`Git Database`


Demo: Working with the Git Directory
------------------------------------

Before we start there are a few low level commands we'll be using throughout
this guide to explore the Git database. You do not need to remember these
commands as they are not typically used in everyday Git but are useful for
exploring the :term:`Git Database`.

.. code-block:: bash

    git cat-file -t <hash>
    git cat-file -p <hash>
    echo 'Hello World' | git hash-object
    git hash-object /path/to/file

Commands:

.. contents::
    :local:
    :depth: 1


git status
^^^^^^^^^^

* Use the ``git status`` command to view the state of the Git :term:`Worktree`
  and :term:`Git Index`.


git add
^^^^^^^

* Use the ``git add`` command to stage files into the :term:`Git Index`
  to prepare for committing into the :term:`Git Database`.
* Be precise and avoid using ``git add .`` which means to stage everything.
* Instead use ``git add path/to/file``.
* Use the ``git status`` command to view the :term:`Git Index`.
* Use ``git diff`` to review file changes before staging.

.. code-block:: bash

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

In a more advanced example ``git add -p path/to/file`` can be used to select
specific changes inside of a single file for staging.

.. code-block:: bash

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

* Use the ``git commit`` command to checkin your work into the
  :term:`Git Database`.
* This is probably the most important command in Git.
* If your work is not committed, it effectively does not exist.
* Think of committing as **saving** your work.

Continuing from the :ref:`core-concepts:git add` section previously we can
commit our ``README``.

.. code-block:: bash

    git status
    git commit

    cat .git/HEAD
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

Since this is the first commit, there is no parent commit so let's create
another commit so that we can see the parent.

.. code-block:: bash

    git status
    # Make changes to the README

    git status
    git diff
    git add README
    git commit

    cat .git/HEAD
    cat .git/refs/heads/master

    git status
    find .git/objects

    git cat-file -t <SHA>
    git cat-file -p <SHA>

* Notice that ``refs/heads/master`` has moved forward to a new commit SHA.
* Notice that this new commit has a parent.

When you share this commit with others (like pushing to a remote repository)
this commit will always be based against this parent so when a remote
repository merges this commit it will be merged against this parent in the Git
timeline.

**git commit --amend**

As mentioned previously it is good practice to commit often to save your work,
of course if you do this you might end up having a lot of incremental commits.
To avoid that we can instead use the ``--amend`` parameter which tells Git to
allow you to **update** your previous commit with new changes to include in
it. If you have not shared your work with the world yet you should always
**amend** your commit until you are ready to shared it.

Once you start sharing though there are practical situations you need to
consider when amending which we will discuss in more detail later.

.. code-block:: bash

    git status
    # Make changes to the README

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

* Notice that ``refs/heads/master`` is yet again updated with a new commit SHA.
* Every time you commit you can expect ``refs/heads/master`` to move the SHA.


git checkout
^^^^^^^^^^^^

* Use the ``git checkout`` command to copy files from the :term:`Git Database`
  into your :term:`Worktree`.
* Checkout a specific file from a commit by passing ``-- path/to/file``.
* Pass the ``-f`` flag to replace modified files.

Try some of these in your own repos:

.. code-block:: bash

    git checkout HEAD
    git checkout master
    git checkout master -- path/to/file
    git checkout [HASH] -- path/to/file
    git checkout -f master


Demo: Working with multiple Worktrees
-------------------------------------

As mentioned earlier, the Git :term:`Worktree` is where your working files are.

.. note::

    This is a bit of an advanced topic but it good to know in case you
    need it. This is meant to be a basic introduction to the feature.
    Most folks can effectively use Git without ever requiring this feature.

When you create a Git repo you get one :term:`Worktree` in the
:term:`Git Repository`, however with the ``git worktree`` command it is
possible to create additional :term:`Worktrees <Worktree>` for parallel
development. This is useful for those who need to work on multiple things in
parallel and if you do not  want to disturb your editor for your existing
checked out files.

Maybe you need to work on a quick hotfix that needs to get out ASAP,
:term:`Worktrees <Worktree>` are a great way temporarily create a new
workspace.

.. code-block:: bash

    git worktree list
    git worktree add ../demo-hotfix
    find .git/worktrees

:term:`Worktree` configuration directory:

.. code-block:: none
    :emphasize-lines: 5, 8-9

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
:term:`Worktree` contains metadata about the tree similar to the default
:term:`Worktree` and has it's own separate ``HEAD`` reference and
:term:`Git Index`.

Next let's switch to the new Worktree and take a look at what's there.

.. code-block:: bash

    cd ../demo-hotfix
    find .
    cat .git

This worktree also has a ``.git`` however instead of it being a directory it is
a file containing a reference to the original :term:`Git Directory` we looked
at above. From here we can see that it is sharing information with the original
repo and no duplication is happening here.

You can remove the :term:`Worktree` when you are done with
``git worktree remove <worktree>`` or just delete the worktree directory with
your usual commandline commands. Git will automatically clean up the metadata.


Git Core Concepts: Key Takeaways
--------------------------------

In this section we learned the fundamental functions of Git. The main
takeaways you should take from this chapter is try to understand.

* :term:`Git Repository`

    * :term:`Git Directory` (:term:`Git Database`)
    * :term:`Git Index` (Staging Area)
    * :term:`Worktree` (Workspace)

* :ref:`core-concepts:The Git Object Model`

  * :ref:`core-concepts:Blob object`
  * :ref:`core-concepts:Tree object`
  * :ref:`core-concepts:Commit object`

* Git Commands

  * :ref:`core-concepts:git status`
  * :ref:`core-concepts:git add`
  * :ref:`core-concepts:git commit`
  * :ref:`core-concepts:git checkout`

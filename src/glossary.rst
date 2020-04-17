Glossary
========

.. glossary::

    Blob object
        Represents the contents of a file.
        Reference :ref:`core-concepts:Blob object`.

    Commit object
        Represents a snapshot of the state and point in time in the repo
        history. Contains a :term:`Tree object`.
        Reference :ref:`core-concepts:Commit object`.

    Git Directory
        This is the ``.git`` folder in your :term:`Git Repository`.
        Reference :ref:`core-concepts:Git Directory`.

    Git Database
        The Git Object storage area ``.git/objects/`` is a key-value store
        containing all of the Git objects.

    Git Index
        The staging area where you can prepare files before they are committed
        into the :term:`Git Database`.
        Reference :ref:`core-concepts:Git Index`.

    Git Repository
        Reference: ref:`core-concepts:Git Repository`.

    Tag object
        Represents a reference to a particular Git Object.
        Often used to tag a :term:`Commit object`.
        Reference :ref:`core-concepts:Tag object`.

    Tree object
        Represents the files in a directory. Can contain
        :term:`Blob objects <Blob object>` and
        :term:`Tree objects <Tree object>`.
        Reference :ref:`core-concepts:Tree object`.

    Worktree
        The working directory where Git files are checked out to. This is where
        you modify and update files before staging the files into your
        :term:`Git Index`.
        Reference :ref:`core-concepts:Worktree`.

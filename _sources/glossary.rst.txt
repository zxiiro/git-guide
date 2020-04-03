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

    Worktree
        A directory containing the checked out files from a Git repository.
        This is typically where you modify and update files before checking
        in your changes to the Git repo.

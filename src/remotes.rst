Working with remotes
====================

.. figure:: img/git-directory-remotes.png
   :alt: Remotes: Fetch & Pull

   Remotes: Fetch & Pull

Topics:

.. contents::
    :local:
    :depth: 2


Git Remote Commands
-------------------

git clone
^^^^^^^^^

Most folks are first introduced to Git with the ``git clone`` command as a way
of creating their Git repo for the first time.

``git clone https://example.com/repo.git`` is a convenient shortcut for:

.. code-block:: bash

    git init repo
    cd repo
    git remote add origin https://example.com/repo.git

``origin`` is the default remote name in Git so ``git clone`` initializes a
Git repo with this default remote name.

In the next section we will discuss ``git remote`` in more detail.


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

Ideally you should be fetching as often as possible (imagine you are using
social media, you want the latest newsfeed information all the time) to ensure
that you are up to date with whatever changes are available in the remote
repos.

The most important times to fetch however are:

* Before you create a new branch
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
can also think of it as a way of backing up your code, think of pushing as
hitting ctrl+s in your editor. You should always push somewhere to save your
work in case something happens to your local system.

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


Git Workflows
-------------

In my experience with Git I have seen 3 types of workflows developers might
use to collaborate on a project.

.. contents::
    :local:
    :depth: 1


Email Workflow
^^^^^^^^^^^^^^

This is the workflow utilized by the Linux Kernel project. Git was designed
with email in mind.

Pros:

* Requires less infrastructure
* No account required

Cons:

* Uncommon workflow
* Not easy to review without specialized tools

The email workflow is also a really handy way to share work with colleagues
without needing to setup any specific infrastructure or if you are stuck
behind a firewall that's blocking your remote repos this can get around that.

Workflow Commands:

.. contents::
    :local:
    :depth: 1


git format-patch
""""""""""""""""

This command is used to create a ascii based ``*.patch`` files containing your
commits. One commit per patch file and each patch file is in unix mailbox
format (basically an email).

.. code-block:: bash

    git format-patch [reference]
    git format-patch origin/master

When using this command ``git format-patch`` will create patch files for all
commits since the reference point. The file names contain the numerical order
the patches should be merged in.

.. code-block:: none

    0001-Update-homepage.patch
    0002-Import-jobs-from-project-config.patch
    0003-Fix-gerrit-code-review-plugin-name.patch
    0004-Enable-docs-linkcheck.patch
    0005-Add-support-for-opsgenie-notification-plugin.patch
    0006-Experimental-support-for-filterChecks-trait.patch
    0007-Fix-authorization-property-issue.patch
    0008-Update-Jenkins-wiki-plugins-URLs.patch
    0009-Update-Jenkins-wiki-plugins-URLs-builders.patch
    0010-Fix-links-causing-redirects.patch
    0011-Update-Jenkins-wiki-plugins-URLs.patch
    0012-Update-Jenkins-wiki-plugins-URLs-parameters.patch
    0013-Update-Jenkins-wiki-plugins-URLs.patch
    0014-Ignore-py-obj-warnings-and-fail-on-warnings.patch
    0015-Re-order-some-XML-attributes-to-preserve-ordering.patch
    0016-Fix-some-typos-in-documentation.patch
    0017-conditional-publisher-sort-publisher-attributes-alph.patch
    0018-Adding-view-for-the-Delivery-Pipeline-Plugin.patch
    0019-Add-support-for-become-in-ansible-playbook.patch
    0020-Fix-zuul-parameters-anchor-link.patch

With these patches you can attach them to an email and send it out to the team.


git apply
"""""""""

Git apply takes a ``*.patch`` file and applies the file changes to the repo.
This command ignores any commit messages and metadata as it is only concerned
about file changes. It is better to use the ``git am`` command instead to
apply commit patches.


git am
""""""

This command takes ``*.patch`` files in mailbox format and merges the commits
to the current branch.

.. code-block:: bash

    git am *.patch


Pull Request Workflow
^^^^^^^^^^^^^^^^^^^^^

The Pull Request (PR) Workflow was popularized by GitHub and is used in
services such as BitBucket and GitLab as well.

Typically in the PR Workflow we would work on a side-branch for the task at
hand and push this side branch to a remote such as GitHub to share with the
project.

Pros:

* Most common workflow
* Arguably easier workflow

Cons:

* Encourages bad practices (undescriptive commit messages)
* Messy commit history
* Difficult for collaborators to update your PR

**Creating a new PR**

.. code-block:: bash

    git fetch origin
    git checkout -b mywork origin/master

    # edit files

    git add path/to/files
    git commit
    git push origin mybranch

    # In GitHub / BitBucket UI create a Pull Request using mybranch

**Updating an existing PR**

.. code-block:: bash

    git checkout mywork

    # edit files

    git add path/to/files
    git commit
    git push origin mybranch


Patchset Workflow
^^^^^^^^^^^^^^^^^

This workflow is what's used in Gerrit. In this workflow we are contributing
a single commit as a **Patchset** for review. Updates to the code are done
via amending the one commit until we reach an acceptable **Patchset***.

Pros:

* More precise commit messages
* Cleaner Git History
* Rebasing is easier

Cons:

* Less common workflow
* More commands to learn (rebase, commit --amend)


Typical workflows:

**Creating a new commit**

.. code-block:: bash

    # Edit some files
    git add path/to/file
    git commit
    git push origin HEAD:refs/for/master

If you are using the *git-review* tool, the command ``git review master`` is
equivalent to ``git push origin HEAD:refs/for/master``.

**Updating an existing review**

.. code-block:: bash

    git fetch origin refs/changes/34/88734/1
    git checkout FETCH_HEAD

    # Update files as necessary

    git add path/to/files
    git commit --amend       # Make sure Change-Id in footer matches in Gerrit
    git push origin HEAD:refs/for/master

If you are using *git-review* tool, the command ``git review -d 88734,1`` is
equivalent to ``git fetch origin refs/changes/34/88734/1``.

It is considered good practice to redownload your change every time you work
on it in Gerrit because other team members could updaet your code since you
last worked on it. If you are 100% sure you are the only one that's worked on
it since last time you can skip the fetch component.


Resolving merge conflicts
-------------------------


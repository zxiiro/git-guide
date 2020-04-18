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

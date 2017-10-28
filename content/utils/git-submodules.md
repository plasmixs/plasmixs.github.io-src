Title: Git submodules
Date: 2013-10-06 12:42
Tags: Git
Slug: git-submodules
Status: published

Git submodules are useful to organize and associate related git
repositories.
Consider a project which has a source repository containing app codes,
master makefiles and libraries. This repository is self-sufficient and
maintains its own history.

Now the app is redesigned in such a way that the core part of the app is
made into a library. The library compilation needs to be triggered from
the master makefile located in the source repository. The master
makefile exports the necessary environment variables required for the
library compilation. Hence this library exhibits a parasitic
relationship with the source repository.
It would make sense to host this library in a separate git repository.
The advantage is that the library repository could be made as a
submodule and made available to different projects (different git
repositories). The separation allows independent repository (and its
history) management also.

### Git submodule add

A new clone of the app source is created and inside this clone the
library repository is linked via git submodule. The modifications are
done in a new clone so as to maintain a untainted version of the source.
Once the modifications are done in the clone it would be pushed to the
source repository but this time only the references to the submodule
would be present instead of the submodule contents.
Similarly whenever a new clone is created from the source repository,
only the submodule references are present. In order to obtain the
contents of the source module the submodules needs to be 'updated' or
rather synced. This is done explicitly via the git submodule commands,
which will be discussed later.

A new submodule can be added by the git command ***git submodule
add***.
Here in this example the external library is added as a submodule to
the app source.

    :/Work/Contents/git/checkout/src> git submodule add file:///Work/Contents/git/repo/ext_lib/
    Cloning into 'ext_lib'...
    remote: Counting objects: 3, done.
    remote: Compressing objects: 100% (2/2), done.
    remote: Total 3 (delta 0), reused 0 (delta 0)
    Receiving objects: 100% (3/3), done.

    :/Work/Contents/git/checkout/src>; ls
    app  ext_lib  makefile

The submodule command ***git submodule summary*** displays the summary
for this app source clone.

    /Work/Contents/git/checkout/src> git submodule summary
    * ext_lib 0000000...c87b13d (1):
      > Initial commit

The summary mentions ext_lib and also displays the hash which is
selected for the submodule. It also displays the commit message related
to the hash.
Note: As a best practise, it is often recommended to have a separate
branch on the submodule and reference that branch during submodule
create. This can be specified in the -b option of git submodule add
command.

The git status revels that following:

    /Work/Contents/git/checkout/src> git status
    # On branch master
    # Changes to be committed:
    #   (use "git reset HEAD ..." to unstage)
    #
    #       new file:   .gitmodules
    #       new file:   ext_lib
    #

The ext_lib submodule is tracked as a whole repository. The files
inside ext_lib are not tracked individually by the app source. This
means that once a file inside ext_lib is modified locally git status of
app source will show ext_lib as being modified.
A new file .gitmodules is created on submodule add. This file contains
the binding between the submodule and the app source.

### .gitmodules file

As mentioned earlier the .gitmodules file maintains the binding between
the submodule and the app sources.
The contents of the .gitmodules file in this example:

    /Work/Contents/git/checkout/src> cat .gitmodules
    [submodule "ext_lib"]
            path = ext_lib
            url = file:///Work/Contents/git/repo/ext_lib/

### git commit and push/pull

The git add command followed by git commit can then be issued which
would add the submodules to the source tree.This is then pushed to the
remote repository.This action assures that the submodules addition is
reflected in the remote repo and any new clone of this repo will reflect
the submodules.

    /Work/Contents/git/repo/src> git pull file:///Work/Contents/git/checkout/src/
    From file:///Work/Contents/git/checkout/src
     * branch            HEAD       -> FETCH_HEAD
    Updating 6011b5d..13d3e03
    Fast-forward
     .gitmodules | 3 +++
     ext_lib     | 1 +
     2 files changed, 4 insertions(+)
     create mode 100644 .gitmodules
     create mode 160000 ext_lib

    :/Work/Contents/git/repo/src> ls ext_lib/
    :/Work/Contents/git/repo/src>

Note: The contents inside the ext_lib are not populated by default.They
have to be explicitly synced as below:

### Git submodule init and update

The contents of the ext_lib needs to be explicitly populated using the
submodule init and update commands.

The ***git submodule init*** initialize the submodules i.e it adds the
submodule reference in the .git/config file. Shown below are the
contents of .git/config file before and after the submodule init
command.

    :/Work/Contents/git/new_checkout/src> cat .git/config
    [core]
            repositoryformatversion = 0
            filemode = true
            bare = false
            logallrefupdates = true
    [remote "origin"]
            url = file:///Work/Contents/git/repo/src/
            fetch = +refs/heads/*:refs/remotes/origin/*
    [branch "master"]
            remote = origin
            merge = refs/heads/master
    :/Work/Contents/git/new_checkout/src> git submodule init
    Submodule 'ext_lib' (file:///Work/Contents/git/repo/ext_lib/) registered for path 'ext_lib'
    :/Work/Contents/git/new_checkout/src> cat .git/config
    [core]
            repositoryformatversion = 0
            filemode = true
            bare = false
            logallrefupdates = true
    [remote "origin"]
            url = file:///Work/Contents/git/repo/src/
            fetch = +refs/heads/*:refs/remotes/origin/*
    [branch "master"]
            remote = origin
            merge = refs/heads/master
    [submodule "ext_lib"]
            url = file:///Work/Contents/git/repo/ext_lib/

The contents of ext_lib are populated only when the ***git submodule
update*** command is issued. This needs to be done only after submodule
init.

    :/Work/Contents/git/new_checkout/src> git submodule update
    Cloning into 'ext_lib'...
    remote: Counting objects: 3, done.
    remote: Compressing objects: 100% (2/2), done.
    remote: Total 3 (delta 0), reused 0 (delta 0)
    Receiving objects: 100% (3/3), done.
    Submodule path 'ext_lib': checked out 'c87b13d4c88f78a2c23f1be0ab40961a59e77444'
    :/Work/Contents/git/new_checkout/src> ls ext_lib/
    lib.c  makefile

The contents of the ext_lib are now available and the app source
repository can be used for building the application in parallel to the
ext_lib. If a separate branch of the ext_lib is referenced in the
submodule command than app source can be developed independently of the
ext_lib development. Any recent changes will not affect the app source
until the branch is updated (merged) with the recent changes.

### Git Sub Module References

1.  http://git-scm.com/docs/git-submodule
2.  http://git-scm.com/book/en/Git-Tools-Submodules

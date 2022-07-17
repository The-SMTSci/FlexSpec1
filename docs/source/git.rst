GIT
===

To join a Github project:
Create an account with Github. They are free, but you can pay for more.
Make sure to "Edit Profile" and add the email address you wish to recieve
invitations.

Git is a version control system. It manages revision histories of files in a *repository*.

Github is a website/service that will manage a copy of your repository should
you wish to do so. 

Basics of Git
-------------

You have a top-level directory. Under the top-level, you may divide
your files into documents, spreadsheets, source code, images,
reference papers etc.

At some point you are ready to make a *snapshot* version of one or more
related files. The goal is make backup and to be easily be able to 
manage those backups.

Git maintains a hidden/secret directory under its toplevel directory
called ".git". This is where all the backup files and all the book-keeping
associated with the project and the saved files reside.


A local repo may be made in a few ways: 

#. If you want to use a cloud based method, use your Github account,
   create a new private repo and clone that to your local machine.

#. Use the command *git --init bare MyDirName*, cd to MyDirName, and
   have at it.

#. Cd into a current directory. Set up a few .gitignore files, clean house
   and *git clone init --bare .*

A new file, unknown to git as to be **ADDED** so, *git add myfile*.

If you create a new file during the course of developement it must
be added when it is ready to have its first snapshot backup recorded

No backups are made until you use the *git clone* command. All files staged
(added) are then tagged with the same message and copied into the local
repo's secret tree.

If this repo is **clone** of some remote repo, then you must use the command
*git push* to copy/merge all changes you made into the **main** tree. This
sometimes causes a bit of greif when working as a team and using the single
remote repository as the collection point. Resource on the web explain and
help with these issues.

Summary
-------


Git is great for teams. It may exclude intermediate files like the ".o" object
files from compile steps, or the plethora of intermediate Latex files for
a documentation project. No need to save these, they are regenerated each
time.

Don't use github as a way to manage astronomical images. They are huge and
should never change anyway. Use something like Google Drive for that storage.

You may save one or two images that are critical test images.




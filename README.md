The file checktrailing.py is a python module compatible with the [mercurial API](https://www.mercurial-scm.org/wiki/MercurialApi) that can be called via [commit hooks](https://www.mercurial-scm.org/wiki/HookExamples) to prevent commits with files that contain trailing whitespace.

This module was inspired by [checkfiles.py](https://www.mercurial-scm.org/wiki/CheckFilesExtension) which is more fully featured.

This module has been tested with Mercurial versions:
* 3.9.2

# Configuration

Edit your project or global hgrc and add the following lines to enable the hooks.

    [hooks]
    pretxnchangegroup.checktrailing = python:/path/to/checktrailing.py:checktrailing
    pretxncommit.checktrailing = python:/path/to/checktrailing.py:checktrailing

# Sample Output

    Trailing whitespace detected in changeset:24 file:src/MyClass.java:
            3:         System.out.println("test trailing space");
            4:         System.out.println("test trailing tab");
    transaction abort!
    rollback completed
    abort: pretxncommit.checktrailing hook failed

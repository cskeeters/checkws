# Detects trailing whitespace and DOS EOL in files
#
# Copyright: Chad Skeeters 2016

# See https://bitbucket.org/cskeeters/checkws for documentation

import re

def deleted(changectx, filepath):
    try:
        # This should throw a ManifestLookupError if the file was removed
        filectx = changectx[filepath]

        if filectx == None:
            return True

    except LookupError as ex:
        #print(type(ex).__name__, ex.args)
        return True

    return False

# Older versions of mercurial don't have filectx.isbinary
def isbinary(filectx):
    return '\0' in filectx.data()

def has_dos(filectx):
    p=re.compile('\s+$', re.IGNORECASE)

    detected_dos = False
    data = filectx.data()
    lines = data.split('\n')
    for i in xrange(0, len(lines)):
        if lines[i].endswith("\r"):
            detected_dos = True
    if detected_dos:
        print("DOS EOL detected in changeset:%s file:%s:" % (filectx.changectx().rev(), filectx.path()))
    return detected_dos


def has_trailing(filectx):
    p=re.compile('\s+$', re.IGNORECASE)

    detected_trailing_ws = False
    data = filectx.data()
    lines = data.splitlines()
    for i in xrange(0, len(lines)):

        m=p.search(lines[i])
        if m != None:
            if not detected_trailing_ws:
                print("Trailing whitespace detected in changeset:%s file:%s:" % (filectx.changectx().rev(), filectx.path()))

            print("    %6i: %s" % (i+1, lines[i]))
            detected_trailing_ws=True
    return detected_trailing_ws

def checktrailing(ui, repo, hooktype, node=None, **kwargs):
    if hooktype not in ['pretxnchangegroup', 'pretxncommit']:
        ui.write('Hook should be pretxncommit/pretxnchangegroup not "%s".' % hooktype)
        return 1

    abort = False

    for rev in xrange(repo[node], len(repo)):
        change_ctx = repo[rev]
        #print("Checking changeset %i" % change_ctx.rev())
        for filename in change_ctx.files():
            if not deleted(change_ctx, filename):
                filectx = change_ctx.filectx(filename)
                if not isbinary(filectx):
                    #print("Checking changed text file %s" % filename)
                    if has_trailing(filectx):
                        abort = True

    return abort

def checkdos(ui, repo, hooktype, node=None, **kwargs):
    if hooktype not in ['pretxnchangegroup', 'pretxncommit']:
        ui.write('Hook should be pretxncommit/pretxnchangegroup not "%s".' % hooktype)
        return 1

    abort = False

    for rev in xrange(repo[node], len(repo)):
        change_ctx = repo[rev]
        #print("Checking changeset %i" % change_ctx.rev())
        for filename in change_ctx.files():
            if not deleted(change_ctx, filename):
                filectx = change_ctx.filectx(filename)
                if not isbinary(filectx):
                    #print("Checking changed text file %s" % filename)
                    if has_dos(filectx):
                        abort = True

    return abort

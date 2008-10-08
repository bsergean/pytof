#!/usr/bin/env python

import os, sys
from email.utils import parseaddr
from os.path import expanduser, join, exists, isdir, basename
from adobe_directory import create_local_directory, Employee

maildir = join(expanduser('~'),'bine_mails')
maildir_cur = join(maildir, 'cur')
maildir_vi = join(maildir, 'vi')

def setup():
    for d in [maildir, maildir_vi, maildir_cur]:
        if not exists(d): 
            os.mkdir(d)

def fetchmail():
    import poplib

    M = poplib.POP3('namail.corp.adobe.com')
    M.user('bsergean')
    passwd = os.getenv('PASSWD')
    if passwd == None:
        import getpass
        passwd = getpass.getpass()
    M.pass_(passwd)

    nb_messages = len(M.list()[1])

    for i in xrange(1, nb_messages+1):
        sys.stderr.write('.')

        fn = join(maildir, 'cur', str(i))
        if exists(fn): continue
        fo = open(fn, 'w')

        for j in M.retr(i)[1]: 
            print >>fo, j 

        fo.close()

    print

# Great spam detector
def is_from_adobe(name):
    name, mail = parseaddr(name)
    if not mail: return False
    login = mail.split('@')[0]

    if login in ['bsergean', 'bnoble']: return False
    if login in ['luc']: return True
    return login in map_login

def real_name(mail):
    return parseaddr(mail)[0]

def nice_link(f, N, mail_info):
    # Create a link for nice vi browsing 
    pad_size = len(str(N))
    vibn = f.rjust(pad_size, '0')

    import string
    clean_mail_info = [c for c in mail_info if not c in string.punctuation]
    clean_mail_info = ''.join(clean_mail_info)

    vifn = join(maildir_vi, vibn + ' ' + clean_mail_info)
    fn = join(maildir, 'cur', f)
    if exists(vifn): return
    os.link(fn, vifn)

def nb_files_in_dir(d):
    return len([f for f in os.listdir(d)])

def walk_mails(d):
    os.chdir(d)
    mails = sorted([(int(f), f) for f in os.listdir('.')])
    return (tuple[1] for tuple in mails)

def parse_mail(f):
    from email.parser import Parser
    p = Parser()
    fo = open(f)
    msg = p.parse(fo, True) # True for parsing header only
    fo.close()
    return msg

def parse_maildir():
    import mailbox
    # Manual parsing because I need to know the filename associated with the 
    # message and I cannot do that with Maildir module

    maildir_cur = join(maildir, 'cur')
    mails = walk_mails(maildir_cur)
    N = nb_files_in_dir(maildir_cur)
    
    for f in mails:
        msg = parse_mail(f)

        mail = msg.get('From')
        if is_from_adobe(mail):
            mail_info = ' %-22s - %s' % (real_name(mail), msg.get('Subject'))
            nice_link(f, N, mail_info)

def parse_maildir_vi():
    import mailbox
    # Manual parsing because I need to know the filename associated with the 
    # message and I cannot do that with Maildir module

    mails = walk_mails(maildir_vi)
    N = nb_files_in_dir(maildir_vi)
    
    for f in mails:
        msg = parse_mail(f)
        print msg.get('From')

setup()
os.system('rm ' + join(maildir_vi, '*'))
map_login, map_fname, map_lname = create_local_directory()
fetchmail()
parse_maildir()
# parse_maildir_vi() # still buggy

os.system('vi ' + maildir_vi)

#!/usr/bin/env python

import apt

def open():
    return apt.Cache().open(apt.progress.text.OpProgress())

if __name__ == '__main__':
    open()

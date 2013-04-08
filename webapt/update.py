#!/usr/bin/env python

import apt

def update():
     
    return apt.Cache().update(apt.progress.text.AcquireProgress())

if __name__ == '__main__':
    update()

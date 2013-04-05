#!/usr/bin/env python

import apt

def commit():
    cache = apt.Cache()
    with cache.actiongroup():
        for pakage in cache.get_changes():
            return cache.commit(apt.progress.text.AcquireProgress(), apt.progress.text.OpProgress())

if __name__ == '__main__':
    commit()

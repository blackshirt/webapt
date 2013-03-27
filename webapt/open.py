#!/usr/bin/env python

import apt

apt.Cache().open(apt.progress.text.OpProgress())

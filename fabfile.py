from deploy import *

env.hosts = ['example.org']

configure(
    domain='example.org',
    root='/home/user/sites',
    repo='git://example.org/example-app',
    #toxenv='py27'
)

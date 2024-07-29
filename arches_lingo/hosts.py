import re
from django_hosts import patterns, host

host_patterns = patterns(
    "",
    host(re.sub(r"_", r"-", r"arches_lingo"), "arches_lingo.urls", name="arches_lingo"),
)

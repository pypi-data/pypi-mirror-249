[![PyPI version](https://badge.fury.io/py/cwhois.svg)](https://badge.fury.io/py/cwhois)

rfc1036's (Marco d'Itri) Intelligent WHOIS client fork extended in C for parsing and Python usage.

## install

`python -m pip install cwhois`

## python sample

```python
>>> import cwhois
>>> domain = cwhois.query('google.com')

>>> print(domain)
created: 1997-09-15T07:00:00+0000
updated: 2019-09-09T15:39:04+0000
expires: 2028-09-13T07:00:00+0000
status: clientUpdateProhibited (https://www.icann.org/epp#clientUpdateProhibited)
registrar: MarkMonitor, Inc.

>>> print(domain.registrar)
MarkMonitor, Inc.
```

## c sample

```c
#include "whois.h"

int main(int argc, char** argv)
{
    if(argc > 1) {
        // Query WHOIS and save output to C-string
        char* q = query_whois(argv[1]);
        puts(q);

        // Parse output into simple struct
        domain* d = parse_whois(q);

        if(d->created)          printf("Created: %s\n", d->created);
        if(d->expires)          printf("Expires: %s\n", d->expires);
        if(d->updated)          printf("Updated: %s\n", d->updated);
        if(d->status)           printf("Status: %s\n", d->status);
        if(d->registrar)        printf("Registrar: %s\n", d->registrar);

        // Free all resources
        domain_free(d);
        free(q);
    } else {
        printf("usage: %s <domain>\n", argv[0]);
    }

    return 0;
}
```

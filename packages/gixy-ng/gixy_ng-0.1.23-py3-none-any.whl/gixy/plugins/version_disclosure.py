import gixy
from gixy.plugins.plugin import Plugin


class version_disclosure(Plugin):
    """
    Syntax for the directive: resolver 127.0.0.1 [::1]:5353 valid=30s;
    """
    summary = 'Do not use external nameservers for "resolver"'
    severity = gixy.severity.HIGH
    description = 'Using external nameservers allows someone to send spoofed DNS replies to poison the resolver ' \
                  'cache, causing NGINX to proxy HTTP requests to an arbitrary upstream server.'
    help_url = 'https://blog.zorinaq.com/nginx-resolver-vulns/'
    directives = ['server_tokens']

    def audit(self, directive):
        if directive.args[0] in ['on', 'build']:
            self.add_issue(
                severity=gixy.severity.HIGH,
                directive=[directive, directive.parent],
                reason="User server_tokens off to hide nginx version"
            )

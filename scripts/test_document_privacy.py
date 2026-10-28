"""Offline negative/positive fixtures for privacy boundaries; no real host names."""
import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

import check_document_privacy as gate


def ipv4(*octets):
    return '.'.join(map(str, octets))


def hostname(label='unpublished'):
    return label + '.' + 'local'


class DetectorTests(unittest.TestCase):
    def values(self, text):
        return [f.value for f in gate.candidates(text)]

    def test_ipv4_exclusions_are_not_all_private_networks(self):
        for text in [ipv4(127, 0, 0, 1), ipv4(127, 0, 0, 2), ipv4(127, 200, 4, 3), ipv4(0, 0, 0, 0), 'localhost']:
            self.assertEqual(self.values(text), [])
        for text in [ipv4(10, 20, 30, 40), ipv4(192, 168, 1, 2), ipv4(192, 0, 2, 10)]:
            self.assertEqual(self.values(text), [text])
            self.assertEqual(self.values(text + '.'), [text])

    def test_invalid_ip_shapes_are_not_addresses(self):
        self.assertEqual(self.values(ipv4(999, 1, 2, 3)), [])
        self.assertEqual(self.values('version 1.2.3'), [])

    def test_ipv6_loopback_and_embedded_ipv4(self):
        for text in [':' * 2 + '1', ':'.join(['0000'] * 7 + ['0001']), ':' * 2 + 'ffff:' + ipv4(127, 2, 3, 4)]:
            self.assertEqual(self.values(text), [])
        text = ':' * 2 + 'ffff:' + ipv4(192, 0, 2, 10)
        self.assertEqual(self.values(text), [text])
        address = '2001:db8' + ':' * 2 + '123'
        self.assertEqual(self.values('https://[' + address + ']:443/'), [address])
        self.assertEqual(self.values('[' + ':' * 2 + ']'), [':' * 2])

    def test_bare_volume_prefix_and_concrete_paths(self):
        prefix = '/' + 'Volumes'
        self.assertEqual(self.values(prefix + ' ' + prefix + '/'), [])
        self.assertEqual(self.values(prefix + '/Disk/repo'), [prefix + '/Disk/repo'])
        self.assertTrue(self.values('/' + 'Users/person/repo'))
        self.assertTrue(self.values('/private/' + 'tmp/work'))

    def test_hosts_urls_sentence_punctuation_and_fqdn(self):
        h = hostname()
        for text in [h, h + '.', 'https://' + h + '/a', '`' + h + '`', h.upper()]:
            self.assertEqual(len(self.values(text)), 1)
        self.assertEqual(self.values('https://orbiplex.localhost/'), [])

    def test_pseudonyms_are_full_tokens(self):
        self.assertEqual(self.values('host-A.local host-AA.local IPADDR-A IPADDR-ZZ'), [])
        self.assertTrue(self.values('host-A.local' + '.example.org'))
        self.assertTrue(self.values('host-A.local' + '-other'))
        self.assertTrue(self.values(hostname('host-a')))
        self.assertTrue(self.values(hostname('prefix-host-A')))

    def test_identifiers_and_regex_are_not_hosts_or_addresses(self):
        name = hostname('contract')
        self.assertEqual(self.values('urn:orbiplex:schema:' + name + ':v1'), [])
        self.assertEqual(self.values(name + '.v1.schema.json'), [])
        self.assertEqual(self.values('(?:' + ':name)'), [])
        self.assertTrue(self.values(name))
        self.assertTrue(self.values('_service._tcp.' + 'local'))

    def test_exception_requires_path_value_and_context(self):
        token = hostname('fixture')
        context = '"value": "' + token + '"'
        rule = dict(path='fixture.json', value=token, context=context, reason='Synthetic example')
        self.assertEqual(gate.inspect(context, 'fixture.json', [rule]), [])
        self.assertTrue(gate.inspect(context, 'other.json', [rule]))
        self.assertTrue(gate.inspect('Host: ' + token, 'fixture.json', [rule]))
        self.assertTrue(gate.inspect(context + '\nHost: ' + token, 'fixture.json', [rule]))

    def test_explicit_example_tokens_are_exact(self):
        for token in [hostname('orbiplex'), hostname('ORBIPLEX').upper(), ipv4(1, 3, 2, 1)]:
            for text in [token, token + '.', 'https://' + token + '/a', 'user@' + token]:
                self.assertEqual(self.values(text), [])
        for token in [hostname('other.orbiplex'), hostname('other-orbiplex'),
                      ipv4(1, 3, 2, 10), ipv4(11, 3, 2, 1),
                      ':' * 2 + 'ffff:' + ipv4(1, 3, 2, 1)]:
            self.assertTrue(self.values(token))

    def test_other_version_numbers_require_context(self):
        token = ipv4(1, 3, 2, 2)
        rule = dict(path='versions.md', value=token, context='version ' + token, reason='Version')
        self.assertEqual(gate.inspect('version ' + token, 'versions.md', [rule]), [])
        self.assertTrue(gate.inspect('connect ' + token, 'versions.md', [rule]))

    def test_example_exceptions_apply_to_rendered_content(self):
        with tempfile.TemporaryDirectory() as directory:
            site = Path(directory)
            text = hostname('orbiplex') + ' ' + ipv4(1, 3, 2, 1)
            (site / 'index.html').write_text('<a href="https://' + hostname('orbiplex') + '/">' + text + '</a>')
            (site / 'search_index.json').write_text(json.dumps({'docs': [
                {'title': 'Examples', 'text': text, 'location': 'index.html'}]}))
            (site / 'example.txt').write_text(text)
            self.assertEqual(gate.check_site(site, []), 0)

    def test_html_spans_and_attributes(self):
        parser = gate.VisibleHTML()
        parser.feed('<code>unpublished<span>.</span>local</code><a href="http://' + hostname('other') + '/">x</a>')
        self.assertIn(hostname(), self.values(''.join(parser.parts)))
        self.assertIn(hostname('other'), self.values('\n'.join(parser.attributes)))

    def test_rendered_exception_remains_source_bound(self):
        token = hostname('fixture')
        rule = dict(path='doc/demo.md', value=token, context='example ' + token, reason='Example')
        self.assertEqual(gate.rendered_exceptions(token, 'doc/demo.md', [rule]), [])
        self.assertTrue(gate.rendered_exceptions(token, 'doc/other.md', [rule]))
        self.assertEqual(gate.source_path('pl/doc/demo/#section'), 'doc/demo.md')
        self.assertEqual(gate.source_path('doc/demo/index.html'), 'doc/demo.md')
        localized = dict(rule, path='doc/demo.pl.md')
        self.assertEqual(gate.rendered_exceptions(token, 'doc/demo.md', [localized]), [])


class RepositoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / '.gitignore').write_text('/local/\n/output/\n')
        (self.root / 'local').mkdir()
        (self.root / 'local/host-pseudonyms.json').write_text(hostname())

    def check(self):
        with contextlib.redirect_stdout(io.StringIO()):
            return gate.check_sources(self.root, [])

    def test_untracked_source_checked_ignored_map_not_read(self):
        self.assertEqual(self.check(), 0)
        (self.root / 'new.md').write_text(hostname())
        self.assertEqual(self.check(), 1)

    def test_forced_tracked_map_refused(self):
        subprocess.run(['git', '-C', str(self.root), 'add', '-f', gate.PRIVATE_MAP], check=True)
        self.assertEqual(self.check(), 1)

    def test_invalid_text_and_symlink_fail(self):
        (self.root / 'bad.md').write_bytes(b'\xff')
        with self.assertRaises(UnicodeDecodeError): self.check()
        (self.root / 'bad.md').unlink()
        (self.root / 'link.md').symlink_to(self.root / gate.PRIVATE_MAP)
        self.assertEqual(self.check(), 1)
        (self.root / gate.PRIVATE_MAP).unlink()
        self.assertEqual(self.check(), 1)  # A dangling symlink is still refused.

    def test_nul_cannot_hide_a_leak_in_markdown(self):
        (self.root / 'nul.md').write_bytes(b'\x00' + hostname().encode())
        with self.assertRaisesRegex(ValueError, 'NUL'): self.check()

    def test_exception_registry_rejects_broad_or_incomplete_entries(self):
        path = self.root / gate.EXCEPTIONS
        path.parent.mkdir()
        for entry in [
            {'path':'*.md', 'value':'x', 'context':'x', 'reason':'too broad'},
            {'path':'doc.md', 'value':'x', 'context':'y', 'reason':'missing token'},
            {'path':'doc.md', 'value':'x', 'context':'x'},
        ]:
            path.write_text(json.dumps({'schema':'document-privacy-exceptions.v1','exceptions':[entry]}))
            with self.assertRaises(ValueError): gate.load_exceptions(self.root)

    def test_site_pages_search_and_private_map(self):
        site = self.root / 'output'
        (site / 'search').mkdir(parents=True)
        (site / 'doc').mkdir()
        (site / 'doc/index.html').write_text('<p>host-A.local</p>')
        (site / 'search/search_index.json').write_text(json.dumps({'docs':[
            {'location':'doc/demo/', 'title':'Title', 'text':hostname()}]}))
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(gate.check_site(site, []), 1)
            (site / 'search/search_index.json').unlink()
            (site / 'host-pseudonyms.json').write_text('{}')
            self.assertEqual(gate.check_site(site, []), 1)

    def test_map_normalized_alias_conflict_and_private_permissions(self):
        path = self.root / gate.PRIVATE_MAP
        data = {'schema':'documentation-pseudonyms.local.v1', 'hosts':{
            'host-A.local':{'aliases':[hostname()]}}, 'addresses':{}}
        path.write_text(json.dumps(data)); path.chmod(0o600)
        gate.check_private_map(self.root)
        data['hosts']['host-B.local'] = {'aliases':[hostname().upper() + '.']}
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'duplicate'): gate.check_private_map(self.root)
        path.chmod(0o644)
        with self.assertRaisesRegex(ValueError, '0600'): gate.check_private_map(self.root)

    def test_map_ip_normalization_and_safe_errors(self):
        path = self.root / gate.PRIVATE_MAP
        data = {'schema':'documentation-pseudonyms.local.v1', 'hosts':{}, 'addresses':{
            'IPADDR-A':{'address':'2001:db8' + ':' * 2 + '1'},
            'IPADDR-B':{'address':':'.join(['2001','0db8'] + ['0'] * 5 + ['1'])}}}
        path.write_text(json.dumps(data)); path.chmod(0o600)
        with self.assertRaisesRegex(ValueError, 'duplicate'): gate.check_private_map(self.root)
        data['addresses'] = {'IPADDR-A':{'address':'private invalid value'}}
        path.write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, '^invalid mapped IP address$'): gate.check_private_map(self.root)


if __name__ == '__main__':
    unittest.main()

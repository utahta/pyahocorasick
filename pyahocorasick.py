# vim:fileencoding=utf8
#---------------------------------------------------------------------------
# Copyright 2011 utahta
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#---------------------------------------------------------------------------

class AhoCorasick(object):
    class Node(object):
        def __init__(self):
            self.terms = []
            self.next = {}
            self.failure_link = None
        def __repr__(self):
            return str(self.next)
    
    def __init__(self, terms=[]):
        self.create(terms)
    
    def create(self, terms=[]):
        self.root = AhoCorasick.Node()
        for term in terms:
            self._add(term)
        self._make_failure_links()
    
    def _add(self, term):
        node = self.root
        for char in term:
            if not char in node.next:
                node.next[char] = AhoCorasick.Node()
            node = node.next[char]
        node.terms.append(term)
        
    def _make_failure_links(self):
        for node in self.root.next.values():
            node.failure_link = self.root
        def _make(_node):
            for (char, node) in _node.next.items():
                failure_link = _node.failure_link
                if char in failure_link.next:
                    node.failure_link = failure_link.next[char]
                else:
                    if char in self.root.next:
                        node.failure_link = self.root.next[char]
                    else:
                        node.failure_link = self.root
                if node.failure_link.terms:
                    node.terms.extend(node.failure_link.terms)
                _make(node)
        for node in self.root.next.values():
            _make(node)
    
    def match(self, query):
        results = []
        node = self.root
        for i in xrange(len(query)):
            char = query[i]
            next = node.next.get(char)
            if next:
                node = next
            else:
                if node != self.root:
                    while True:
                        node = node.failure_link
                        if char in node.next:
                            break
                        if node == self.root:
                            break
                    node = node.next.get(char)
                    if not node:
                        node = self.root
            if node.terms:
                for term in node.terms:
                    term_length = len(term)
                    results.append((i+1-term_length, term_length))
        return results
    
    def __repr__(self):
        output = []
        def _debug(output, char, node, depth=0):
            output.append('%s[%s]%s' % (' '*depth, char, node.terms))
            for (key, n) in node.next.items():
                _debug(output, key, n, depth+1)
        _debug(output, '', self.root)
        return '\n'.join(output)

if __name__ == '__main__':
    ac = AhoCorasick(['ab', 'bc', 'bab', 'd', 'abcde'])
    print ac
    print ac.match('xbabcdex')
    print ac.match('abc')
    
    ac = AhoCorasick(['he', 'hers', 'his', 'she'])
    print ac
    print ac.match('a his hoge hershe xx.')
    
    ac = AhoCorasick([u'こんにちは', u'ありがとう', u'こんばんは', u'さようなら', u'まほうのことばで', u'たのしいなかまが', u'ポポポポ〜ン'])
    print unicode(ac)
    print ac.match(u'ありがとうございますこんにちはポポポポ〜ン')

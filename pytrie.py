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

class Trie(object):
    class Node(object):
        def __init__(self):
            self.term = None
            self.next = {}
    
    def __init__(self, terms=[]):
        self.root = Trie.Node()
        for term in terms:
            self.add(term)
    
    def add(self, term):
        node = self.root
        for char in term:
            if not char in node.next:
                node.next[char] = Trie.Node()
            node = node.next[char]
        node.term = term
    
    def match(self, query):
        results = []
        for i in xrange(len(query)):
            node = self.root
            for j in xrange(i, len(query)):
                node = node.next.get(query[j])
                if not node:
                    break
                if node.term:
                    results.append((i, len(node.term)))
        return results
    
    def __repr__(self):
        output = []
        def _debug(output, char, node, depth=0):
            output.append('%s[%s][%s]' % (' '*depth, char, node.term))
            for (key, n) in node.next.items():
                _debug(output, key, n, depth+1)
        _debug(output, '', self.root)
        return '\n'.join(output)

if __name__ == '__main__':
    t = Trie(['ab', 'bc', 'bab', 'd', 'abcde'])
    print t
    print t.match('xbabcdex')
    print t.match('abc')

    t = Trie(['he', 'hers', 'his', 'she'])
    print t
    print t.match('a his hoge hershe xx.')

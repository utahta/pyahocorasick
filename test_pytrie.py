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
from pytrie import Trie

def test_trie():
    t = Trie(['he','hers','his','she'])
    results = t.match('a his hoge hershe xx.')
    assert len(results) == 5
    rows = [(2,3), (11,2), (11,4), (14,3), (15,2)]
    for i in xrange(5):
        print results[i], rows[i]
        assert results[i] == rows[i]

if __name__ == '__main__':
    test_trie()
    
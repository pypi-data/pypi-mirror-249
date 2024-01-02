from typing import List, Tuple, Union

AstNode = Union[str, Tuple[str, List['AstNode']]]

def parse(src: str) -> AstNode:
    """
    parse the source code of WhileDB language and return AstNode
    ```
    AstNode = Tuple[str, List[AstNode]]
    ```
    """

def exec(src: str) -> None:
    """
    execuate the WhileDB code

    example:
    ```
    import whiledb_rs

    whiledb_rs.exec(
    \"\"\"
    class DisjointSet {
        fn __init__(self, n) {
            self.data = [];
            idx = 0;
            while idx < n {
                self.data.append(-1);
                idx = idx + 1;
            }
            return self;
        }
        fn __string__(self) {
            return "DisjointSet(" + string(self.data) + ")";
        }
        fn find(self, idx) {
            if self.data[idx] < 0 {
                return idx;
            }
            self.data[idx] = self.find(self.data[idx]);
            return self.data[idx];
        }
        fn union(self, a, b) {
            fa = self.find(a);
            fb = self.find(b);
            if fa == fb {
                return None;
            }
            if self.data[fa] < self.data[fb] {
                self.data[fa] = self.data[fa] + self.data[fb];
                self.data[fb] = fa;
            }
            else {
                self.data[fb] = self.data[fb] + self.data[fa];
                self.data[fa] = fb;
            }
        }
    }

    s = DisjointSet(10);
    s.union(1, 2);
    s.union(1, 5);
    print(s.find(1) == s.find(5));
    // true
    \"\"\"
    )
    ```
    """
use whiledb::ast::*;
use pyo3::prelude::*;

pub struct AST {
    name: String,
    childs: Option<Vec<AST>>
}

impl IntoPy<Py<PyAny>> for AST {
    fn into_py(self, py: Python<'_>) -> Py<PyAny> {
        match self.childs {
            Some(childs) => (self.name.into_py(py), childs.into_py(py)).into_py(py),
            None => self.name.into_py(py),
        }
    }
}

impl AST {
    fn new(name: &str, childs: Vec<AST>) -> AST {
        AST { name: name.to_string(), childs: Some(childs) }
    }
    fn leaf(name: &str) -> AST {
        AST { name: name.to_string(), childs: None }
    }
}

pub fn cmd2ast(root: &Cmd) -> AST {
    match root {
        Cmd::Asgn(e1, e2) => AST::new("asgn", vec![expr2ast(e1), expr2ast(e2)]),
        Cmd::Seq(cs) => AST::new("seq", cs.iter().map(|e| cmd2ast(e)).collect()),
        Cmd::If(e, c1, c2) => AST::new("if", vec![expr2ast(e), cmd2ast(c1), cmd2ast(c2)]),
        Cmd::While(e, c) => AST::new("while", vec![expr2ast(e), cmd2ast(c)]),
        Cmd::Expr(e) => AST::new("expr", vec![expr2ast(e)]),
        Cmd::Continue => AST::new("continue", vec![]),
        Cmd::Break => AST::new("break", vec![]),
        Cmd::Func(s, e, c) => AST::new("func", vec![AST::leaf(s), expr2ast(e), cmd2ast(c)]),
        Cmd::Class(s, c) => AST::new("class", vec![AST::leaf(s), cmd2ast(c)]),
        Cmd::Return(e) => AST::new("return", vec![expr2ast(e)]),
        Cmd::Nop => AST::new("nop", vec![]),
    }
}

pub fn expr2ast(root: &Expr) -> AST {
    match root {
        Expr::ConstInt(s) => AST::new("int", vec![AST::leaf(s)]),
        Expr::ConstFloat(s) => AST::new("float", vec![AST::leaf(s)]),
        Expr::ConstString(s) => AST::new("string", vec![AST::leaf(s)]),
        Expr::Tuple(es) => AST::new("tuple", es.iter().map(|e| expr2ast(e)).collect()),
        Expr::Var(s) => AST::new("ident", vec![AST::leaf(s)]),
        Expr::BinOp(op, e1, e2) => AST::new(binop2str(op), vec![expr2ast(e1), expr2ast(e2)]),
        Expr::UnOp(op, e) => AST::new(unop2str(op), vec![expr2ast(e)]),
        Expr::Call(e1, e2) => AST::new("call", vec![expr2ast(e1), expr2ast(e2)]),
        Expr::GetItem(e1, e2) => AST::new("getitem", vec![expr2ast(e1), expr2ast(e2)]),
        Expr::GetAttr(e, s) => AST::new("getattr", vec![expr2ast(e), AST::leaf(s)]),
    }
}

pub fn binop2str(op: &BinOp) -> &'static str {
    match op {
        BinOp::Plus => "+",
        BinOp::Minus => "-",
        BinOp::Mul => "*",
        BinOp::Div => "/",
        BinOp::Mod => "%",
        BinOp::Lt => "<",
        BinOp::Gt => ">",
        BinOp::Le => "<=",
        BinOp::Ge => ">=",
        BinOp::Eq => "==",
        BinOp::Ne => "!=",
        BinOp::And => "and",
        BinOp::Or => "or",
    }
}

pub fn unop2str(op: &UnOp) -> &'static str {
    match op {
        UnOp::Negate => "negate",
        UnOp::Not => "not",
        UnOp::Deref => "deref",
    }
}

use core::ops::ControlFlow;
use sqlparser::ast::*;
use sqlparser::dialect::AnsiDialect;
use sqlparser::parser::Parser;

use pyo3::prelude::*;

const DATE_COLUMN_NAMES: [&'static str; 3] = ["date", "p_date", "pdate"];
const ARRAY_AGG_FUNCS: [&'static str; 5] = [
    "array_agg",
    "set_agg",
    "collect_set",
    "collect_list",
    "array_set",
];
const ARRAY_SORT: &'static str = "array_sort";

struct Formalizer {
    broken: bool,
}

impl Formalizer {
    pub fn is_broken(&self) -> bool {
        self.broken
    }
}

fn construct_order_by(count: usize) -> Vec<OrderByExpr> {
    let mut v = Vec::new();
    for i in 1..count + 1 {
        let number = Value::Number(i.to_string(), false);
        let expr = Expr::Value(number);
        v.push(OrderByExpr {
            expr,
            asc: None,
            nulls_first: None,
        });
    }
    v
}

fn no_wild(projection: &Vec<SelectItem>) -> bool {
    for project in projection {
        match project {
            SelectItem::QualifiedWildcard(_, _) => {
                return false;
            }
            SelectItem::Wildcard(_) => {
                return false;
            }
            _ => {}
        }
    }
    true
}

fn need_to_add_limit(limit: &Option<Expr>) -> bool {
    match limit {
        Some(limit) => match limit {
            Expr::Value(value) => match value {
                Value::Number(val, _) => {
                    let parsed: Result<u32, _> = val.parse();
                    match &parsed {
                        Ok(val) => {
                            if val <= &20000 {
                                false
                            } else {
                                true
                            }
                        }
                        Err(_) => true,
                    }
                }
                _ => true,
            },
            _ => true,
        },
        _ => true,
    }
}

fn formalize_function(func: &mut Function) {
    if func.name.0.len() != 1 || func.args.len() != 1 {
        return;
    }
    let mut name_matched = false;
    ARRAY_AGG_FUNCS.into_iter().for_each(|array_agg_func| {
        if func.name.0[0].value == array_agg_func {
            name_matched = true;
        }
    });
    if !name_matched {
        return;
    }

    func.args[0] = FunctionArg::Unnamed(FunctionArgExpr::Expr(Expr::Function(func.clone())));
    func.name.0[0].value.clear();
    func.name.0[0].value.push_str(ARRAY_SORT);
}

fn formalize_binop(left: &Box<Expr>, op: &mut BinaryOperator, right: &Box<Expr>) {
    match op {
        BinaryOperator::Gt => (),
        BinaryOperator::GtEq => (),
        BinaryOperator::Lt => (),
        BinaryOperator::LtEq => (),
        _ => return,
    }
    match left.as_ref() {
        Expr::Identifier(ident) => {
            let mut name_matched = false;
            DATE_COLUMN_NAMES.into_iter().for_each(|s| {
                if s == ident.value {
                    name_matched = true;
                }
            });
            if !name_matched {
                return;
            }
            match op {
                BinaryOperator::Gt => *op = BinaryOperator::Eq,
                BinaryOperator::GtEq => *op = BinaryOperator::Eq,
                _ => (),
            }
            return;
        }
        _ => (),
    }
    match right.as_ref() {
        Expr::Identifier(ident) => {
            let mut name_matched = false;
            DATE_COLUMN_NAMES.into_iter().for_each(|s| {
                if s == ident.value {
                    name_matched = true;
                }
            });
            if !name_matched {
                return;
            }
            match op {
                BinaryOperator::Lt => *op = BinaryOperator::Eq,
                BinaryOperator::LtEq => *op = BinaryOperator::Eq,
                _ => (),
            }
        }
        _ => (),
    }
}

impl VisitorMut for Formalizer {
    type Break = ();

    fn pre_visit_query(&mut self, query: &mut Query) -> ControlFlow<Self::Break> {
        let body = query.body.as_ref();
        match body {
            SetExpr::Select(select) => {
                if !no_wild(&select.projection) {
                    self.broken = true;
                    return ControlFlow::Break(());
                }
                query.order_by = construct_order_by(select.projection.len());
                if need_to_add_limit(&query.limit) {
                    query.limit = Some(Expr::Value(Value::Number(String::from("20000"), false)));
                }
                query.limit_by = vec![];
                ControlFlow::Continue(())
            }
            SetExpr::SetOperation {
                left,
                op: _,
                set_quantifier: _,
                right: _,
            } => match left.as_ref() {
                SetExpr::Select(select) => {
                    if !no_wild(&select.projection) {
                        self.broken = true;
                        return ControlFlow::Break(());
                    }
                    query.order_by = construct_order_by(select.projection.len());
                    if need_to_add_limit(&query.limit) {
                        query.limit =
                            Some(Expr::Value(Value::Number(String::from("20000"), false)));
                    }
                    query.limit_by = vec![];
                    ControlFlow::Continue(())
                }
                _ => ControlFlow::Continue(()),
            },
            _ => ControlFlow::Continue(()),
        }
    }

    fn post_visit_expr(&mut self, _expr: &mut Expr) -> ControlFlow<Self::Break> {
        match _expr {
            Expr::BinaryOp { left, op, right } => formalize_binop(left, op, right),
            Expr::Function(function) => formalize_function(function),
            _ => (),
        };
        ControlFlow::Continue(())
    }
}

fn make_deterministic(sql: &str) -> String {
    let result = Parser::parse_sql(&AnsiDialect {}, sql);
    match result {
        Ok(mut statements) => {
            if statements.len() == 0 {
                "".to_owned()
            } else {
                let mut first_statement = &mut statements[0];
                make_deterministic_impl(&mut first_statement)
            }
        }
        Err(_) => "".to_owned(),
    }
}

fn make_deterministic_impl(statement: &mut Statement) -> String {
    let mut visitor = Formalizer { broken: false };
    statement.visit(&mut visitor);
    if visitor.is_broken() {
        String::from("")
    } else {
        statement.to_string()
    }
}

#[pyfunction]
#[pyo3(text_signature = "(sql)")]
#[pyo3(name = "make_deterministic")]
fn python_wrapper(sql: &str) -> PyResult<String> {
    Ok(make_deterministic(sql))
}

#[pymodule]
fn deterministic_sql(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(python_wrapper, m)?)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use crate::make_deterministic;

    #[test]
    fn simple() {
        let sql = "select a, b, c from t";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a, b, c FROM t ORDER BY 1, 2, 3 LIMIT 20000"
        );
    }

    #[test]
    fn nested() {
        let sql = "select a, b, c from (select a, b, c from t)";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a, b, c FROM (SELECT a, b, c FROM t ORDER BY 1, 2, 3 LIMIT 20000) ORDER BY 1, 2, 3 LIMIT 20000"
        );
    }

    #[test]
    fn limit() {
        let sql = "select a, b, c from t limit 10";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a, b, c FROM t ORDER BY 1, 2, 3 LIMIT 10"
        );
    }

    #[test]
    fn wild() {
        let sql = "select * from t limit 10";
        assert_eq!(make_deterministic(sql), "");
    }

    #[test]
    fn union() {
        let sql = "select a from t1 union all select b from t2";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a FROM t1 UNION ALL SELECT b FROM t2 ORDER BY 1 LIMIT 20000"
        );
    }

    #[test]
    fn join() {
        let sql = "
            SELECT orders.order_id, orders.order_amount, customers.customer_name
            FROM orders
            INNER JOIN (
                SELECT customer_id, customer_name
                FROM customers
            ) AS customers ON orders.customer_id = customers.customer_id;";
        assert_eq!(
            make_deterministic(sql),
            "SELECT orders.order_id, orders.order_amount, customers.customer_name FROM orders JOIN (SELECT customer_id, customer_name FROM customers ORDER BY 1, 2 LIMIT 20000) AS customers ON orders.customer_id = customers.customer_id ORDER BY 1, 2, 3 LIMIT 20000"
        );
    }

    #[test]
    fn formalize_partition() {
        let sql = "SELECT a FROM t WHERE date >= '20240101'";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a FROM t WHERE date = '20240101' ORDER BY 1 LIMIT 20000"
        );
        let sql = "SELECT a FROM t WHERE date > '20240101'";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a FROM t WHERE date = '20240101' ORDER BY 1 LIMIT 20000"
        );
        let sql = "SELECT a FROM t WHERE '20240101' <= date";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a FROM t WHERE '20240101' = date ORDER BY 1 LIMIT 20000"
        );
        let sql = "SELECT a FROM t WHERE '20240101' < date";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a FROM t WHERE '20240101' = date ORDER BY 1 LIMIT 20000"
        );
        let sql = "SELECT a FROM t WHERE name = 'Tom' AND date >= '20240101'";
        assert_eq!(
            make_deterministic(sql),
            "SELECT a FROM t WHERE name = 'Tom' AND date = '20240101' ORDER BY 1 LIMIT 20000"
        );
    }

    #[test]
    fn array_sort() {
        let sql = "SELECT set_agg(a) FROM t";
        assert_eq!(
            make_deterministic(sql),
            "SELECT array_sort(set_agg(a)) FROM t ORDER BY 1 LIMIT 20000"
        );
    }
}

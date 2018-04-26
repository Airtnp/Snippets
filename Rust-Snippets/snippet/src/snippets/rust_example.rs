use std::fmt;

struct List(Vec<i32>);

impl fmt::Display for List {
    fn fmt(&self, f: &mut::Formatter) -> fmt::Result {
        let List(ref vec) = *self;
        try!(write!(f, "["));
        for (count, v) in vec.iter().enumerate() {
            if count != 0 {
                try!(write!(f, ", "));
            }
            try!(write!(f, "{}: {}", count, v));
        }
        try!(write!(f, "]"));
    }
}

fn test0() {
    let v = List(vec![1, 2, 3]);
    println!("{}", v);
}

use std::fmt::{self, Formatter, Display};
struct City {
    name: &'static str,
    lat: f32,
    lon: f32,
}

impl Display for City {
    fn fmt(&self, f: &mut Formatter) -> fmt::Result {
        let lat_c = if self.lat >= 0.0 { 'N' } else { 'S' };
        let lon_c = if self.lon >= 0.0 { 'E' } else { 'W' };
        // `write!` 和 `format!` 类似，但它会将格式化后的字符串写入到一个缓冲区
        // 中（第一个参数f）
        write!(f, "{}: {:.3}°{} {:.3}°{}",
        self.name, self.lat.abs(), lat_c, self.lon.abs(), lon_c)
    }
}

#[derive(Debug)]
struct Color {
    red: u8,
    green: u8,
    blue: u8,
}

fn test1() {
    for city in [
        City { name: "Dublin", lat: 53.347778, lon: -6.259722 },
        City { name: "Oslo", lat: 59.95, lon: 10.75 },
        City { name: "Vancouver", lat: 49.25, lon: -123.1 },
    ].iter() {
        println!("{}", *city);
    }
    for color in [
        Color { red: 128, green: 255, blue: 90 },
        Color { red: 0, green: 3, blue: 254 },
        Color { red: 0, green: 0, blue: 0 },
    ].iter() {
        println!("{:?}", *color)
    }
}

fn analyze_slice(slice: &[i32]) {
    println!("first element of the slice: {}", slice[0]);
    println!("the slice has {} elements", slice.len());
}

fn test2() {
    let logical : bool = true;
    let a_float: f64 = 1.0;
    let an_integer = 5i32; 

    let default_float = 3.0; // `f64`
    let default_integer = 7; // `i32`
    let mut mutable = 12; // mutable `i32`。
    // error
    // mutable = true;

    // tuple
    let long_tuple = (1u8, 2u16, 3u32, 4u64,
                        -1i8, -2i16, -3i32, -4i64,
                        0.1f32, 0.2f64,
                        'a', true);
    // slice
    let xs: [i32; 5] = [1, 2, 3, 4, 5];
    let ys: [i32; 500] = [0; 500];
    analyze_slice(&xs);
    analyze_slice(&ys[1 .. 4]);
    // panic
    // println!("{}", xs[5]);
}

struct Nil;

struct Pair(i32, i32);

struct Point {
    x: f32;
    y: f32;
}

#[allow(dead_code)]
struct Rectangle {
    p1: Point;
    p2: Point;
}

fn test3() {
    let point: Point = Point { x: 0.3, y: 0.4 };
    println!("point coordinates: ({}, {})", point.x, point.y);

    let Point { x: my_x, y: my_y } = point;
    let _rectangle = Rectangle {
        p1: Point { x: my_y, y: my_x },
        p2: point,
    };

    let _nil = Nil;

    let pair = Pair(1, 0.1);

    println!("pair contains {:?} and {:?}", pair.0, pair.1);

    let Pair(integer, decimal) = pair;
    println!("pair contains {:?} and {:?}", integer, decimal)
}

#![allow(dead_code)]
enum Person {
    Engineer,
    Scientist,
    Height(i32),
    Weight(i32),
    Info { name: String, height: i32 }
}

fn inspect(p: Person) {
    match p {
        Person::Engineer => println!("Is engineer!"),
        Person::Scientist => println!("Is scientist!"),
        Person::Height(i) => println!("Has a height of {}.", i),
        Person::Weight(i) => println!("Has a weight of {}.", i),
        Person::Info { name, height } => {
            println!("{} is {} tall!", name, height);
        },
    }
}

fn test4() {
    let person = Person::Height(18);
    let amira = Person::Weight(10);
    // slice => string
    let dave = Person::Info { name: "Dave".to_owned(), height: 72 };
    let rebecca = Person::Scientist;
    let rohan = Person::Engineer;
    inspect(person);
    inspect(amira);
    inspect(dave);
    inspect(rebecca);
    inspect(rohan);

    use Person::{Engineer, Info};
    use Person::*;   
}

use List::*;
enum List {
    Cons(u32, Box<List>),
    Nil,
}

impl List {
    fn new() -> List {
        Nil
    }

    fn prepend(self, elem: u32) -> List {
        Cons(elem, Box::new(self))
    }

    fn len(&self) -> u32 {
        match *self {
            Cons(_, ref tail) => 1 + tail.len(),
            Nil => 0
        }
    }

    fn stringify(&self) -> String {
        match *self {
            Cons(head, ref tail) => {
                format!("{}, {}", head, tail.stringify())
            },
            Nil => {
                format!("Nil")
            },
        }
    }
}

fn test5() {
    let mut list = List::new();
    list = list.prepend(1);
    list = list.prepend(2);
    list = list.prepend(3);
    println!("linked list has length: {}", list.len());
    println!("{}", list.stringify());
}

// may change in 'static
static LANGUAGE: &'static str = "Rust";
// just constexpr
const THRESHOLD: i32 = 10;

fn is_big(n: i32) -> bool {
    n > THRESHOLD
}

fn test6() {
    // underscore => no unused warning
    let _unused = 3u32;
    let mut mut_int = 1;
    mut_int += 1;
    let test = 'a';
    {
        let test = 'b'; // hiding
    }
    let test = 'c'; // override

    let a_binding;
    {
        a_binding = 4;
    }

    let decimal = 65.2f32;
    let integer: u8 = decimal as u8;
    // default integral => i32
    // default floating => f64

    // fun(&foo) borrow by immutable ref
    // fun(foo) borrow by value

    let elem = 5u8;
    let mut vec = Vec::new(); // defer type
    vec.push(elem); // now vec has Vec<u8> (type deduction across statements)

    type NanoSecond = u64; // name aliasing
    #[allow(non_camel_case_types)]
    type u64_t = u64;
    // IoResult<T> => Result<T, IoError>;

    let n = 5;
    if n < 0 {
        ;
    } else if {
        print!("{}", n);
    }

    let big_n = 
        if n < 10 && n > -10 {
            10 * n
        } else {
            n / 2
        };
    
    let mut cnt = 0;
    loop {
        cnt += 1;
        break;
    }

    'outer : loop {
        'inner : loop {
            break 'outer;
        }
        break cnt * 2; // return cnt * 2
    }

    while cnt < 100 {
        n += 1;
    }

    for i in 1..100 {
        println!("{}", n);
        match i {
            1 => ,
            2 | 3 | 4 => ,
            n@5..7 => , // n = 5 or 6 or 7
            _ => ,
        }
        let p = (2, 3);
        match p {
            (0, y) if y % 2 == 0 => ,
            (x, 0) if x % 2 == 0 => ,
            _ => ,
        }
    }

    let n_ref = &4;
    match n_ref {
        &val => println!("{}", val),
    }

    match *n_ref {
        val => println!("{}", val),
    }

    let ref m_ref = 4;
    let k = 4;
    let mut l = 4;
    match k {
        ref r => ,
    }
    match l {
        ref mut r => {
            *r += 10;
        }
    }

    struct Foo { x : (u32, u32), y : u32 }
    let foo = Foo { x : (1, 2), y : 3 };
    let Foo { x : (a, b), c } = foo;
    let Foo { y, .. } = foo;
    // now a = 1, b = 2, c = 3, y = 3

    let s = Some(7);
    let p = Option<i32> = None;
    if let Some(i) = s {
        ;
    } else {
        ;
    }
    let cond = true;
    if let Some(i) = p {
        ;
    } else if cond {
        ;
    } else {
        ;
    }

    let mut opt = Some(0);
    while let Some(i) = opt {
        if i > 9 {
            opt = None;
        } else {
            opt = Some(i + 1);
        }
    }
}

// Rust functions don't need forward declaration
// Rust has no overload resolution
// return type void == () (can be omitted)
fn is_divisible_by(lhs: u32, rhs: u32) -> bool {
    if rhs == 0 {
        return false;
    }
    lhs % rhs == 0
}

// method
// impl StructName {}

fn test7() {
    fn function (i: i32) -> i32 { i + 1 }

    let closure_annotated = |i: i32| -> i32 { i + 1 };
    let closure_inferred = |i| i + 1 ;
    let closure_inferred_2 = |&i| i + 1 ;
    let closure_inferred_2 = |&i| i + 1 ;
    let i = 1;

    println!("function: {}", function(i));
    println!("closure_annotated: {}", closure_annotated(i));
    println!("closure_inferred: {}", closure_inferred(i));

    let one = || 1;
    println!("closure returning one: {}", one());

    let color = "green";
    // println!` only requires `by reference` so it doesn't impose anything more restrictive.
    // capture by ref
    let print = || println!("`color`: {}", color);

    print();
    print();
    let mut count = 0;
    // A `mut` is required on `inc` because a `&mut` is stored inside. Thus, calling the closure mutates the closure which requires a `mut`.
    // capture by mut ref
    let mut inc = || {
        count += 1;
        println!("`count`: {}", count);
    };
    inc();
    inc();
    // cannot reborrow
    // let reborrow = &mut count;

    // noncopyable, capture by move
    let movable = Box::new(3);
    // `mem::drop` requires `T` so this must take by value. A copy type
    // would copy into the closure leaving the original untouched.
    // moved to closure
    let consume = || {
        println!("`movable`: {:?}", movable);
        mem::drop(movable);  // move movable out of the closure's environment
    };
    // consume the movable, so only can be called once
    consume();

    let x = vec![1, 2, 3];
    // capture all by value
    let equal_to_x = move |z| z == x;
    // println!("can't use x here: {:?}", x);

    let y = vec![1, 2, 3];
    assert!(equal_to_x(y));
}

// Fn: capture by &T (ref)
// FnMut: capture by &mut T (mut ref)
// FnOnce: capture by T (value)

// F must be polymorphic (no name, only trait)
fn apply<F>(f: F) where
    F: FnOnce() {
    f();
}

fn apply_to_3<F>(f: F) -> i32 where
    F: Fn(i32) -> i32 {
    f(3)
}

fn call_me<F: Fn()>(f: F) {
    f()
}

fn create_fn() -> Box<Fn()> {
    let text = "Fn".to_owned();
    Box::new(move || println!("This is a: {}", text))
}

fn create_fnmut() -> Box<FnMut()> {
    let text = "FnMut".to_owned();
    Box::new(move || println!("This is a: {}", text))
}

// @ref: https://stackoverflow.com/questions/25445761/returning-a-closure-from-a-function
// unboxed closure
fn make_adder(a: i32) -> impl Fn(i32) -> i32 {
    move |b| a + b
}

fn make_adder(a: int, b: int) -> |&:| -> int {
    |&:| a + b
}

fn test8() {
    use std::mem;
    let greeting = "hello";
    // non-copyable (String as Vec)
    let mut farewell = "goodbye".to_owned();
    // greeting by ref, farewell by value (move)
    let diary = || {
        // ref => need Fn
        println!("I said {}.", greeting);
        // force change
        // mut ref => need FnMut
        farewell.push_str("!!!");
        println!("Then I screamed {}.", farewell);
        println!("Now I can sleep. zzzzz");
        // force move
        // value => need FnOnce
        mem::drop(farewell);
    };
    apply(diary);
    let double = |x| 2 * x;
    println!("3 doubled: {}", apply_to_3(double));
}

// cannot use in stable
#![feature(core_intrinsics)]
fn print_type_of<T>(_: &T) {
    println!("{}", unsafe { std::intrinsics::type_name::<T>() });
}

fn test9() {
    // Iterator::any : <F>(&mut self, f : F) -> bool where F : FnMut(Self::Item) -> bool ()
    let vec1 = vec![1, 2, 3];
    let vec2 = vec![4, 5, 6];
    // &i32
    println!("2 in vec1: {}", vec1.iter() .any(|&x| x == 2));
    // i32
    println!("2 in vec2: {}", vec2.into_iter().any(| x| x == 2));
    let array1 = [1, 2, 3];
    let array2 = [4, 5, 6];
    // &i32
    println!("2 in array1: {}", array1.iter() .any(|&x| x == 2));
    // &i32
    println!("2 in array2: {}", array2.into_iter().any(|&x| x == 2));

    let mut acc = 0;
    for n in 0.. {
        let n_squared = n * n;
        if n_squared >= upper {
            break;
        } else if is_odd(n_squared) {
            acc += n_squared;
        }
    }
    println!("imperative style: {}", acc);
    // high order function in option, iterators
    // std::ops::RangeFrom<{Integer}>
    let sum_of_squared_odd_numbers: u32 =
        (0..).map(|n| n * n)
        .take_while(|&n| n < upper)
        .filter(|&n| is_odd(n))
        .fold(0, |sum, i| sum + i);
    println!("functional style: {}", sum_of_squared_odd_numbers);
}

mod namespace {
    fn private() {
        ;
    }

    pub fn public() {
        self::np2::public();
    }

    pub mod np2 {
        pub fn public() {
            ;
        }
        pub fn public2() { 
            self::public();
            public();

            super::private();
            {
                use super::np2::public as r;
                r();
            }
        }
    }
}

// mod prelude; => find prelude.rs or prelude/mod.rs

// Structure is default private
// add pub to make attribute public

// use deeply::nested::function as other_name;

// extern crate lib;

/*
attribute:
    #[attribute = "vlaue"]
    #[attribute(key = "value")]
    #[attribute(value)]

    dead_code: -Wno-unused_function
    crate: executable or lib (#[crate_type = "lib"])
    cfg: #[cfg(...)] or cfg!(...)
        #[cfg(not(target_os = "linux"))] == #ifndef __linux__
*/

struct SingleGen<T>(T); // because <T> is not ahead of T => generic

fn generic<T>(_s : SingleGen<T>) {}

impl <T> SingleGen<T> {
    fn value(&self) -> &T { &self.0 }
}

trait DoubleDrop<T> {
    fn double_drop(self, _: T);
}

impl<T, U> DoubleDrop<T> for U {
    fn double_drop(self, _: T) {}
}

use std::fmt::{Debug, Display};

fn generic_trait_req<U, T: DoubleDrop<U> + Display>(t : &T) {}

impl<T> PrintInOption for T where
    Option<T>: Debug + Display {
    fn print_in_option(self) {
        println!("{:?}", Some(self));
    }
}

// associated type
// @ref: https://github.com/rust-lang/rfcs/blob/master/text/0195-associated-items.md
// The kind * -> *
trait TypeToType<Input> {
    type Output;
}
type Apply<Name, Elt> where Name: TypeToType<Elt> = Name::Output;

struct Vec_;
struct DList_;

impl<T> TypeToType<T> for Vec_ {
    type Output = Vec<T>;
}

impl<T> TypeToType<T> for DList_ {
    type Output = DList<T>;
}

trait Mappable {
    type E; // contains E
    type HKT where Apply<HKT, E> = Self;

    fn map<F>(self, f: E -> F) -> Apply<HKT, F>;
}

trait Contains {
    // 在这里定义可以被方法利用的泛型类型。
    type A;
    type B;
    fn contains(&self, &Self::A, &Self::B) -> bool;
    fn first(&self) -> i32;
    fn last(&self) -> i32;
}
// type family
impl Contains for Container {
    type A = i32;
    type B = i32;
    fn contains(&self, number_1: &i32, number_2: &i32) -> bool {
        (&self.0 == number_1) && (&self.1 == number_2)
    }
    fn first(&self) -> i32 { self.0 }
    fn last(&self) -> i32 { self.1 }
}

use std::marker::PhantomData;

#[derive(PartialEq)]
struct PhantomTuple<A, B>(A,PhantomData<B>);

#[derive(PartialEq)]
struct PhantomStruct<A, B> { first: A, phantom: PhantomData<B> }

use std::ops::Add;

#[derive(Debug, Clone, Copy)]
enum Inch {}

#[derive(Debug, Clone, Copy)]
enum Mm {}

#[derive(Debug, Clone, Copy)]
struct Length<Unit>(f64, PhantomData<Unit>);
impl<Unit> Add for Length<Unit> {
    type Output = Length<Unit>;
    fn add(self, rhs: Length<Unit>) -> Length<Unit> {
        Length(self.0 + rhs.0, PhantomData)
    }
}

// RAII - stack & heap(Box)\\

#[allow(dead_code)]
#[derive(Clone, Copy)]
pub struct Book {
    author: &'static str,
    title: &'static str,
    year: u32,
}

fn new_edition(book: &mut Book) {
    book.year = 2014;
}

fn test10() {
    // non-copyable, pass by move
    let immut = Box::new(5u32);
    let mut mutbox = immut;
    *mutbox = 4;   

    let immut_b = Book {
        author: "A",
        title: "B",
        year: 1979,
    }
    let mut mut_b = immut_b;
    // can only borrow mutable object to mutable refs
    new_edition(&mut mut_b);

    {
        let immut_b = &mut_b;
        // freeze mut_b
        // mut_b.year = 20;
    }

    // only 1 mutable borrow same time
    // can be multiple immutable borrow same time

    let _copy_of_x = {
        let Point { x: ref ref_to_x, y: _ } = point;
        *ref_to_x
    };

    // also ref mut
}

// 'a, 'b must have lifetime longer than print_refs
fn print_refs<'a, 'b>(x: &'a i32, y: &'b i32) {
    println!("x is {} and y is {}", x, y);
}

// 'a default = 'static
fn failed_borrow<'a>() {
    let _x = 12;
    // _x does not live long enough then 'a
    // let y = &'a i32 = &_x;
}

fn pass_x<'a, 'b>(x: &'a i32, _: &'b i32) -> &'a i32 { x }

struct Owner(i32);
impl Owner {
    fn add_one<'a>(&'a mut self) { self.0 += 1; }
    fn print<'a>(&'a self) {
        println!("`print`: {}", self.0);
    }
}

#[derive(Debug)]
struct Borrowed<'a>(&'a i32);

#[derive(Debug)]
enum Either<'a> {
    Num(i32),
    Ref(&'a i32),
}

// T has Debug trait, all ref in T must live longer than print_ref
fn print_ref<'a, T>(t: &'a T) where
    T: Debug + 'a {
    println!("`print_ref`: t is {:?}", t);
}

// 'a longer than 'b, cast to 'b
fn choose_first<'a: 'b, 'b>(first: &'a i32, _: &'b i32) -> &'b i32 {
    first
}

// elision for lifetime

struct Sheep { naked: bool, name: &'static str }
trait Animal {
    // Self: implementer type
    fn new(name: &'static str) -> Self;
    fn name(&self) -> &'static str;
    fn noise(&self) -> &'static str;
    // default defintion
    fn talk(&self) {
        println!("{} says {}", self.name(), self.noise());
    }
}

impl Sheep {
    fn is_naked(&self) -> bool {
        self.naked
    }
    fn shear(&mut self) {
        if self.is_naked() {
            println!("{} is already naked...", self.name());
        } else {
            println!("{} gets a haircut!", self.name);
            self.naked = true;
        }
    }
}

impl Animal for Sheep {
    fn new(name: &'static str) -> Sheep {
        Sheep { name: name, naked: false }
    }
    fn name(&self) -> &'static str {
        self.name
    }
    fn noise(&self) -> &'static str {
        if self.is_naked() {
            "baaaaah?"
        } else {
            "baaaaah!"
        }
    }
    // ovrload
    fn talk(&self) {
        println!("{} pauses briefly... {}", self.name, self.noise());
    }
}

/*
#derive
    Eq, PartialEq, Ord, PartialOrd
    Clone (copy from &T -> T)
    Copy (copy semantics instead of move)
    Hash (&T)
    Default
    Zero
    Debug {:?}
*/

// operations overload
use std::ops;

impl ops::Add<T> for U {
    type Output = X;
    fn add(self, _rhs: T) -> X {
        X;
    }
}

// Drop (~T)
// manually drop(obj), then it will not call drop exiting scope
impl Drop for Droppable {
    fn drop(&mut self) {
        ;
    }
}

// Iterator
struct Fibonacci {
    curr: u32,
    next: u32,
}

impl Iterator for Fibonacci {
    type Item = u32;
    fn next(&mut self) -> Option<u32> {
        let new_next = self.curr + self.next;
        self.curr = self.next;
        self.next = new_next;
        Some(self.curr)
    }
}

// Clone

// macro_rules!
macro_rules! say_hello {
    // no argument
    // extend to println!
    () => (
        println!("Hello");
    )
}

macro_rules! create_function {
    // identity argument
    ($func_name:ident) => (
        fn $func_name() {
            println!("{:?}()", stringify!($func_name));
        }
    )
}

macro_rules! print_result {
    // expression argumnet
    ($expression:expr) => (
        println!("{:?} = {:?}", stringify!($expression), $expression)
    )
}

/*
    block
    expr: expression
    identity: name of variable / function
    item
    pat: pattern
    path
    stmt: statement
    tt: token tree
    ty: type
*/

// macro can overload
macro_rules! test {
    // any template can be used
    ($left:expr; and $right:expr) => (
        println!("{:?} and {:?} is {:?}",
                stringify!($left),
                stringify!($right),
                $left && $right)
    );
    ($left:expr; or $right:expr) => (
        println!("{:?} or {:?} is {:?}",
                stringify!($left),
                stringify!($right),
                $left || $right)
    );
}

// macro argument repeat
macro_rules! find_min {
    ($x:expr) => ($x);
    // one or more $y
    ($x:expr, $($y:expr),+) => (
        // extend parameter
        std::cmp::min($x, find_min!($($y),+))
    )
}

macro_rules! assert_equal_len {
    // token tree is used for operators / tokens
    ($a:ident, $b: ident, $func:ident, $op:tt) => (
        assert!($a.len() == $b.len(),
                "{:?}: dimension mismatch: {:?} {:?} {:?}",
                stringify!($func),
                ($a.len(),),
                stringify!($op),
                ($b.len(),));
    )
}

macro_rules! op {
    ($func:ident, $bound:ident, $op:tt, $method:ident) => (
        fn $func<T: $bound<T, Output=T> + Copy>(xs: &mut Vec<T>, ys: &Vec<T>) {
            assert_equal_len!(xs, ys, $func, $op);
            for (x, y) in xs.iter_mut().zip(ys.iter()) {
                *x = $bound::$method(*x, *y);
                // *x = x.$method(*y);
            }
        }
    )
}

op!(add_assign, Add, +=, add);
op!(mul_assign, Mul, *=, mul);
op!(sub_assign, Sub, -=, sub);

// #[test]: let compiler output test test::function ... ok

// panic: print then unwinding the stack
fn give_princess(gift: &str) {
    if gift == "snake" { panic!("AAAaaaaa!!!!"); }
    println!("I love {}s!!!!!", gift);
}

fn give_commoner(gift: Option<&str>) {
    match gift {
        Some("snake") => println!("Yuck! I'm throwing that snake in a fire."),
        Some(inner) => println!("{}? How nice.", inner),
        None => println!("No gift? Oh well."),
    }
}

fn give_princess(gift: Option<&str>) {
    // panic when unwrap a None
    let inside = gift.unwrap();
    if inside == "snake" { panic!("AAAaaaaa!!!!"); }
    println!("I love {}s!!!!!", inside);
}

// Functor map: m a -> (a -> b) -> m b
// Monad and_then: m a -> (a -> m b) -> m b

// Option<T> -> Some<T>, None
// Result<T, E> -> Ok<T>, Err<E>
fn double_number(number_str: &str) -> Result<i32, ParseIntError> {
    match number_str.parse::<i32>() {
        // 10
        Ok(n) => Ok(2 * n),
        // t
        Err(e) => Err(e),
    }
}

use std::num::ParseIntError;

type AliasedResult<T> = Result<T, ParseIntError>;

type Result<T> = std::result::Result<T, String>;

fn double_first(vec: Vec<&str>) -> Result<i32> {
    vec.first()
    // Option<T> -> Result<T, String>
    .ok_or("Please use a vector with at least one element.".to_owned())
    // Result<T, ParseIntError>
    .and_then(|s| s.parse::<i32>()
                    // map Result<T, ParseIntError> -> Result<T, String>
                    .map_err(|e| e.to_string())
                    // Result<T, String> => Result<T, String>
                    .map(|i| 2 * i))
}

// match and return => early return

fn double_first(vec: Vec<&str>) -> Result<i32> {
    let first = try!(vec.first()
                    .ok_or("Please use a vector with at least one element.".to_owned()));
    // try!: unwrap error then return
    let value = try!(first.parse::<i32>()
                                .map_err(|e| e.to_string()));
    Ok(2 * value)
}

#[derive(Debug)]
enum DoubleError {
    EmptyVec,
    Parse(ParseIntError),
}
// try! automatically call ParseIntError => DoubleError
impl From<ParseIntError> for DoubleError {
    fn from(err: ParseIntError) -> DoubleError {
        DoubleError::Parse(err)
    }
}

impl fmt::Display for DoubleError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        match *self {
            DoubleError::EmptyVec =>
            write!(f, "please use a vector with at least one element"),
            DoubleError::Parse(ref e) => e.fmt(f),
        }
    }
}

fn double_first(vec: Vec<&str>) -> Result<i32> {
    let first = try!(vec.first().ok_or(DoubleError::EmptyVec));
    let parsed = try!(first.parse::<i32>());
    Ok(2 * parsed)
}

// Box<Error>: Error trait object => Box<Error>

type Result<T> = std::result::Result<T, Box<error::Error>>;

impl error::Error for DoubleError {
    fn description(&self) -> &str {
        match *self {
            DoubleError::EmptyVec => "empty vectors not allowed",
            DoubleError::Parse(ref e) => e.description(),
        }
    }
    fn cause(&self) -> Option<&error : Error> {
        match *self {
            DoubleError::EmptyVec => None,
            // since ParseIntputError implements Error
            DoubleError::Parse(ref e) => Some(e),
        }
    }
}

// Box<T>: heap, like unique_ptr<T>
// Vec<T>: slice as &[T]
// String: Vec<u8> on heap
// &str: &[u8]
// ? operator == try!
// HashMap<T : Eq + Hash, U>
// HashSet<T> = HashMap<T, ()>

// Thread spawn
use std::thread;
static NTHREADS: i32 = 10;
fn test11() {
    let mut children = vec![];
    for i in 0..NTHREADS {
        children.push(thread::spawn(move || {
            println!("this is thread number {}", i)
        }));
    }
    for child in children {
        let _ = child.join();
    }
}

use std::sync::mpsc::{Sender, Receiver};
use std::sync::mpsc;
use std::thread;
static NTHREADS: i32 = 3;

fn test12() {
    let (tx, rx): (Sender<i32>, Receiver<i32>) = mpsc::channel();
    for id in 0..NTHREADS {
        // sender can be cloned
        let thread_tx = tx.clone();

        thread::spawn(move || {
            // take ownership of thread_tx
            // blocking
            thread_tx.send(id).unwrap();
            println!("thread {} finished", id);
        });
    }
    let mut ids = Vec::with_capacity(NTHREADS as usize);
    for _ in 0..NTHREADS {
        // blocking
        ids.push(rx.recv());
    }
    println!("{:?}", ids);
}

// Path / posix::Path / windows::Path / FileStat

// File::open/read_to_string(&mut s)/create/write_all(as_bytes)

use std::process::Command;

fn test13() {
    let output = Command::new("rustc")
        .arg("--version")
        .output().unwrap_or_else(|e| {
            panic!("failed to execute process: {}", e)
        });
    if output.status.success() {
        let s = String::from_utf8_lossy(&output.stdout);
        print!("rustc succeeded and stdout was:\n{}", s);
    } else {
        let s = String::from_utf8_lossy(&output.stderr);
        print!("rustc failed and stderr was:\n{}", s);
    }
}

// process.stdin.unwrap().write_all

// std::env::args

// link extern to lib m
#[link(name = "m")]
extern {
    fn csqrtf(z: Complex) -> Complex;
}

#[repr(C)]
#[derive(Clone, Copy)]
struct Complex {
    re: i32,
    im: i32,
}

fn sqrt(z: Complex) -> Complex {
    unsafe { csqrtf(z) }
}

// Documentation: ///

// Test
// #[test]: func: () -> ()
// #[should_panic]

/* 
Unsafe
    deference raw pointer
    FFI
    std::mem::transmute
    inline assembly
*/

fn test14() {
    let raw_p : *const u32 = &10;
    unsafe {
        assert!(*raw_p == 10);
    }
    
    let u: &[u8] = &[49, 50, 51];
    unsafe {
        assert!(u == std::mem::transmute::<&str, &[u8]>("123"));
    }   
}

#![feature(asm)]

#[cfg(any(target_arch = "x86", target_arch = "x86_64"))]
fn foo() {
    unsafe {
        asm!("add $2, $0"
             : "=r"(c)
             : "0"(a), "r"(b)
             "eax");
    }
}
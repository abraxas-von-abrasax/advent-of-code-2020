use std::fs;

#[cfg(windows)]
const LINE_ENDING: &'static str = "\r\n";
#[cfg(not(windows))]
const LINE_ENDING: &'static str = "\n";

struct Password {
    test_char: char,
    min: u32,
    max: u32,
    pwd: String,
}

fn read_input() -> Vec<Password> {
    let contents = fs::read_to_string("src/input.txt")
        .expect("Something went wrong while reading the file");
    return contents.trim().split(LINE_ENDING)
        .map(|s| {
            let dash_split: Vec<&str> = s.split('-').collect();
            let min = String::from(dash_split[0]);
            let min: u32 = min.parse().unwrap();

            let ws_split: Vec<&str> = dash_split[1].split(' ').collect();

            let max = String::from(ws_split[0]);
            let max: u32 = max.parse().unwrap();

            let test_char = String::from(ws_split[1]);
            let test_char = test_char[..1].chars().collect::<Vec<char>>()[0];


            let pwd = String::from(ws_split[2]);

            return Password { test_char, min, max, pwd };
        })
        .collect()
}

fn pwd_is_correct(pwd: &Password) -> bool {
    let mut found = 0;

    for c in pwd.pwd.chars() {
        if c == pwd.test_char {
            found += 1;
        }
    }

    found >= pwd.min && found <= pwd.max
}

fn solve_first(passwords: &Vec<Password>) -> u32 {
    let mut result = 0;
    for pwd in passwords.iter() {
        if pwd_is_correct(pwd) {
            result += 1;
        }
    }
    return result;
}

fn solve_second(passwords: &Vec<Password>) -> u32 {
    let mut result = 0;
    for pwd in passwords.iter() {
        let pwd_chars: Vec<char> = pwd.pwd.chars().collect();
        let first_char_correct = match pwd_chars.get((pwd.min - 1) as usize) {
            Some(c) => *c == pwd.test_char,
            None => continue
        };
        let second_char_correct = match pwd_chars.get((pwd.max - 1) as usize) {
            Some(c) => *c == pwd.test_char,
            None => continue
        };

        if (first_char_correct && !second_char_correct) || (!first_char_correct && second_char_correct) {
            result += 1;
        }
    }
    return result;
}

fn main() {
    let passwords = read_input();
    println!("Solution first part: {}", solve_first(&passwords));
    println!("Solution second part: {}", solve_second(&passwords));
}

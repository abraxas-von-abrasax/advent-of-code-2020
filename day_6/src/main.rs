use std::fs;
use array_tool::vec::Intersect;

#[cfg(windows)]
const LINE_ENDING: &'static str = "\r\n";
#[cfg(not(windows))]
const LINE_ENDING: &'static str = "\n";


fn get_file_content() -> Vec<String> {
    let contents = fs::read_to_string("src/input.txt")
        .expect("Could not read input.");
    contents.split(LINE_ENDING).map(|row| String::from(row)).collect()
}

fn solve_first(contents: &Vec<String>) -> u32 {
    let mut rows: Vec<String> = Vec::new();
    let mut row_chars: Vec<char> = Vec::new();

    for row in contents.iter() {
        for c in row.chars() {
            row_chars.push(c);
        }
        if row.is_empty() {
            row_chars.sort();
            row_chars.dedup();
            rows.push(row_chars.iter().collect());
            row_chars.clear();
        }
    }

    let mut sum = 0;
    for el in rows.iter() {
        sum += el.len();
    }
    sum as u32
}

fn solve_second(contents: &Vec<String>) -> u32 {
    let mut sum = 0;
    let mut row_chars: Vec<char> = Vec::new();
    let mut new_group = true;

    for row in contents.iter() {
        if row.is_empty() {
            sum += row_chars.len();
            row_chars.clear();
            new_group = true;
            continue;
        }

        let mut new_row: Vec<char> = row.chars().collect::<String>().trim().chars().collect();
        new_row.sort();
        new_row.dedup();
        if row_chars.is_empty() && new_group {
            row_chars = new_row.clone();
        } else {
            row_chars = row_chars.intersect(new_row);
        }
        new_group = false;
    }
    sum as u32
}

fn main() {
    let content = get_file_content();
    println!("Solution first part: {}", solve_first(&content));
    println!("Solution second part: {}", solve_second(&content));
}

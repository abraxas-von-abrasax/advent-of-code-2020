use std::fs;
use std::ptr;

fn read_file(file_name: &str) -> Vec<i32> {
    let contents = fs::read_to_string(file_name)
        .expect("Something went wrong while reading the file");
    return contents.trim().split('\n')
        .map(|s| String::from(s))
        .map(|s| s.parse::<i32>().expect("Cannot parse string."))
        .collect()
}

fn solve_first(input: &Vec<i32>) -> Option<i32> {
    for &num in input.iter() {
        for &other_num in input.iter() {
            if ptr::eq(&num, &other_num) {
                continue;
            }
            if num + other_num == 2020 {
                return Some(num * other_num);
            }
        }
    }
    return None;
}

fn solve_second(input: &Vec<i32>) -> Option<i32> {
    for &num in input.iter() {
        for &other_num in input.iter() {
            if ptr::eq(&num, &other_num) {
                continue;
            }
            for &third_num in input.iter() {
                if ptr::eq(&num, &third_num) | ptr::eq(&other_num, &third_num) {
                    continue;
                }

                if num + other_num + third_num == 2020 {
                    return Some(num * other_num * third_num);
                }
            }
        }
    }
    return None;
}

fn main() {
    let input = read_file("./src/input_1.txt");
    if let Some(res) = solve_first(&input) {
        println!("Solution first part: {}", res);
    } else {
        println!("Couldn't find a solution for the first part.");
    }

    if let Some(res) = solve_second(&input) {
        println!("Solution second part: {}", res);
    } else {
        println!("Couldn't find a solution for the second part.");
    }
}

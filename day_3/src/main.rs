use std::fs;

type Field = Vec<Vec<FieldType>>;

enum FieldType {
    EMPTY,
    TREE,
}

fn get_input() -> Field {
    let contents = fs::read_to_string("src/input.txt")
        .expect("Could not read input.");
    contents.trim().split('\n')
        .map(|row|
            row.chars()
                .map(|c| if c == '.' { FieldType::EMPTY } else { FieldType::TREE })
                .collect()
        )
        .collect()
}

fn traverse(field: &Field, right: usize, down: usize) -> u32 {
    let col_length = field.len();
    let row_length = field[0].len();

    let mut trees_found = 0;

    let mut row_index = 0;
    let mut col_index = 0;

    loop {
        row_index = (row_index + right) % row_length;
        col_index += down;
        if col_index >= col_length {
            break;
        }
        if let FieldType::TREE = field[col_index][row_index] {
            trees_found += 1;
        }
    }

    trees_found
}

fn solve_first(field: &Field) -> u32 {
    traverse(&field, 3, 1)
}

fn solve_second(field: &Field) -> u32 {
    let mut trees_found = traverse(&field, 1, 1);
    trees_found *= traverse(&field, 3, 1);
    trees_found *= traverse(&field, 5, 1);
    trees_found *= traverse(&field, 7, 1);
    trees_found *= traverse(&field, 1, 2);
    trees_found
}

fn main() {
    let field = get_input();
    println!("Solution first part: {}", solve_first(&field));
    println!("Solution second part: {}", solve_second(&field));
}

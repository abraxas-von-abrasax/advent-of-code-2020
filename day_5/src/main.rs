use std::fs;

enum SpaceChar {
    ROW(char),
    COL(char)
}

impl SpaceChar {
    fn get_num_char(sc: SpaceChar) -> char {
        match sc {
            SpaceChar::ROW(c) => if c == 'B' { '1' } else { '0' },
            SpaceChar::COL(c) => if c == 'R' { '1' } else { '0' },
        }
    }
}

struct Seat {
    row: u32,
    col: u32,
}

impl Seat {
    fn new(space_id: String) -> Seat {
        let mut row_str = String::new();
        let mut col_str = String::new();
        for c in space_id[0..space_id.len() - 3].chars().collect::<Vec<char>>().iter() {
            row_str.push(SpaceChar::get_num_char(SpaceChar::ROW(*c)));
        }
        for c in space_id[space_id.len() - 3..space_id.len()].chars().collect::<Vec<char>>().iter() {
            col_str.push(SpaceChar::get_num_char(SpaceChar::COL(*c)));
        }
        Seat {
            row: u32::from_str_radix(&row_str[..], 2).unwrap(),
            col: u32::from_str_radix(&col_str[..], 2).unwrap(),
        }
    }

    fn get_id(&self) -> u32 {
        self.row * 8 + self.col
    }
}

fn get_input() -> Vec<Seat> {
    let contents = fs::read_to_string("src/input.txt")
        .expect("Could not read input.");
    contents.trim()
        .split('\n')
        .map(|row| Seat::new(String::from(row)))
        .collect::<Vec<Seat>>()
}

fn solve_first(seats: &Vec<Seat>) -> u32 {
    let mut biggest_id = 0;
    for seat in seats.iter() {
        let new_id = seat.get_id();
        if new_id > biggest_id {
            biggest_id = new_id;
        }
    }
    biggest_id
}

fn solve_second(seats: &Vec<Seat>) -> u32 {
    let mut seat_ids: Vec<u32> = Vec::new();
    for seat in seats.iter() {
        if seat.row == 0 || seat.row == 127 {
            continue;
        }

        seat_ids.push(seat.get_id());
    }

    seat_ids.sort();

    for seat_id in seat_ids.iter() {
        if !seat_ids.contains(&(seat_id + 1)) {
            return seat_id + 1;
        }
    }

    0
}

fn main() {
    let seats = get_input();
    println!("Solution first part: {}", solve_first(&seats));
    println!("Solution second part: {}", solve_second(&seats));
}

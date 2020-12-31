use std::fs;
use regex::Regex;

#[cfg(windows)]
const LINE_ENDING: &'static str = "\r\n";
#[cfg(not(windows))]
const LINE_ENDING: &'static str = "\n";

struct Passport {
    byr: Option<u16>,
    iyr: Option<u16>,
    eyr: Option<u16>,
    hgt: Option<String>,
    hcl: Option<String>,
    ecl: Option<String>,
    pid: Option<String>,
    cid: Option<String>,
}

impl Passport {
    fn is_valid(&self) -> bool {
        self.byr != None && self.iyr != None && self.eyr != None && self.hgt != None && self.hcl != None &&
            self.ecl != None && self.pid != None
    }

    fn new() -> Passport {
        Passport {
            byr: None,
            iyr: None,
            eyr: None,
            hgt: None,
            hcl: None,
            ecl: None,
            pid: None,
            cid: None,
        }
    }

    fn fields_are_valid(&self) -> bool {
        if !self.is_valid() {
            return false;
        }

        if self.byr.unwrap() < 1920 || self.byr.unwrap() > 2002 {
            return false;
        }

        if self.iyr.unwrap() < 2010 || self.iyr.unwrap() > 2020 {
            return false;
        }

        if self.eyr.unwrap() < 2020 || self.eyr.unwrap() > 2030 {
            return false;
        }

        let mut hgt = self.hgt.as_ref().unwrap().clone();
        hgt.drain(hgt.len() - 2..hgt.len());
        let hgt_num: u32 = match hgt.parse() {
            Ok(res) => res,
            Err(_) => return false,
        };

        if self.hgt.as_ref().unwrap().ends_with("cm") {
            if hgt_num < 150 || hgt_num > 193 {
                return false;
            }
        } else if self.hgt.as_ref().unwrap().ends_with("in") {
            if hgt_num < 59 || hgt_num > 76 {
                return false;
            }
        } else {
            return false;
        }

        let hcl_regex = Regex::new(r"^\#[0-9a-f]{6}").unwrap();
        if !hcl_regex.is_match(&self.hcl.as_ref().unwrap()[..]) {
            return false;
        }

        match &self.ecl.as_ref().unwrap()[..] {
            "amb" | "blu" | "brn" | "gry" | "grn" | "hzl" | "oth" => (),
            _ => return false,
        }

        let pid_regex = Regex::new(r"\d{9}").unwrap();
        if self.pid.as_ref().unwrap().len() != 9 || !pid_regex.is_match(&self.pid.as_ref().unwrap()[..]) {
            return false;
        }

        true
    }

    fn set(&mut self, key: &str, val: &str) {
        match key {
            "byr" => self.byr = Some(String::from(val).parse().expect("Cannot parse string for byr.")),
            "iyr" => self.iyr = Some(String::from(val).parse().expect("Cannot parse string for iyr.")),
            "eyr" => self.eyr = Some(String::from(val).parse().expect("Cannot parse string for eyr.")),
            "hgt" => self.hgt = Some(String::from(val)),
            "hcl" => self.hcl = Some(String::from(val)),
            "ecl" => self.ecl = Some(String::from(val)),
            "pid" => self.pid = Some(String::from(val)),
            "cid" => self.cid = Some(String::from(val)),
            err => panic!("Can't map key {} to Passport object", err),
        }
    }
}

fn get_input() -> Vec<Passport> {
    let contents = fs::read_to_string("src/input.txt")
        .expect("Could not read input.");
    let contents: Vec<&str> = contents.split(LINE_ENDING).collect();

    let mut passports: Vec<Passport> = Vec::new();
    let mut passport_row = String::new();

    for row in contents.iter() {
        passport_row.push(' ');
        passport_row.push_str(row);
        if row.is_empty() {
            passport_row = String::from(passport_row.trim());
            let mut new_passport = Passport::new();
            for field in passport_row.split(' ') {
                let field_values = field.split(':').collect::<Vec<&str>>();
                let k = field_values[0];
                let v = field_values[1];
                new_passport.set(k, v);
            }
            passports.push(new_passport);
            passport_row.clear();
        }
    }

    passports
}

fn solve_first(passports: &Vec<Passport>) -> u32 {
    passports.iter().filter(|passport| passport.is_valid()).collect::<Vec<&Passport>>().len() as u32
}

fn solve_second(passports: &Vec<Passport>) -> u32 {
    passports.iter().filter(|passport| passport.fields_are_valid()).collect::<Vec<&Passport>>().len() as u32
}

fn main() {
    let passports = get_input();
    println!("Solution first part: {}", solve_first(&passports));
    println!("Solution second part: {}", solve_second(&passports));
}

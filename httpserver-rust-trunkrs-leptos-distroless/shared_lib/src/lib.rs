pub struct MyStruct {
    pub field: i64,
}

impl MyStruct {
    pub fn new(field: i64) -> Self {
        Self { field }
    }

    pub fn get_field(&self) -> i64 {
        self.field
    }
}

pub fn add(left: i64, right: i64) -> i64 {
    left + right
}

pub fn subtract(left: i64, right: i64) -> i64 {
    left - right
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn it_adds() {
        let result = add(2, 2);
        assert_eq!(result, 4);
    }

    #[test]
    fn it_subtracts() {
        let result = subtract(4, 2);
        assert_eq!(result, 2);
    }

    #[test]
    fn it_subtracts_2() {
        let result = subtract(2, 4);
        assert_eq!(result, -2);
    }
}

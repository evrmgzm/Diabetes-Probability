fn euclidean_distance(vector1: &[f64], vector2: &[f64]) -> f64 {
    if vector1.len() != vector2.len() {
        panic!("Vectors must be of the same length");
    }
    let squared_difference: f64 = vector1.iter()
        .zip(vector2.iter())
        .map(|(x, y)| (x - y).powi(2))
        .sum();
    squared_difference.sqrt()
}

fn main() {
    let v1 = vec![1.0, 2.0, 3.0];
    let v2 = vec![4.0, 5.0, 6.0];
    let distance = euclidean_distance(&v1, &v2);
    println!("Euclidean Distance: {}", distance);
}

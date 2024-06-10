package main

import (
    "fmt"
    "math"
)

func euclideanDistance(vector1, vector2 []float64) float64 {
    if len(vector1) != len(vector2) {
        panic("Vectors must be of the same length")
    }
    var squaredDifference float64
    for i := range vector1 {
        squaredDifference += math.Pow(vector1[i]-vector2[i], 2)
    }
    return math.Sqrt(squaredDifference)
}

func main() {
    v1 := []float64{1.0, 2.0, 3.0}
    v2 := []float64{4.0, 5.0, 6.0}
    distance := euclideanDistance(v1, v2)
    fmt.Println("Euclidean Distance:", distance)
}

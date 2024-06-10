def euclidean_distance(vector1, vector2)
    if vector1.length != vector2.length
      raise "Vectors must be of the same length"
    end
    squared_difference = vector1.zip(vector2).map { |x, y| (x - y) ** 2 }.sum
    Math.sqrt(squared_difference)
  end
  
  v1 = [1.0, 2.0, 3.0]
  v2 = [4.0, 5.0, 6.0]
  distance = euclidean_distance(v1, v2)
  puts "Euclidean Distance: #{distance}"
  
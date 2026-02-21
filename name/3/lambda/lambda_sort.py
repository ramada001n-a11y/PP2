students_scores = [("Али", 85), ("Диас", 92), ("Бека", 78)] #tuple

# Сортировка по второму значению
students_scores.sort(key=lambda x: x[1]) 

print(students_scores) 
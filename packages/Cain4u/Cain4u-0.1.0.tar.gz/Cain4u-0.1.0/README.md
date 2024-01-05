# Hack4u  Academy Courses Library
Una biblioteca en pyhton para consultar cursos de la academia Hack4u
## Cursos Disponibles:

- Introducción a Linux [15 Horas]
- Personalizacion de Linux [3 Horas]
- Introduccion al Hacking [53 Horas]

## Instalacion 
 
Instala el paque usando `pip3`:

```python3
pip3 install hack4u
```
## Uso basico

### Listar todos los cursos
```python
from hack4u import list_courses

for course in list_courses():
    print(course)
```

### Obtener el curso por nombre
```python
from hack4u import get_course_by_name
course = get_course_by_name("Introducción a Linux")
print(course)
```
### calcular duracion total de todos los cursos
```python3
from hack4u.utils import total_duration
```

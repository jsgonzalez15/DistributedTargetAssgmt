# Distributed Target Assgmt
## Descripción
El proyecto se realiza para simular el desempeño energético de un algoritmo de control distribuido para flotas de vehículos con restricciones energéticas. El algoritmo consiste en la partición del área de operación en nodos con líderes para asignación intranodal e internodal. Cada vehículo conoce la información inicial de la misión y la información actualizada de su nodo. Los líderes realizan asignaciones según el consumo estimado con la distancia de cada vehículo y el consumo por distancia respectivo.
## Contenidos en Simulación
Réplica del método distribuido GRID target Assignment y su extensión a asignación de tareas no monotónicas: Smith, Stephen Leslie. Task allocation and vehicle routing in dynamic environments. University of California, Santa Barbara, 2009.

Simulación de propuesta de algoritmo de control distribuido con planteamiento de grafos cómo mejora de GRID target Assgmt a asignación no monotónica con restricciones energéticas, despliegue y recolección en puntos de recolección.

Simulación de asignación internodal GRID adaptada a algoritmo propuesto para comparación directa de desempeño.

Simulación de consumo promedio para variación en tamaño de la flota y variación de número de particiones GRID junto con la desviación respectiva.

## Ejecución y resultados
Para ejecutar el algoritmo únicamente es necesario eejcutar el archivo TesisModelRun. En este archivo pueden modificarse las variables booleanas para obtener un video de la simulación y simular alguno de los algoritmos propuestos. Es posible variar la cantidad de objetivos, divisiones del área de operaciones, número de objetivos por vehículo y número de puntos de recolección. Los resultados de esta simulación se almacenan en archivos JSON para la obtención de gráficas asociadas.

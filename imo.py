# desde el año 2000 al 2022 analisis
# variables obligatorias
tabla_imo = "imo"
capa_world = "Mapa del mundo"

#opcional
exp = "coalesce(scale_exp(\"imo_total\", 0, 15, 1, 12, 0.57), 0)"

#.......... pyqgis ................
from qgis.core import *
# Seleccionar solo los primeros puestos
mi_capa = QgsProject.instance().mapLayersByName(tabla_imo)[0]
expression = ' OR '.join(['"{}" = 1'.format(i) for i in range(0, 23)])
mi_capa.selectByExpression(expression, QgsVectorLayer.SetSelection)
mi_capa = QgsProject.instance().mapLayersByName(tabla_imo)[0]
group_ones = {}
for f in mi_capa.selectedFeatures():
    pais_val = f['pais']
    if pais_val not in group_ones:
        group_ones[pais_val] = 0
    count_ones = 0
    for i in range(0, 23):
        try:
            if f['{}'.format(i)] == 1:
                count_ones +=1
        except KeyError:
            pass
    group_ones[pais_val] += count_ones

for key, value in sorted(group_ones.items(), key=lambda item: item[1], reverse=True):
    print("{} 1° Puesto desde 2000 - 2020 Total: {}".format(key, value))
    
    
    
# Crear el nuevo atributo en la capa
mi_capa = QgsProject.instance().mapLayersByName(tabla_imo)[0]
mi_capa.startEditing()
mi_capa.addAttribute(QgsField("total", QVariant.Int))

# Asignar el valor del diccionario a cada feature
for f in mi_capa.selectedFeatures():
    pais_val = f['pais']
    f.setAttribute("total", group_ones[pais_val])
    mi_capa.updateFeature(f)

mi_capa.commitChanges()

from qgis.core import QgsProject, QgsVectorLayerJoinInfo

# Obtener las capas
map_world = QgsProject.instance().mapLayersByName(capa_world)[0]
mi_capa = QgsProject.instance().mapLayersByName(tabla_imo)[0]

# Crear el join
join_info = QgsVectorLayerJoinInfo()
join_info.setJoinFieldName("pais")
join_info.setTargetFieldName("WB_A3")
join_info.setJoinLayer(mi_capa)
join_info.setUsingMemoryCache(True)
map_world.addJoin(join_info)

# Guardar el resultado en una nueva capa
QgsProject.instance().addMapLayer(map_world, False)
map_world.setName("Mapa del mundo")

# centroides
layer = QgsProject.instance().mapLayersByName("Mapa del mundo")[0]

# Obtener la capa
params = {'INPUT': layer, 
          'ALL_PARTS':False,
          'OUTPUT': 'memory:'}

newLayer = processing.run("native:pointonsurface", params)
layerOutput = newLayer['OUTPUT']
QgsProject.instance().addMapLayer(layerOutput)

# simbologias
layer1 = QgsProject.instance().mapLayersByName("output")[0]
symbol = QgsMarkerSymbol()
symbol.setColor(QColor(12, 180, 120))
symbol.setDataDefinedSize(QgsProperty.fromExpression(exp))
renderer = QgsSingleSymbolRenderer(symbol)
layer1.setRenderer(renderer)







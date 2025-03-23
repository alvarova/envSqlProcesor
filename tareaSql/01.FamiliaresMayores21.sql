//mayores a 21 años - personas sin discapacidad
update grupo_familiar
set id_parentesco = 4, es_estudiante = 0
where id_parentesco = 3 
and es_discapacitado = 0
and (YEAR(CURDATE())-YEAR(gf.fecha_nacimiento_fliar) + IF(DATE_FORMAT(CURDATE(),'%m-%d') > DATE_FORMAT(gf.fecha_nacimiento_fliar,'%m-%d'), 0 , -1 )) between 21 and 25

//mayores a 26 años - personas sin discapacidad
update grupo_familiar
set id_parentesco = 7, es_estudiante = 0
where id_parentesco in (3,4) 
and es_discapacitado = 0
and (YEAR(CURDATE())-YEAR(gf.fecha_nacimiento_fliar) + IF(DATE_FORMAT(CURDATE(),'%m-%d') > DATE_FORMAT(gf.fecha_nacimiento_fliar,'%m-%d'), 0 , -1 )) > 25


//mayores a 21 años - personas con discapacidad
update grupo_familiar
set id_parentesco = 4
where id_parentesco = 3 
and es_discapacitado = 1
and (YEAR(CURDATE())-YEAR(gf.fecha_nacimiento_fliar) + IF(DATE_FORMAT(CURDATE(),'%m-%d') > DATE_FORMAT(gf.fecha_nacimiento_fliar,'%m-%d'), 0 , -1 )) between 21 and 25

//mayores a 26 años - personas con discapacidad
update grupo_familiar
set id_parentesco = 7
where id_parentesco in (3,4) 
and es_discapacitado = 1
and (YEAR(CURDATE())-YEAR(gf.fecha_nacimiento_fliar) + IF(DATE_FORMAT(CURDATE(),'%m-%d') > DATE_FORMAT(gf.fecha_nacimiento_fliar,'%m-%d'), 0 , -1 )) > 25
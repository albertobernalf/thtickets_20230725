select * from tickets_empleados;

select * from tickets_sedes;

select * from tickets_tiposempleadosperfil;

2989207 "ROJAS ARGUELLO JEFFERSON EDUARDO"
1234



select * from tickets_sedes;
select * from tickets_tickets  where "visibleTicketEmpleado" = 'S';
select * from tickets_tickets  order by id ;  --where "visibleTicketEmpleado" = 'S';

update tickets_tickets set "estadoRespuestaCoordinador"='Pendiente' where id=11;

select empleado_id, count(*)
from tickets_tickets
group by empleado_id
order by empleado_id

39678113  MENDEZ MORA LADY MILENA  tp=2  empleados
123

52888300 FERNANDEZ GARZON MARIA JIMENA  tp= 1  coordinadors
123
23030123 PEÃ‘ARANDA AGUIRRE LEONOR ISABEL tp=3 talento humano
123

update tickets_empleados set "tiposEmpleadoPerfil_id"=3 where cedula= '23030123';
 
select * from tickets_areas;

select * from tickets_mallaturnos where ano=2023 and mes=4;

SELECT ticket.id,ticket."tiposTicket_id",  tiposticket.nombre nombreTiposTicket ,to_char(ticket.fecha,'YYYY-MM-DD HH:MM.SS'),empleado_id empleado,"sedeInicial_id",
"tiposTurnoInicial_id",tiposturno.nombre nombreTiposTurnoInicial,  to_char(ticket."desdeInicial",'YYYY-MM-DD HH:MM.SS'),to_char(ticket."hastaInicial",'YYYY-MM-DD HH:MM.SS') , 
"sedeReemplazo_id" sedeReemplazo, reemplazo_id reemplazo,
 "respuestaEmpleadoCoordinador_id" respuestaEmpleadoCoordinador,coord.nombre nombreCoordinador,  "textoRespuestaCoordinador" textoRespuestaCoordinador, "estadoRespuestaCoordinador" estadoRespuestaCoordinador,
"respuestaEmpleadoThumano_id" respuestaEmpleadoThumano, thumano.nombre nombreTHumano, "textoRespuestaThumano" textoRespuestaThumano,"estadoRespuestaThumano" estadoRespuestaThumano, 
"visibleTicketEmpleado" visibleTicketEmpleado  , emp.nombre nombreEmpleado, sedesi.nom_sede nomSedeinicial, sedesf.nom_sede nomSedeFinal, 
tiposturnof.nombre nombreTiposTurnoFinal,sedesr.nom_sede nomSedeReemplazo,empr.nombre nombreEmpleadoReemplazo  
FROM tickets_tickets  ticket 
INNER JOIN tickets_tiposticket tiposticket ON (tiposticket.id = ticket."tiposTicket_id") 
LEFT JOIN tickets_tiposturno tiposturno   ON (tiposturno.id = ticket."tiposTurnoInicial_id" ) 
INNER JOIN tickets_empleados emp on (emp.id = ticket.empleado_id ) 
LEFT JOIN tickets_sedes sedesi on (sedesi.id = ticket."sedeInicial_id") 
LEFT JOIN tickets_sedes sedesf on (sedesf.id = ticket."sedeFinal_id") 
LEFT JOIN tickets_tiposturno tiposturnof on (tiposturnof.id = ticket."tiposTurnoFinal_id" ) 
LEFT JOIN tickets_sedes sedesr on (sedesr.id = ticket."sedeReemplazo_id") 
LEFT JOIN tickets_empleados empr on (empR.id = ticket.reemplazo_id ) 
LEFT JOIN tickets_empleados coord on (coord.id = ticket."respuestaEmpleadoCoordinador_id" ) 
LEFT JOIN tickets_empleados thumano on (thumano.id = ticket."respuestaEmpleadoThumano_id" ) 
WHERE  ticket.id = 11 

select * from tickets_tickets where id=11;
    



select * from tickets_tickets order by id;

select * from tickets_tickets where asignado_id= 5 order by id;

update tickets_tickets set "estadoRespuestaCoordinador"='Pendiente' where id=4;

select * from tickets_ticketsmalla;
select * from tickets_mallaturnos;

select * from tickets_tickets;

select * from tickets_mallaturnos order by id ;

update tickets_mallaturnos set  area_id=39 where id in (11,12);
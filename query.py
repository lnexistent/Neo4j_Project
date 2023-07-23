from neo4j import GraphDatabase
from geopy.geocoders import Nominatim
from tqdm import tqdm
import random
from datetime import timedelta
from faker import Faker

# Connessione al database Neo4j
driver = GraphDatabase.driver("neo4j+s://f824646d.databases.neo4j.io", auth=("neo4j", "FoqxTbpaU4YiWrJHyY7OrzI2HIevo2anuoUah9WRhNs"))

# Funzione per ottenere le celle telefoniche collegate a una persona in una data e orario specifici
def localizza_persona(data_inizio, data_fine, persona):
    query = (
        "MATCH (persona:Persona {nome: $nome})"
        "MATCH (persona)-[:POSSIEDE]->(sim:SIM)-[r:COLLEGATO_A]->(cella:CellaTelefonica)"
        "WHERE date(r.connected_at) >= date($data_inizio) AND date(r.disconnected_at) <= date($data_fine)"
        "RETURN DISTINCT cella.nome AS cella_telefonica, cella.latitude AS latitudine, cella.longitude AS longitudine"
    )

    with driver.session() as session:
        result = session.run(query, nome=persona, data_inizio=data_inizio, data_fine=data_fine)
        celle_telefoniche = [record["cella_telefonica"] for record in result]

    return celle_telefoniche

def localizza_persona_ora(data, orario, persona):
    query = (
        "MATCH (persona:Persona {nome: $nome})"
        "MATCH (persona)-[:POSSIEDE]->(sim:SIM)-[r:COLLEGATO_A]->(cella:CellaTelefonica)"
        "WHERE datetime($data + 'T' + $orario) >= datetime(r.connected_at) AND datetime($data + 'T' + $orario) <= datetime(r.disconnected_at)"
        "RETURN DISTINCT cella.nome AS cella_telefonica, cella.latitude AS latitudine, cella.longitude AS longitudine"
    )




    with driver.session() as session:
        result = session.run(query, nome=persona, data=data, orario=orario)
        celle_telefoniche = [record["cella_telefonica"] for record in result]

    return celle_telefoniche


'''
 MATCH (persona:Persona {nome: $nome})
 MATCH (persona)-[:POSSIEDE]->(sim:SIM)-[r:COLLEGATO_A]->(cella:CellaTelefonica)
 WHERE datetime($data + 'T' + $orario) >= datetime(r.connected_at) AND datetime($data + 'T' + $orario) <= datetime(r.disconnected_at)
 RETURN DISTINCT cella.nome AS cella_telefonica, cella.latitude AS latitudine, cella.longitude AS longitudine
'''


# Funzione per trovare i sospetti in una zona di reato
def trova_sospetti(data, orario, cella):
    query = (
        "MATCH (cella:CellaTelefonica {nome: $cella})"
        "MATCH (persona:Persona)-[:POSSIEDE]->(sim:SIM)-[r:COLLEGATO_A]->(cella)"
        "WHERE datetime($data + 'T' + $orario) >= datetime(r.connected_at) AND datetime($data + 'T' + $orario) <= datetime(r.disconnected_at)"
        "RETURN DISTINCT persona.nome AS nome_persona"
    )

    with driver.session() as session:
        result = session.run(query, cella=cella, data=data, orario=orario)
        sospetti = [record["nome_persona"] for record in result]

    return sospetti


'''
MATCH (cella:CellaTelefonica {nome: $cella})
MATCH (persona:Persona)-[:POSSIEDE]->(sim:SIM)-[r:COLLEGATO_A]->(cella)
WHERE datetime($data + 'T' + $orario) >= datetime(r.connected_at) AND datetime($data + 'T' + $orario) <= datetime(r.disconnected_at)
RETURN DISTINCT persona.nome AS intestataria
'''

# Funzione per trovare le persone intestatarie delle SIM nelle celle entro un raggio dalle coordinate geografiche
def trova_persone_in_raggio(latitudine, longitudine, raggio, data, orario):
    query = (
        "MATCH (cella:CellaTelefonica) "
        "WHERE cella.latitude IS NOT NULL AND cella.longitude IS NOT NULL "
        "WITH cella, point({ latitude: $latitudine, longitude: $longitudine }) AS reference_point, $raggio as radius, "
        "datetime($data + 'T' + $orario) as start_time, datetime($data + 'T' + $orario) as end_time "
        "WITH cella, reference_point, radius, "
        "point.distance(reference_point, point({ latitude: cella.latitude, longitude: cella.longitude })) AS calculated_distance, start_time, end_time "
        "WHERE calculated_distance <= radius "
        "MATCH (persona:Persona)-[:POSSIEDE]->(sim:SIM)-[r:COLLEGATO_A]->(cella) "
        "WHERE start_time >= datetime(r.connected_at) AND end_time <= datetime(r.disconnected_at) "
        "RETURN DISTINCT persona.nome AS intestataria, sim.serial AS sim_number"
    )

    with driver.session() as session:
        result = session.run(query, latitudine=latitudine, longitudine=longitudine, raggio=raggio, data=data, orario=orario)
        persone_sim = [(record["intestataria"], record["sim_number"]) for record in result]

    return persone_sim


'''
MATCH(cella:CellaTelefonica)
WHEREcella.latitudeISNOTNULLANDcella.longitudeISNOTNULL

WITHcella,point({latitude: $latitude,longitude: $longitude})ASreference_point,$raggioasradius,
datetime($data + 'T' + $orario)asstart_time,datetime($data + 'T' + $orario)asend_time

WITHcella,reference_point,radius,point.distance(reference_point,point({latitude:cella.latitude,longitude:cella.longitude}))AScalculated_distance,start_time,end_time

WHEREcalculated_distance<=radius
MATCH(persona:Persona)-[:POSSIEDE]->(sim:SIM)-[r:COLLEGATO_A]->(cella)
WHEREstart_time>=datetime(r.connected_at)ANDend_time<=datetime(r.disconnected_at)
RETURNDISTINCTpersona.nomeASintestataria,COLLECT(sim.serial)ASsim_numbers

'''
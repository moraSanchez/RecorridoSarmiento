import sqlite3
import os
import json

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), "..", "db", "recorrido_sarmiento.db")
        self.ensure_db_directory()
        self.create_tables()

    def ensure_db_directory(self):
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)

    def create_tables(self):
        """Crea las tablas necesarias si no existen"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Tabla de jugadores
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS jugadores (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nombre TEXT UNIQUE NOT NULL,
                    fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
                    ultima_partida DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Tabla de progreso de partidas
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS partidas_guardadas (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jugador_id INTEGER NOT NULL,
                    escena_actual TEXT NOT NULL,
                    indice_dialogo INTEGER DEFAULT 0,
                    datos_adicionales TEXT, -- JSON con estado del juego
                    fecha_guardado DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (jugador_id) REFERENCES jugadores (id)
                )
            ''')
            
            # Tabla de afinidad con el Linyera
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS afinidad_linyera (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    jugador_id INTEGER UNIQUE NOT NULL,
                    puntos_afinidad INTEGER DEFAULT 0,
                    fecha_actualizacion DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (jugador_id) REFERENCES jugadores (id)
                )
            ''')
            
            conn.commit()
            conn.close()
            print("Tablas verificadas/creadas correctamente")
            
        except Exception as e:
            print(f"Error al crear tablas: {e}")

    def check_table_exists(self):
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='jugadores'")
            table_exists = cursor.fetchone()
            conn.close()
            return table_exists is not None
        except Exception as e:
            print(f"Error al verificar tabla: {e}")
            return False

    def guardar_jugador(self, nombre):
        try:
            if not os.path.exists(self.db_path):
                print("ERROR: La base de datos no existe")
                return None
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT id FROM jugadores WHERE nombre = ?', (nombre,))
            existing_player = cursor.fetchone()
            
            if existing_player:
                cursor.execute('''
                    UPDATE jugadores 
                    SET ultima_partida = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (existing_player[0],))
                player_id = existing_player[0]
                print(f"Jugador existente actualizado: {nombre} (ID: {player_id})")
            else:
                cursor.execute('''
                    INSERT INTO jugadores (nombre) 
                    VALUES (?)
                ''', (nombre,))
                player_id = cursor.lastrowid
                print(f"Nuevo jugador creado: {nombre} (ID: {player_id})")
            
            conn.commit()
            conn.close()
            return player_id
            
        except Exception as e:
            print(f"Error al guardar jugador: {e}")
            return None

    def guardar_progreso(self, jugador_id, escena_actual, indice_dialogo, datos_adicionales=None):
        """Guarda el progreso actual del jugador"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar si ya existe una partida guardada para este jugador
            cursor.execute('''
                SELECT id FROM partidas_guardadas 
                WHERE jugador_id = ?
            ''', (jugador_id,))
            
            partida_existente = cursor.fetchone()
            
            datos_json = json.dumps(datos_adicionales) if datos_adicionales else "{}"
            
            if partida_existente:
                # Actualizar partida existente
                cursor.execute('''
                    UPDATE partidas_guardadas 
                    SET escena_actual = ?, 
                        indice_dialogo = ?, 
                        datos_adicionales = ?,
                        fecha_guardado = CURRENT_TIMESTAMP
                    WHERE jugador_id = ?
                ''', (escena_actual, indice_dialogo, datos_json, jugador_id))
                print(f"Progreso actualizado para jugador {jugador_id}")
            else:
                # Crear nueva partida guardada
                cursor.execute('''
                    INSERT INTO partidas_guardadas 
                    (jugador_id, escena_actual, indice_dialogo, datos_adicionales)
                    VALUES (?, ?, ?, ?)
                ''', (jugador_id, escena_actual, indice_dialogo, datos_json))
                print(f"Nuevo progreso guardado para jugador {jugador_id}")
            
            # Actualizar también la última partida en la tabla jugadores
            cursor.execute('''
                UPDATE jugadores 
                SET ultima_partida = CURRENT_TIMESTAMP 
                WHERE id = ?
            ''', (jugador_id,))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"Error al guardar progreso: {e}")
            return False

    def cargar_progreso(self, jugador_id):
        """Carga el progreso guardado de un jugador"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT escena_actual, indice_dialogo, datos_adicionales
                FROM partidas_guardadas 
                WHERE jugador_id = ?
            ''', (jugador_id,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                escena_actual, indice_dialogo, datos_json = resultado
                datos_adicionales = json.loads(datos_json) if datos_json else {}
                return {
                    "escena_actual": escena_actual,
                    "indice_dialogo": indice_dialogo,
                    "datos_adicionales": datos_adicionales
                }
            else:
                return None
                
        except Exception as e:
            print(f"Error al cargar progreso: {e}")
            return None

    def obtener_todos_los_jugadores(self):
        try:
            if not os.path.exists(self.db_path):
                print("ERROR: La base de datos no existe")
                return []
                
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT j.id, j.nombre, j.fecha_registro, j.ultima_partida,
                       p.escena_actual, p.indice_dialogo
                FROM jugadores j
                LEFT JOIN partidas_guardadas p ON j.id = p.jugador_id
                ORDER BY j.ultima_partida DESC
            ''')
            
            players = cursor.fetchall()
            conn.close()
            return players
            
        except Exception as e:
            print(f"Error al obtener jugadores: {e}")
            return []

    def eliminar_jugador(self, player_id):
        """Elimina un jugador de la base de datos"""
        try:
            if not os.path.exists(self.db_path):
                print("ERROR: La base de datos no existe")
                return False

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Primero eliminar el progreso guardado
            cursor.execute('DELETE FROM partidas_guardadas WHERE jugador_id = ?', (player_id,))
            # Luego eliminar el jugador
            cursor.execute('DELETE FROM jugadores WHERE id = ?', (player_id,))
            
            conn.commit()
            conn.close()
            
            if cursor.rowcount > 0:
                print(f"Jugador con ID {player_id} eliminado correctamente")
                return True
            else:
                print(f"No se encontró jugador con ID {player_id}")
                return False
                
        except Exception as e:
            print(f"Error al eliminar jugador: {e}")
            return False

    # En la clase Database, agrega estos métodos:

    def actualizar_afinidad(self, jugador_id, cambio_puntos):
        """Actualiza los puntos de afinidad (puede ser positivo o negativo)"""
        afinidad_actual = self.obtener_afinidad(jugador_id)
        nueva_afinidad = afinidad_actual + cambio_puntos
        return self.guardar_afinidad(jugador_id, nueva_afinidad)

    def obtener_afinidad(self, jugador_id):
        """Obtiene los puntos de afinidad del jugador"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT puntos_afinidad FROM afinidad_linyera 
                WHERE jugador_id = ?
            ''', (jugador_id,))
            
            resultado = cursor.fetchone()
            conn.close()
            
            if resultado:
                return resultado[0]
            else:
                return 0  # Valor por defecto si no existe
                
        except Exception as e:
            print(f"Error al obtener afinidad: {e}")
            return 0

    def guardar_afinidad(self, jugador_id, puntos_afinidad):
        """Guarda o actualiza los puntos de afinidad del jugador con el Linyera"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar si ya existe afinidad para este jugador
            cursor.execute('''
                SELECT id FROM afinidad_linyera 
                WHERE jugador_id = ?
            ''', (jugador_id,))
            
            afinidad_existente = cursor.fetchone()
            
            if afinidad_existente:
                # Actualizar afinidad existente
                cursor.execute('''
                    UPDATE afinidad_linyera 
                    SET puntos_afinidad = ?,
                        fecha_actualizacion = CURRENT_TIMESTAMP
                    WHERE jugador_id = ?
                ''', (puntos_afinidad, jugador_id))
            else:
                # Crear nueva entrada de afinidad
                cursor.execute('''
                    INSERT INTO afinidad_linyera 
                    (jugador_id, puntos_afinidad)
                    VALUES (?, ?)
                ''', (jugador_id, puntos_afinidad))
            
            conn.commit()
            conn.close()
            print(f"Afinidad guardada: {puntos_afinidad} puntos para jugador {jugador_id}")
            return True
            
        except Exception as e:
            print(f"Error al guardar afinidad: {e}")
            return False

db_manager = Database()
# utils/database.py
import sqlite3
import os

class Database:
    def __init__(self):
        # CORREGIDO: Usar el nombre exacto de tu base de datos
        self.db_path = os.path.join(os.path.dirname(__file__), "..", "db", "recorrido_sarmiento.db")
        self.ensure_db_directory()
        # ELIMINADO: No llamar a init_db automáticamente para no crear tablas nuevas
        print(f"Ruta de la base de datos: {self.db_path}")

    def ensure_db_directory(self):
        """Asegura que el directorio de la base de datos exista"""
        db_dir = os.path.dirname(self.db_path)
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"Directorio de BD creado: {db_dir}")

    def check_table_exists(self):
        """Verifica si la tabla existe sin crearla"""
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
        """Guarda un nuevo jugador o actualiza la fecha de última partida si ya existe"""
        try:
            # Verificar primero si la base de datos y tabla existen
            if not os.path.exists(self.db_path):
                print("ERROR: La base de datos no existe")
                return None
                
            if not self.check_table_exists():
                print("ERROR: La tabla 'jugadores' no existe en la base de datos")
                return None

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar si el jugador ya existe
            cursor.execute('SELECT id FROM jugadores WHERE nombre = ?', (nombre,))
            existing_player = cursor.fetchone()
            
            if existing_player:
                # Actualizar fecha de última partida
                cursor.execute('''
                    UPDATE jugadores 
                    SET ultima_partida = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (existing_player[0],))
                player_id = existing_player[0]
                print(f"Jugador existente actualizado: {nombre} (ID: {player_id})")
            else:
                # Insertar nuevo jugador
                cursor.execute('''
                    INSERT INTO jugadores (nombre) 
                    VALUES (?)
                ''', (nombre,))
                player_id = cursor.lastrowid
                print(f"Nuevo jugador guardado: {nombre} (ID: {player_id})")
            
            conn.commit()
            conn.close()
            return player_id
            
        except Exception as e:
            print(f"Error al guardar jugador: {e}")
            return None

    def obtener_todos_los_jugadores(self):
        """Obtiene todos los jugadores ordenados por última partida"""
        try:
            # Verificar primero si la base de datos y tabla existen
            if not os.path.exists(self.db_path):
                print("ERROR: La base de datos no existe")
                return []
                
            if not self.check_table_exists():
                print("ERROR: La tabla 'jugadores' no existe en la base de datos")
                return []

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, nombre, fecha_registro, ultima_partida 
                FROM jugadores 
                ORDER BY ultima_partida DESC
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
            # Verificar primero si la base de datos y tabla existen
            if not os.path.exists(self.db_path):
                print("ERROR: La base de datos no existe")
                return False
                
            if not self.check_table_exists():
                print("ERROR: La tabla 'jugadores' no existe en la base de datos")
                return False

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
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

# Instancia global para usar en todo el proyecto
db_manager = Database()
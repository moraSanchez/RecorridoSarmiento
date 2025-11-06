import sqlite3
import os

class DatabaseManager:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), 'recorrido_sarmiento.db')
        self.init_database()
    
    def init_database(self):
        """Inicializa la base de datos y crea las tablas si no existen"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Tabla de jugadores
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS jugadores (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                ultima_partida TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla de partidas guardadas (para futuras expansiones)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS partidas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                jugador_id INTEGER,
                escena_actual TEXT,
                progreso TEXT,
                objetos_obtenidos TEXT,
                fecha_guardado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (jugador_id) REFERENCES jugadores (id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def guardar_jugador(self, nombre):
        """Guarda un nuevo jugador en la base de datos"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Verificar si el jugador ya existe
            cursor.execute('SELECT id FROM jugadores WHERE nombre = ?', (nombre,))
            jugador_existente = cursor.fetchone()
            
            if jugador_existente:
                # Actualizar fecha de última partida
                cursor.execute('''
                    UPDATE jugadores 
                    SET ultima_partida = CURRENT_TIMESTAMP 
                    WHERE id = ?
                ''', (jugador_existente[0],))
                jugador_id = jugador_existente[0]
            else:
                # Insertar nuevo jugador
                cursor.execute('INSERT INTO jugadores (nombre) VALUES (?)', (nombre,))
                jugador_id = cursor.lastrowid
            
            conn.commit()
            conn.close()
            return jugador_id
        except Exception as e:
            print(f"Error al guardar jugador: {e}")
            return None
    
    def obtener_ultimo_jugador(self):
        """Obtiene el último jugador registrado"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT nombre FROM jugadores 
                ORDER BY ultima_partida DESC 
                LIMIT 1
            ''')
            resultado = cursor.fetchone()
            
            conn.close()
            return resultado[0] if resultado else None
        except Exception as e:
            print(f"Error al obtener último jugador: {e}")
            return None
    
    def obtener_todos_los_jugadores(self):
        """Obtiene todos los jugadores registrados (para cargar partidas)"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT id, nombre, fecha_registro, ultima_partida 
                FROM jugadores 
                ORDER BY ultima_partida DESC
            ''')
            jugadores = cursor.fetchall()
            
            conn.close()
            return jugadores
        except Exception as e:
            print(f"Error al obtener jugadores: {e}")
            return []

# Instancia global de la base de datos
db_manager = DatabaseManager()
import mysql.connector

def insert_job_offer_into_db(title, company, location, job_type, salary, experience, description, unique_id):
    conn = None
    try:
        conn = mysql.connector.connect(
            user='root',
            password='root',
            host='localhost',
            database='local',
            port=10005
        )
        cursor = conn.cursor()

        # Vérifier si l'offre d'emploi existe déjà dans la base de données
        cursor.execute("SELECT ID FROM wp_posts WHERE post_title = %s AND post_content = %s", (title, description))
        existing_post = cursor.fetchone()
        if existing_post:
            post_id = existing_post[0]
        else: 
            # Insérer l'offre d'emploi dans la table wp_posts
            query = ("""
                INSERT INTO wp_posts (post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, 
                post_status, comment_status, ping_status, post_name, post_modified, post_modified_gmt, post_parent, 
                guid, menu_order, post_type, comment_count, to_ping, pinged, post_content_filtered) 
                VALUES (%s, NOW(), NOW(), %s, %s, '', 'publish', 'closed', 'closed', %s, NOW(), NOW(), 0, '', 0, 'job_listing', 0, '', '', '')
            """)
            data = (1, description, title, unique_id)
            cursor.execute(query, data)
            post_id = cursor.lastrowid

            # Mettre à jour les métadonnées de l'offre d'emploi
            update_postmeta(cursor, post_id, '_application', 'candidature@elzei.fr')
            update_postmeta(cursor, post_id, '_job_location', location)
            update_postmeta(cursor, post_id, '_company_name', company)
            update_postmeta(cursor, post_id, '_job_type', job_type)
            update_postmeta(cursor, post_id, '_salary', salary)
            update_postmeta(cursor, post_id, '_experience_years', experience)

        # Valider la transaction
        conn.commit() 
        print(f"Offre d'emploi '{title}' ajoutée dans la base de données avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur MySQL: {err}")
        conn.rollback()
    finally:
        if conn and conn.is_connected():
            if cursor:
                cursor.close()
            conn.close()

def get_term_taxonomy_id(cursor, job_type):
    cursor.execute("SELECT term_taxonomy_id FROM wp_term_taxonomy WHERE term_id IN (SELECT term_id FROM wp_terms WHERE name = %s)", (job_type,))
    row = cursor.fetchone()
    return row[0] if row else None

def update_postmeta(cursor, post_id, meta_key, meta_value):
    query = ("""
        INSERT INTO wp_postmeta (post_id, meta_key, meta_value) 
        VALUES (%s, %s, %s)
        ON DUPLICATE KEY UPDATE
        meta_value = VALUES(meta_value)
    """)
    cursor.execute(query, (post_id, meta_key, meta_value))

def add_job_to_term_relationships(cursor, post_id, term_taxonomy_id):
    query = """
        INSERT INTO wp_term_relationships (object_id, term_taxonomy_id)
        VALUES (%s, %s)
    """
    cursor.execute(query, (post_id, term_taxonomy_id))

def insert_scraping_history(scraping_date, scraping_status, site_url):
    conn = None
    try:
        conn = mysql.connector.connect(
            user='root',
            password='root',
            host='localhost',
            database='local',
            port=10005
        )
        cursor = conn.cursor()
        
        query = "INSERT INTO scraping_history (scraping_date, scraping_status, site_url) VALUES (%s, %s, %s)"
        data = (scraping_date, scraping_status, site_url)
        cursor.execute(query, data)
        
        conn.commit()
    except mysql.connector.Error as err:
        print(f"Erreur MySQL: {err}")
        conn.rollback()
    finally:
        if conn and conn.is_connected():
            if cursor:
                cursor.close()
            conn.close()

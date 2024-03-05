import mysql.connector

def insert_job_offer_into_db(title, company, location, job_type, description, unique_id):
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
        
        if get_post_id_by_unique_id(cursor, unique_id) is not None:
            print(f"L'offre d'emploi '{title}' existe déjà dans la base de données.")
            return
        
        query = ("""
            INSERT INTO wp_posts (post_author, post_date, post_date_gmt, post_content, post_title, post_excerpt, 
            post_status, comment_status, ping_status, post_name, post_modified, post_modified_gmt, post_parent, 
            guid, menu_order, post_type, comment_count, to_ping, pinged, post_content_filtered) 
            VALUES (%s, NOW(), NOW(), %s, %s, '', 'publish', 'closed', 'closed', %s, NOW(), NOW(), 0, '', 0, 'job_listing', 0, '', '', '')
        """)
        data = (1, description, title, unique_id)

        cursor.execute(query, data)
        post_id = cursor.lastrowid

        update_postmeta(cursor, post_id, '_application', 'candidature@elzei.fr')
        update_postmeta(cursor, post_id, '_job_location', location)
        update_postmeta(cursor, post_id, '_company_name', company)
        update_postmeta(cursor, post_id, '_job_type', job_type)

        freelance_term_id = 9
        add_job_to_term_relationships(cursor, post_id, freelance_term_id)

        conn.commit() 
        print(f"Offre d'emploi '{title}' ajoutée dans la base de données avec succès.")
    except mysql.connector.Error as err:
        print(f"Erreur MySQL: {err}")
    finally:
        if conn and conn.is_connected():
            if cursor:
                cursor.close()
            conn.close()

def get_post_id_by_unique_id(cursor, unique_id):
    cursor.execute("SELECT ID FROM wp_posts WHERE post_name = %s", (unique_id,))
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

def add_job_to_term_relationships(cursor, post_id, term_id):
    query = """
        INSERT INTO wp_term_relationships (object_id, term_taxonomy_id)
        VALUES (%s, %s)
    """
    cursor.execute(query, (post_id, term_id))

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
    finally:
        if conn and conn.is_connected():
            if cursor:
                cursor.close()
            conn.close()

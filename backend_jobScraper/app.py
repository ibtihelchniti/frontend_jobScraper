from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from scrapers.free_work_en import FreeWorkEn
from scrapers.free_work_fr import FreeWorkFr
from scrapers.choose_your_boss import ChooseYourBoss
from utils.webdriver import init_webdriver
from db.database import insert_scraping_history
import mysql.connector
from datetime import datetime
import os
import pandas as pd
import time


app = Flask(__name__)
CORS(app) 

# Route pour le scraping du site Free Work En  
@app.route('/scrape-en', methods=['GET'])
def scrape_jobs():
    try:
        driver = init_webdriver()
        scraper = FreeWorkEn(driver)
        scraper.scrape_jobs()
        
        # Insérer les données dans la base de données pour succès
        insert_scraping_history(datetime.now(), "Success", "https://www.free-work.com/en-gb/tech-it/jobs") 
        
        return jsonify({"success": True, "message": "Scraping terminé avec succès."})
    except Exception as e:
        # En cas d'erreur, insérer l'échec dans la base de données
        insert_scraping_history(datetime.now(), "Failed", "https://www.free-work.com/en-gb/tech-it/jobs")  
        return jsonify({"success": False, "message": str(e)})


# Route pour le scraping du site Free Work Fr
@app.route('/scrape-fr', methods=['GET'])
def scrape_jobs_fr():
    try:
        driver = init_webdriver()
        scraper_fr = FreeWorkFr(driver)
        scraper_fr.scrape_jobs()
        
        # Insérer les données dans la base de données pour succès
        insert_scraping_history(datetime.now(), "Success", "https://www.free-work.com/fr/tech-it/jobs")  
        
        return jsonify({"success": True, "message": "Scraping terminé avec succès pour free work fr."})
    except Exception as e:
        # En cas d'erreur, insérer l'échec dans la base de données
        insert_scraping_history(datetime.now(), "Failed", "https://www.free-work.com/fr/tech-it/jobs") 
        return jsonify({"success": False, "message": str(e)})


# Route pour le scraping du site Choose Your Boss
@app.route('/scrape-ch', methods=['GET'])
def scrape_jobs_ch():
    try:
        driver = init_webdriver()
        scraper_ch = ChooseYourBoss(driver)
        scraper_ch.scrape_jobs()
        
        # Insérer les données dans la base de données pour succès
        insert_scraping_history(datetime.now(), "Success", "https://www.chooseyourboss.com/offres/emploi-it")  
        
        return jsonify({"success": True, "message": "Scraping terminé avec succès pour free work fr."})
    except Exception as e:
        # En cas d'erreur, insérer l'échec dans la base de données
        insert_scraping_history(datetime.now(), "Failed", "https://www.chooseyourboss.com/offres/emploi-it") 
        return jsonify({"success": False, "message": str(e)})
    

# Route pour récupérer l'historique de scraping
@app.route('/scraping-history', methods=['GET'])
def get_scraping_history():
    try:
        conn = mysql.connector.connect(
            user='root',
            password='root',
            host='localhost',
            database='local',
            port=10005
        )
        cursor = conn.cursor(dictionary=True)

        scraping_history = []

        # Sélectionner le site_url distinct pour lesquels on va récupérer les dernières données de scraping
        query = "SELECT DISTINCT site_url FROM scraping_history"
        cursor.execute(query)
        sites = cursor.fetchall()

        # Pour chaque site_url, sélectionner la dernière entrée
        for site in sites:
            query = "SELECT scraping_date, scraping_status FROM scraping_history WHERE site_url = %s ORDER BY scraping_date DESC LIMIT 1"
            cursor.execute(query, (site['site_url'],))
            row = cursor.fetchone()
            if row:
                site_info = {
                    "site_url": site['site_url'],
                    "lastScrapingDate": row['scraping_date'].strftime('%Y-%m-%d %H:%M:%S'),
                    "scrapingStatus": row['scraping_status']
                }
                scraping_history.append(site_info)

        return jsonify(scraping_history)
    except mysql.connector.Error as err:
        print(f"Erreur MySQL: {err}")
        return jsonify({"error": str(err)}), 500
    finally:
        if conn and conn.is_connected():
            if cursor:
                cursor.close()
            conn.close()


# Route pour exporter les données en CSV
@app.route('/export-csv', methods=['GET'])
def export_csv():
    # Récupérer le nom du site à partir de la requête
    site_name = request.args.get('site')

    # Sélectionnez le scraper en fonction du nom du site
    if site_name == 'Free Work En':
        scraper = FreeWorkEn(init_webdriver())
    elif site_name == 'Free Work Fr':
        scraper = FreeWorkFr(init_webdriver())
    elif site_name == 'Choose Your Boss':
        scraper = ChooseYourBoss(init_webdriver())
    else:
        return jsonify({"error": "Site non pris en charge"}), 400

    # Scraper les données pour le site spécifié
    data = scraper.scrape_jobs()

    if data:
        try:
            # Convertir les données en DataFrame Pandas
            df = pd.DataFrame(data)

            # Réorganiser les colonnes selon la structure souhaitée
            df = df[['unique_id', 'title', 'company', 'location', 'job_type', 'salary', 'experience', 'description','logo_url' ]]

            # Générer un nom de fichier unique basé sur le timestamp actuel
            timestamp = int(time.time())
            csv_file_name = f'{site_name.lower().replace(" ", "_")}_{timestamp}.csv'
            csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'csv', csv_file_name))

            # Écrire les données dans un nouveau fichier CSV
            df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')  

            # Retourner le chemin du fichier CSV pour téléchargement
            return send_from_directory(os.path.dirname(csv_file_path), csv_file_name, as_attachment=True)
        except Exception as e:
            return jsonify({"error": f"Erreur lors de l'exportation en CSV : {str(e)}"}), 500
    else:
        return jsonify({"error": "Aucune donnée à exporter"}), 404



if __name__ == '__main__':
    app.run(debug=True)

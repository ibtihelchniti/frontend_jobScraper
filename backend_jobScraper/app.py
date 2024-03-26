from flask import Flask, jsonify, send_file, request
from flask_cors import CORS
from scrapers.free_work_en import FreeWorkEn
from scrapers.free_work_fr import FreeWorkFr
from scrapers.choose_your_boss import ChooseYourBoss
from utils.webdriver import init_webdriver
from db.database import insert_scraping_history
import mysql.connector
from datetime import datetime
import os
import csv
import pandas as pd
import sys


app = Flask(__name__)
CORS(app)

    
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


@app.route('/export-csv', methods=['GET'])
def export_csv():
    # Récupérer le nom du site à partir de la requête
    site_name = request.args.get('site')

    # Sélectionnez le scraper en fonction du nom du site
    if site_name == 'Free Work En':
        scraper = FreeWorkEn(init_webdriver())
        csv_file = os.path.join(os.path.dirname(__file__), '..', 'csv', 'free_work_en.csv')
    elif site_name == 'Free Work Fr':
        scraper = FreeWorkFr(init_webdriver())
        csv_file = os.path.join(os.path.dirname(__file__), '..', 'csv', 'free_work_fr.csv')
    elif site_name == 'Choose Your Boss':
        scraper = ChooseYourBoss(init_webdriver())
        csv_file = os.path.join(os.path.dirname(__file__), '..', 'csv', 'choose_your_boss.csv')
    else:
        return jsonify({"error": "Site non pris en charge"}), 400

    # Scraper les données pour le site spécifié
    data = scraper.scrape_jobs()

    if data:
        try:
            # Convertir les données en DataFrame Pandas pour inspection
            df = pd.DataFrame(data)

             # Réorganiser les colonnes selon votre structure souhaitée
            df = df[['unique_id', 'title', 'company','logo_url', 'location', 'job_type', 'salary', 'experience', 'description' ]]

            # Afficher le DataFrame dans la console Flask pour inspection
            print("DataFrame Pandas des offres avant l'exportation en CSV :")
            print(df)  

            # Écrire les données dans un fichier CSV
            csv_file_path = os.path.abspath(csv_file)
            df.to_csv(csv_file_path, index=False)

            # Renvoyer le fichier CSV en tant que pièce jointe
            return send_file(csv_file_path, as_attachment=True)
        except Exception as e:
            return jsonify({"error": f"Erreur lors de l'exportation en CSV : {str(e)}"}), 500
    else:
        return jsonify({"error": "Aucune donnée à exporter"}), 404


if __name__ == '__main__':
    app.run(debug=True)

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


# Fonction pour récupérer les détails du site à partir de l'ID
def get_site_details(site_id):
    try:
        conn = mysql.connector.connect(
            user='root',
            password='Ibtihel456@Chniti',
            host='localhost',
            database='scraping_management',
            port=3306
        )
        cursor = conn.cursor(dictionary=True)

        # Sélectionner les détails du site à partir de l'ID
        query = "SELECT site_name, site_url FROM scrap_config WHERE site_id = %s"
        cursor.execute(query, (site_id,))
        site_details = cursor.fetchone()

        if site_details:
            return site_details
        else:
            return None
    except mysql.connector.Error as err:
        print(f"Erreur MySQL: {err}")
        return None
    finally:
        if conn and conn.is_connected():
            if cursor:
                cursor.close()
            conn.close()


@app.route('/site-details/<int:site_id>', methods=['GET'])
def get_site_details_route(site_id):
    site_details = get_site_details(site_id)
    if site_details:
        return jsonify(site_details)
    else:
        return jsonify({"error": "Site non trouvé"}), 404


# Route pour le scraping du site Free Work En
@app.route('/scrape-en', methods=['GET'])
def scrape_jobs_en():
    try:
        driver = init_webdriver()

        # Récupérer l'URL du site à partir de la base de données
        site_id = 1  # ID du site Free Work En
        site_details = get_site_details(site_id)
        if site_details:
            site_url = site_details['site_url']
        else:
            return jsonify({"success": False, "message": "URL du site non trouvé dans la base de données."}), 404

        scraper = FreeWorkEn(driver, site_url)  # Passer l'URL récupéré au scraper
        scraper.scrape_jobs()

        # Insérer les données dans la base de données pour succès
        insert_scraping_history(datetime.now(), "Success", site_url)

        return jsonify({"success": True, "message": "Scraping terminé avec succès."})
    except Exception as e:
        # En cas d'erreur, insérer l'échec dans la base de données
        insert_scraping_history(datetime.now(), "Failed", site_url)
        return jsonify({"success": False, "message": str(e)})


# Route pour le scraping du site Free Work Fr
@app.route('/scrape-fr', methods=['GET'])
def scrape_jobs_fr():
    try:
        driver = init_webdriver()

        # Récupérer l'URL du site à partir de la base de données
        site_id = 2  # ID du site Free Work Fr
        site_details = get_site_details(site_id)
        if site_details:
            site_url = site_details['site_url']
        else:
            return jsonify({"success": False, "message": "URL du site non trouvé dans la base de données."}), 404

        scraper = FreeWorkFr(driver, site_url)  # Passer l'URL récupéré au scraper
        scraper.scrape_jobs()

        # Insérer les données dans la base de données pour succès
        insert_scraping_history(datetime.now(), "Success", site_url)

        return jsonify({"success": True, "message": "Scraping terminé avec succès."})
    except Exception as e:
        # En cas d'erreur, insérer l'échec dans la base de données
        insert_scraping_history(datetime.now(), "Failed", site_url)
        return jsonify({"success": False, "message": str(e)})


# Route pour le scraping du site Choose Your Boss
@app.route('/scrape-ch', methods=['GET'])
def scrape_jobs_ch():
    try:
        driver = init_webdriver()

        # Récupérer l'URL du site à partir de la base de données
        site_id = 3  # ID du site Choose Your Boss
        site_details = get_site_details(site_id)
        if site_details:
            site_url = site_details['site_url']
        else:
            return jsonify({"success": False, "message": "URL du site non trouvé dans la base de données."}), 404

        scraper = ChooseYourBoss(driver, site_url)  # Passer l'URL récupéré au scraper
        scraper.scrape_jobs()

        # Insérer les données dans la base de données pour succès
        insert_scraping_history(datetime.now(), "Success", site_url)

        return jsonify({"success": True, "message": "Scraping terminé avec succès."})
    except Exception as e:
        # En cas d'erreur, insérer l'échec dans la base de données
        insert_scraping_history(datetime.now(), "Failed", site_url)
        return jsonify({"success": False, "message": str(e)})


# Route pour récupérer l'historique de scraping
@app.route('/scraping-history', methods=['GET'])
def get_scraping_history():
    try:
        conn = mysql.connector.connect(
            user='root',
            password='Ibtihel456@Chniti',
            host='localhost',
            database='scraping_management',
            port=3306
        )
        cursor = conn.cursor(dictionary=True)

        scraping_history = []

        # Sélectionner les informations d'historique de scraping depuis la base de données
        query = "SELECT site_url, scraping_date, scraping_status FROM scraping_history ORDER BY scraping_date DESC"
        cursor.execute(query)
        history_data = cursor.fetchall()

        # Formatage des données récupérées
        for row in history_data:
            site_info = {
                "site_url": row['site_url'],
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
    site_id = request.args.get('site_id')  # Récupérer l'ID du site à partir de la requête

    # Récupérer les détails du site à partir de l'ID
    site_details = get_site_details(site_id)
    if not site_details:
        return jsonify({"error": "Détails du site non trouvés"}), 404

    # Sélectionner le scraper en fonction de l'ID du site
    scraper = None
    if site_id == 1:
        scraper = FreeWorkEn(init_webdriver(), site_details['site_url'])
    elif site_id == 2:
        scraper = FreeWorkFr(init_webdriver(), site_details['site_url'])
    elif site_id == 3:
        scraper = ChooseYourBoss(init_webdriver(), site_details['site_url'])
    else:
        return jsonify({"error": "Site non pris en charge"}), 400

    try:
        # Scraper les données pour le site spécifié
        data = scraper.scrape_jobs()

        if data:
            # Convertir les données en DataFrame Pandas
            df = pd.DataFrame(data)

            # Réorganiser les colonnes selon la structure souhaitée
            df = df[['unique_id', 'title', 'company', 'location', 'job_type', 'salary', 'experience', 'description', 'logo_url']]

            # Générer un nom de fichier unique basé sur le timestamp actuel
            timestamp = int(time.time())
            csv_file_name = f'{site_details["site_name"].lower().replace(" ", "_")}_{timestamp}.csv'
            csv_file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'csv', csv_file_name))

            # Écrire les données dans un nouveau fichier CSV
            df.to_csv(csv_file_path, index=False, encoding='utf-8-sig')

            # Insérer les données dans la base de données pour succès lors de l'exportation en CSV
            insert_scraping_history(datetime.now(), "Success", site_details['site_url'])

            # Retourner le chemin du fichier CSV pour téléchargement
            return send_from_directory(os.path.dirname(csv_file_path), csv_file_name, as_attachment=True)
        else:
            return jsonify({"error": "Aucune donnée à exporter"}), 404
    except Exception as e:
        # En cas d'erreur, insérer l'échec dans la base de données
        insert_scraping_history(datetime.now(), "Failed", f"Export CSV - Site ID: {site_id}")
        return jsonify({"error": f"Erreur lors de l'exportation en CSV : {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
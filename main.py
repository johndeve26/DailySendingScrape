import os
from generate_characters import generate_unique_code
from send_csv_as_email import send_email_with_two_csv
from listing_from_crexi import CrexiListings
from listing_from_xome import XomeListings
from save_to_csv import SaveToCSV
import datetime


def run():
    time = datetime.datetime.now()
    today_date = time.strftime('%c').replace(' ', '_')
    # Generate a unique code
    generated_code = generate_unique_code()

    crexi = CrexiListings('https://www.google.com', f'crexi', generated_code)
    try:
        # Crexi listings operation
        crexi.operate()
    except Exception as e:
        print(f"Error with Crexi listings: {e}")
    finally:
        crexi.close_driver()

    xome = XomeListings('https://www.xome.com/listing/listingsearch.aspx', f'xome', generated_code)
    try:
        xome.operate()
    except Exception as e:
        print(f"Error with Xome listings: {e}")
    finally:
        xome.close_driver()

    try:
        # Saving to CSV for Xome listings
        save_to_csv_xome = SaveToCSV(f'xome', generated_code, today_date)
        save_to_csv_xome.save_to_csv()

        # Saving to CSV for Crexi listings
        save_to_csv_crexi = SaveToCSV(f'crexi', generated_code, today_date)
        save_to_csv_crexi.save_to_csv()

        # Emailing the CSV files
        sender_email = 'towerslist@gmail.com'
        sender_password = 'zeeu qkwv cewp uent'
        # receiver_email = 'deals@hilton-global.com'
        receiver_email = 'contact@smartlancedesigns.com'
        subject = 'New Listing Update'
        body = 'Please find both CSV files attached.'

        # List of file paths to the CSV files you want to send
        file_paths = [f'crexi/listing_CSV/crexi_new_listings_for_{today_date}.csv',
                      f'xome/listing_CSV/xome_new_listings_for_{today_date}.csv']

        send_email_with_two_csv(sender_email, sender_password, receiver_email, subject, body, file_paths)

        print("CSV files sent successfully!")

    except Exception as e:
        print(f"Error saving or sending email: {e}")

    with open('search_terms.txt', 'r') as file:
        all_files = [each_search.strip() for each_search in file.readlines()]

    for each_crexi_file in all_files:
        try:
            os.remove(f'crexi/{each_crexi_file}_{generated_code}_new.txt')
        except:
            pass

    for each_xome_file in all_files:
        try:
            os.remove(f'xome/{each_xome_file}_{generated_code}_new.txt')
        except:
            pass

    try:
        os.remove(f'crexi/listing_CSV/crexi_new_listings_for_{today_date}.csv')
    except:
        pass

    try:
        os.remove(f'xome/listing_CSV/xome_new_listings_for_{today_date}.csv')
    except:
        pass


run()

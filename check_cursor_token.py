import argparse
import requests
from tokenManager.cursor import Cursor

def check_token(token):
    try:
        # Kalan kullanım hakkını kontrol et
        remaining_balance = Cursor.get_remaining_balance(token)
        
        # Deneme süresinden kalan günü kontrol et
        remaining_days = Cursor.get_trial_remaining_days(token)
        
        print("\n=== Cursor Token Bilgileri ===")
        print(f"Token: {token}")
        
        if remaining_balance is not None:
            print(f"Kalan GPT-4 Kullanım Hakkı: {remaining_balance}")
        else:
            print("GPT-4 kullanım bilgisi alınamadı")
            
        if remaining_days is not None:
            print(f"Deneme Süresinden Kalan Gün: {remaining_days}")
        else:
            print("Deneme süresi bilgisi alınamadı")
            
        print("\nKullanılabilir Modeller:")
        for model in Cursor.models:
            print(f"- {model}")
            
    except requests.exceptions.RequestException as e:
        print(f"\nHata: API'ye bağlanırken bir sorun oluştu")
        print(f"Detay: {str(e)}")
    except Exception as e:
        print(f"\nHata: Beklenmeyen bir hata oluştu")
        print(f"Detay: {str(e)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cursor Token Kontrol Aracı')
    parser.add_argument('--token', type=str, help='Cursor token')
    
    args = parser.parse_args()
    
    if args.token:
        check_token(args.token)
    else:
        token = input("Lütfen Cursor token'ınızı girin: ")
        check_token(token) 
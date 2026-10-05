# Port Scanner

Python ile yazılmış, çok iş parçacıklı (multithreaded) basit bir TCP port tarayıcı. Belirtilen hedefteki açık portları tespit eder, bilinen servisleri eşler ve mümkünse banner (servis bilgisi) çeker.

> ⚠️ Yalnızca sahibi olduğunuz veya tarama izniniz olan sistemler üzerinde kullanın. İzinsiz tarama birçok ülkede/yerde yasa dışıdır.

## Özellikler

- Çok iş parçacıklı (threading) hızlı tarama
- Port aralığı veya tekil port listesi desteği (`1-1000`, `22,80,443`)
- Yaygın portlar için servis ismi tahmini
- Banner grabbing (mümkünse servisin kendini tanıtan verisini okur)
- Sonuçları JSON dosyasına kaydetme

## Gereksinimler

- Python 3.x
- Harici kütüphane gerekmez (standart kütüphane yeterli)

## Kullanım

```bash
python PortScanner.py <hedef>
```

### Örnekler

```bash
# Varsayılan port aralığı (1-1024) ile tarama
python PortScanner.py 192.168.1.1

# Belirli port aralığı ve 200 thread ile
python PortScanner.py 192.168.1.1 -p 1-1000 -t 200

# Belirli portlar, sonucu dosyaya kaydet
python PortScanner.py example.com -p 22,80,443 -o sonuc.json
```

### Parametreler

| Parametre | Açıklama | Varsayılan |
|---|---|---|
| `target` | Hedef IP adresi veya domain | - |
| `-p`, `--ports` | Taranacak portlar (`1-1000` veya `22,80,443`) | `1-1024` |
| `-t`, `--threads` | Eş zamanlı thread sayısı | `100` |
| `--timeout` | Bağlantı zaman aşımı (saniye) | `0.5` |
| `-o`, `--output` | Sonuçları JSON dosyasına kaydet | - |

## Örnek Çıktı

```
Hedef: 127.0.0.1 (127.0.0.1)
Taranacak port sayısı: 1024
Başlangıç: 2026-10-05 14:30:00

--------------------------------------------------
[+] Port 135    AÇIK  | Servis: Bilinmiyor
[+] Port 139    AÇIK  | Servis: NetBIOS
[+] Port 445    AÇIK  | Servis: SMB
--------------------------------------------------
Tarama tamamlandı. 3 açık port bulundu.
```

## Geliştirme Fikirleri

- UDP port tarama desteği
- SYN scan (root/admin yetkisiyle daha hızlı tarama)
- Çıktıyı renkli/tablo formatında gösterme
- CVE veritabanı ile basit zafiyet eşleştirme

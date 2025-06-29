# automate-create-task-jira



## Getting started

To make it easy for you to get started with GitLab, here's a list of recommended next steps.

Already a pro? Just edit this README.md and make it your own. Want to make it easy? [Use the template at the bottom](#editing-this-readme)!

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/topics/git/add_files/#add-files-to-a-git-repository) or push an existing Git repository with the following command:

```
cd existing_repo
git remote add origin https://github.com/salis21n/automate-create-task-jira.git
git branch -M main
git push -uf origin main
```

Berikut adalah dokumentasi lengkap dalam format **Markdown** untuk kode Python yang Anda berikan, termasuk panduan untuk **deploy di Docker** menggunakan Dockerfile dan menjalankan dengan `docker run --rm`.

---

# Dokumentasi Batch Jira Task Creator

## Deskripsi

Script Python ini digunakan untuk membuat tugas (task) Jira secara batch berdasarkan data dari file CSV. Script ini mendukung fitur-fitur:

- Membaca data task dari file CSV.
- Mendapatkan tipe isu (issue type) "Task" di tiap project.
- Mendapatkan ID custom field Jira dinamically (misal: Epic Link).
- Mendapatkan `accountId` user berdasarkan email, dengan fallback jika tidak ditemukan.
- Membuat tugas dengan payload yang sesuai, termasuk deskripsi dalam format Atlassian Document Format (ADF).
- Mengisi tanggal mulai (`start date`) dan tanggal selesai (`due date`) pada custom field.
- Melakukan transisi status tugas ke "Done" secara otomatis dengan transition ID yang diberikan.

---

## Persiapan

1. **File CSV**  
   File CSV harus memiliki kolom yang minimal meliputi:  
   - `project-key` (misal: SYS)  
   - `title-task` (judul tugas)  
   - `desc-task` (deskripsi tugas)  
   - `due-date` (tanggal selesai, format `YYYY-MM-DD`)  
   - `epic-code` (kode Epic jika ada, bisa dikosongkan)  
   - `assign` (email assignee)

2. **Konfigurasi**  
   Variabel konfigurasi pada script perlu diubah sesuai dengan Jira instance dan akun Anda:
   ```python
   JIRA_URL = "https://your_url_jira.atlassian.net"  # URL Jira Anda
   EMAIL = "your_jira_email_here"  # Email login Jira Anda
   API_TOKEN = "your_jira_api_token_here"  # API Token Jira Anda
   FALLBACK_ACCOUNT_ID = "your_jira_account_id_here"
   START_DATE_CUSTOM_FIELD = "customfield_xxxxx"  # Ganti dengan ID custom field Start Date
   TRANSITION_ID_DONE = "xxx"  # Ganti dengan ID transisi ke Done
   ```

---

## Cara Kerja Script

- Script akan mengelompokkan task berdasarkan `due-date` sehingga dapat memproses batch task per tanggal tertentu.
- Setiap task dibuat dengan mengisi field summary, description, assignee, due date, start date, dan epic link (jika ada).
- Jika lookup email assignee gagal menemukan accountId, akan menggunakan fallback accountId.
- Setelah task berhasil dibuat, script akan otomatis melakukan transisi status task ke "Done" menggunakan API Jira.

---

## Docker Deployment

### Dockerfile

Buat file bernama `Dockerfile` dengan isi berikut:

```Dockerfile
FROM python:alpine

WORKDIR /jira

COPY . .

RUN pip install pandas requests openpyxl

CMD ["sh", "-c", "python your_script_name.py data.csv"]

```

> **Catatan:** Ganti `your_script_name.py` dengan nama file Python script Anda.

---

### Menjalankan Docker Container

1. **Build image Docker:**

```sh
docker build -t jira-batch-task-creator .
```

2. **Jalankan container dengan file CSV di-mount dari host agar bisa diakses script:**

```sh
docker run --rm -v /path/ke/folder/csv:/app jira-batch-task-creator
```

Gantilah `/path/ke/folder/csv` dengan path folder aktual di komputer Anda yang berisi file `data.csv`.

---

## Contoh Pemanggilan Script

Jika ingin menjalankan secara langsung (tanpa Docker):

```bash
python your_script_name.py
```

Script akan otomatis membaca file `data.csv` di direktorinya.

---

## Hal yang Perlu Diperhatikan

- Pastikan API token sudah benar dan memiliki izin akses yang cukup di Jira.
- Jika tidak mendapatkan `accountId` dari email, pastikan email sudah terdaftar di Jira dan dapat diakses oleh API.
- Transition ID "41" harus valid di workflow Jira project Anda untuk transisi ke status "Done".
- CSV harus berformat benar dan kolom konsisten.
